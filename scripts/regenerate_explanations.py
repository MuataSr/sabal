#!/usr/bin/env python3
"""Regenerate explanations that were written against the wrong option set.

The defect the sweep found: prose that rebuts distractors the question does not
carry. Patching sentences out of that prose leaves a hole; the honest fix is prose
written with all four options in view, which is what this does.

The constraint that matters, learned from the 413 defects: the generator is told to
rebut ONLY option text it can see, to treat outside doctrines as background at most,
and never to introduce a clause, case or scenario absent from the row. The previous
generation had no such instruction, which is how a Bible-oath scenario ended up
explaining a question about judicial activism.

Output is JSONL with before and after, one line per row, checkpointed. Nothing is
written to the database here; apply after review and after the audit re-run.

    python3 scripts/regenerate_explanations.py --ids-from flagged.jsonl --limit 20 \
        --endpoint http://host:8085 --out pilot20.jsonl
"""
import argparse
import json
import os
import sqlite3
import time
import urllib.request

DB = "/home/papichulo/sabal/data/fcle.db"

SYSTEM = ("You rewrite explanations for a civics practice bank. You answer with JSON only, "
          "no preamble, no markdown.")

PROMPT = """Rewrite the explanation for this question.

QUESTION
{question}

A (the correct answer)
{correct}

B
{w1}

C
{w2}

D
{w3}

Write:
1. "explanation": 2 to 3 sentences, at most 70 words total. Say why A is correct,
   then say why B, C and D are wrong, referring to what each option actually says.
2. "wrong_explanations": exactly three strings, in the order B, C, D. Each ONE
   sentence, at most 30 words: why a student might choose it, and why it is wrong.

Hard rules:
- Rebut only text that appears in B, C or D above. Never answer a distractor that is
  not printed here.
- Do not introduce any law, case, clause, amendment, doctrine or scenario that is not
  in the question or the four options. Background references are allowed only if they
  are the subject of the question itself.
- Never begin a sentence with "The claim that" or "The assertion that".
- No commentary about the exam, the student or the format.
- Be brief. Long answers are rejected.

Return exactly:
{{"explanation": "...", "wrong_explanations": ["...", "...", "..."]}}"""


def chat(endpoint, prompt, max_tokens=900, timeout=240):
    body = json.dumps({
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "max_tokens": max_tokens, "temperature": 0.2,
    }).encode()
    req = urllib.request.Request(endpoint.rstrip("/") + "/v1/chat/completions",
                                 data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode())
    m = d["choices"][0]["message"]
    return (m.get("content") or "") + (m.get("reasoning_content") or "")


def parse(raw):
    s, e = raw.find("{"), raw.rfind("}")
    if s < 0 or e <= s:
        return None
    try:
        d = json.loads(raw[s:e + 1])
    except json.JSONDecodeError:
        return None
    ex, wx = d.get("explanation"), d.get("wrong_explanations")
    if not isinstance(ex, str) or len(ex) < 80:
        return None
    if not isinstance(wx, list) or len(wx) != 3 or not all(isinstance(x, str) and len(x) > 40 for x in wx):
        return None
    if "the claim that" in ex.lower()[:40]:
        return None
    return ex.strip(), [x.strip() for x in wx]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default="http://192.168.1.210:8085")
    ap.add_argument("--ids-from", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--db", default=DB)
    args = ap.parse_args()

    want = []
    with open(args.ids_from) as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                if rec.get("verdict") == "FLAG":
                    want.append(rec["id"])
    want = want[:args.limit]

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    done = set()
    if os.path.exists(args.out):
        with open(args.out) as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if rec.get("ok"):      # failures are retried, not treated as done
                    done.add(rec["id"])
    out = open(args.out, "a")
    t0 = time.time()
    ok = 0
    for i, qid in enumerate([w for w in want if w not in done], 1):
        row = conn.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()
        if row is None:
            print("  id %d missing (retired?)" % qid)
            continue
        wrongs = json.loads(row["wrong_answers"] or "[]")
        while len(wrongs) < 3:
            wrongs.append("(none)")
        prompt = PROMPT.format(question=row["question"], correct=row["correct_answer"],
                               w1=wrongs[0], w2=wrongs[1], w3=wrongs[2])
        t = time.time()
        try:
            raw = chat(args.endpoint, prompt)
            got = parse(raw)
            if got is None:
                raw = chat(args.endpoint, prompt)
                got = parse(raw)
        except Exception as ex:
            got = None
            raw = str(ex)[:120]
        rec = {"id": qid, "ok": got is not None, "secs": round(time.time() - t, 1),
               "before": {"explanation": row["explanation"],
                          "wrong_explanations": json.loads(row["wrong_explanations"] or "[]")}}
        if got:
            rec["after"] = {"explanation": got[0], "wrong_explanations": got[1]}
            ok += 1
        else:
            rec["raw"] = raw[:300]
        out.write(json.dumps(rec) + "\n")
        out.flush()
        print("[%d/%d] id=%d %s %.1fs" % (i, len(want), qid, "OK" if got else "FAIL", rec["secs"]), flush=True)
    print("done: %d ok of %d, %.1fs/item" % (ok, len(want), (time.time() - t0) / max(len(want), 1)))


if __name__ == "__main__":
    main()
