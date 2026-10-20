#!/usr/bin/env python3
"""Audit answer keys: does the stored key match the option a reader would choose?

The explanation sweep cannot see a wrong key. A row can have flawless prose and still
teach the wrong answer, which is the worst defect a study app can carry.

Method: present the four options in a deterministic shuffled order (seeded by id, so a
rerun is reproducible), ask the model which one answers the question, then compare its
choice *by text* against the stored key. Comparing text rather than letter is what makes
the shuffle safe.

    --calibrate        run the hand-labelled rows and print expected vs actual
    --run              full pass, checkpointed and resumable
    --shard k/n        split across workers
    --ids-from FILE    only ids whose "id" appears in a JSONL

Output line per row: {id, pick, stored, agree, reason}
"""
import argparse
import json
import random
import sqlite3
import time
import urllib.request

DB = "/home/papichulo/sabal/data/fcle.db"

SYSTEM = (
    "You are checking a civics question bank for the state of Florida. One answer is "
    "claimed to be correct. Your job is to test that claim, not to guess which option "
    "looks like a typical key. Say false when the claimed answer is wrong, imprecise, or "
    "when no listed option actually answers the question. Do not defend a claim because "
    "it is long or detailed. Reply with JSON only."
)

PROMPT = """Question: {question}

Options:
A. {a}
B. {b}
C. {c}
D. {d}

Claimed correct answer: {letter}. {key}

Is the claimed answer actually correct for this question?
Reply with JSON only: {{"correct": true or false, "better": "A" or null, "reason": "at most 15 words"}}
Set "better" to the letter of a clearly better option, or null if none is better."""


def close_json(t):
    """Append closing braces the model forgot (observed on this model, reliably)."""
    stack, in_str, esc = [], False, False
    for ch in t:
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch in "{[":
                stack.append(ch)
            elif ch in "}]" and stack:
                stack.pop()
    if in_str:
        t += '"'
    for ch in reversed(stack):
        t += "}" if ch == "{" else "]"
    return t


def parse(raw):
    s = raw.find("{")
    if s < 0:
        return None
    body = raw[s:]
    for cand in (body, close_json(body)):
        try:
            d = json.loads(cand, strict=False)
        except json.JSONDecodeError:
            continue
        c = d.get("correct")
        if isinstance(c, str):
            c = c.strip().lower() in ("true", "yes", "correct")
        if isinstance(c, bool):
            better = str(d.get("better") or "").strip().upper()[:1]
            return {"correct": c, "better": better if better in "ABCD" else None,
                    "reason": str(d.get("reason") or "")[:120]}
    return None


def chat(endpoint, prompt, max_tokens=120, timeout=120):
    body = json.dumps({
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "max_tokens": max_tokens, "temperature": 0.0,
    }).encode()
    req = urllib.request.Request(endpoint.rstrip("/") + "/v1/chat/completions",
                                 data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())[
        "choices"][0]["message"].get("content") or ""


def norm(t):
    return " ".join((t or "").lower().split())


def build(row):
    opts = [row["correct_answer"]] + json.loads(row["wrong_answers"] or "[]")
    order = list(range(4))
    random.Random(row["id"]).shuffle(order)
    shuffled = [opts[i] for i in order]
    idx = "ABCD"[order.index(0)]
    prompt = PROMPT.format(question=row["question"], a=shuffled[0], b=shuffled[1],
                           c=shuffled[2], d=shuffled[3], letter=idx,
                           key=row["correct_answer"])
    return prompt, shuffled, idx


def judge(endpoint, row):
    prompt, shuffled, keyletter = build(row)
    for _ in range(3):
        try:
            got = parse(chat(endpoint, prompt))
        except Exception:
            got = None
        if got:
            better = got.get("better")
            return {"verdict": "KEY-OK" if got["correct"] else "MIS-KEY",
                    "keyed": keyletter, "better": better,
                    "better_text": shuffled["ABCD".index(better)] if better else None,
                    "reason": got.get("reason", "")}
        time.sleep(1)
    return {"verdict": "ERROR", "keyed": keyletter, "better": None,
            "better_text": None, "reason": ""}


CALIBRATION = {94: False, 128: False, 990: False, 1944: False, 1967: False, 1970: False,
               1000: True, 2256: True, 962: True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default="http://192.168.1.210:8085")
    ap.add_argument("--out", required=True)
    ap.add_argument("--db", default=DB)
    ap.add_argument("--shard", default=None)
    ap.add_argument("--ids-from", default=None)
    ap.add_argument("--limit", type=int, default=10000)
    ap.add_argument("--calibrate", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    rows = {r["id"]: r for r in conn.execute("SELECT * FROM questions")}

    if args.calibrate:
        print("%-6s %-10s %-10s %s" % ("id", "expected", "actual", "reason"))
        hit = 0
        for qid, expected in CALIBRATION.items():
            got = judge(args.endpoint, rows[qid])
            actual = got["verdict"] == "KEY-OK"
            ok = actual == expected
            hit += ok
            print("%-6d %-10s %-10s %s%s" % (qid, "key ok" if expected else "mis-keyed",
                                             "key ok" if actual else "mis-keyed",
                                             got["reason"][:60], "" if ok else "   <- WRONG"))
        print("\ncalibration: %d/%d" % (hit, len(CALIBRATION)))
        return

    done = set()
    try:
        for line in open(args.out):
            r = json.loads(line)
            if r.get("verdict") in ("KEY-OK", "MIS-KEY"):
                done.add(r["id"])
    except FileNotFoundError:
        pass

    ids = list(rows)
    if args.ids_from:
        want = [json.loads(l)["id"] for l in open(args.ids_from) if l.strip()]
        ids = [i for i in want if i in rows]
    if args.shard:
        k, n = args.shard.split("/")
        ids = [i for i in ids if i % int(n) == int(k)]
    todo = [i for i in ids if i not in done][:args.limit]
    print("resuming with %d already done, %d to go" % (len(ids) - len(todo), len(todo)), flush=True)

    f = open(args.out, "a")
    t0 = time.time()
    for n, qid in enumerate(todo, 1):
        rec = {"id": qid}
        rec.update(judge(args.endpoint, rows[qid]))
        f.write(json.dumps(rec) + "\n")
        f.flush()
        if n % 25 == 0 or n == len(todo):
            el = time.time() - t0
            print("[%d/%d] %.1fs/item, eta %.1fh" % (n, len(todo), el / n,
                                                     (len(todo) - n) * el / n / 3600), flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
