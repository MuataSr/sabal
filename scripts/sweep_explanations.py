#!/usr/bin/env python3
"""Exhaustive sweep: explanations that argue about options the question does not have.

Companion to the 2026-10-20 targeted audit (docs/CONTENT-AUDIT-2026-10-20.md).
The targeted pass found four rows via decisive structural markers; this pass is
semantic, so it can also catch rows where a phantom rebuttal shares vocabulary
with a real option and no regex can separate them.

Design notes that matter:

* **Checkpointed.** One JSON line per row, appended and flushed. Re-running skips
  completed ids. A multi-hour job against a local model WILL be interrupted
  (the Sep 2026 rewrite survived ten unit restarts this way, not by luck).
* **Resumable across model swaps.** The row id is the key; the judge name is
  recorded so a mixed run is visible rather than silently averaged.
* **Short output on purpose.** The judge returns a verdict and <= 20 words of
  evidence. Long prose both slows the sweep and invites the model to editorialise
  about civics accuracy, which is not the question being asked.
* **Calibration before commitment.** `--calibrate` runs rows whose verdict is
  already known by hand (four confirmed defects from the pre-fix backup, four
  rows reviewed and kept, three known-clean rows). If the judge cannot separate
  those, its output on 2,350 rows is noise and the run should not start.

    python3 scripts/sweep_explanations.py --calibrate --endpoint http://host:8087
    python3 scripts/sweep_explanations.py --run --endpoint http://host:8087
"""
import argparse
import json
import os
import random
import shutil
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

LIVE_DB = "/home/papichulo/sabal/data/fcle.db"
PREFIX_DB = "/home/papichulo/.hermes/cache/scratch/sabal-audit/fcle.db.bak-20261020T131727Z"
WORKDIR = "/home/papichulo/.hermes/workspace/sabal-sweep"

# Ground truth from the 2026-10-20 hand audit.
KNOWN_DEFECT = [1365, 1969, 1087, 2136]      # pre-fix text, read from PREFIX_DB
KNOWN_CLEAN = [2055, 2138, 150, 1425, 82, 147, 1266]

SYSTEM = (
    "You audit a multiple-choice question bank for one specific defect: text that "
    "argues against an option the question does not contain. Reply with JSON only."
)

FEWSHOT = """EXAMPLE of a CLEAN item (note the outside doctrine used as background, which is fine):

QUESTION: Why does Congress struggle to act on local concerns?
OPTIONS: A. national coalition building B. local party control C. state veto D. judicial review
EXPLANATION: Members answer to national coalitions, so local majorities rarely prevail. The
Supremacy Clause makes federal law controlling, which shapes the pressure members feel.
FEEDBACK: B misses the national coalition; C confuses state law with federal supremacy; D
describes courts, not legislatures.
VERDICT: CLEAN. The Supremacy Clause is background, not a rebuttal of a missing option.

Now audit the real item.

"""

TEMPLATE = """QUESTION
{question}

FOUR OPTIONS (A is the key)
A. {correct}
B. {w1}
C. {w2}
D. {w3}

EXPLANATION
{explanation}

PER-OPTION FEEDBACK FOR B, C AND D
{wrong_explanations}

Work in this order:
1. For B, C and D, does its feedback describe that option? If a feedback describes
   something else entirely, it is a mismatch.
2. Does the EXPLANATION quote or rebut a scenario that is not A, B, C or D?
3. A doctrine named as background is NOT a defect. Only a rebuttal or a quote of a
   scenario that is absent counts. Ignore whether the civics is correct.

Reply exactly:
{{"verdict":"FLAG" or "CLEAN","evidence":"<the option letter it should refer to, or the missing scenario in <= 20 words>"}}"""


def build_prompt(row):
    wrongs = json.loads(row["wrong_answers"] or "[]")
    while len(wrongs) < 3:
        wrongs.append("(none)")
    wxs = json.loads(row["wrong_explanations"] or "[]")
    return FEWSHOT + TEMPLATE.format(
        question=row["question"],
        correct=row["correct_answer"],
        w1=wrongs[0], w2=wrongs[1], w3=wrongs[2],
        explanation=row["explanation"],
        wrong_explanations="\n".join("- " + x for x in wxs) or "(none)",
    )


def chat(endpoint, prompt, timeout=180, max_tokens=160):
    body = json.dumps({
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
    }).encode()
    req = urllib.request.Request(endpoint.rstrip("/") + "/v1/chat/completions",
                                 data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode())
    msg = d["choices"][0]["message"]
    return (msg.get("content") or "") + (msg.get("reasoning_content") or "")


def parse(raw):
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        d = json.loads(raw[start:end + 1])
    except json.JSONDecodeError:
        return None
    v = str(d.get("verdict", "")).upper().strip()
    if v not in ("FLAG", "CLEAN"):
        return None
    return {"verdict": v, "evidence": str(d.get("evidence", ""))[:160]}


def read_rows(path, ids=None):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    if ids:
        marks = ",".join("?" * len(ids))
        return conn.execute("SELECT * FROM questions WHERE id IN (%s)" % marks, ids).fetchall()
    return conn.execute("SELECT * FROM questions ORDER BY id").fetchall()


def calibrate(endpoint):
    rows = read_rows(PREFIX_DB, KNOWN_DEFECT + KNOWN_CLEAN)
    by_id = {r["id"]: r for r in rows}
    order = KNOWN_DEFECT + KNOWN_CLEAN
    hits, total, t0 = 0, 0, time.time()
    print("calibration: %d rows (%d known defects, %d known clean)\n"
          % (len(order), len(KNOWN_DEFECT), len(KNOWN_CLEAN)))
    for qid in order:
        row = by_id[qid]
        want = "FLAG" if qid in KNOWN_DEFECT else "CLEAN"
        t = time.time()
        try:
            raw = chat(endpoint, build_prompt(row))
            got = parse(raw)
        except Exception as e:
            print("  id %-5d ERROR %s" % (qid, str(e)[:80]))
            continue
        dt = time.time() - t
        total += 1
        ok = got and got["verdict"] == want
        hits += 1 if ok else 0
        print("  id %-5d want %-5s got %-5s %5.1fs  %s"
              % (qid, want, (got or {}).get("verdict", "PARSE-FAIL"), dt,
                 ("OK" if ok else "MISS: " + (got or {}).get("evidence", raw[:60]))))
    dt = time.time() - t0
    print("\naccuracy %d/%d on hand-labelled rows" % (hits, total))
    print("mean %.1fs/item  -> 2,350 items = %.1f hours at one worker"
          % (dt / max(total, 1), 2350 * (dt / max(total, 1)) / 3600))
    return hits, total


def run(endpoint, out_path, judge, workers=1, limit=None, shard=None, ids_from=None):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    done = set()
    if os.path.exists(out_path):
        with open(out_path) as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                # ERROR and PARSE-FAIL rows are retried on resume; only real
                # verdicts count as done, or a model hiccup silently becomes a
                # permanent hole in the sweep.
                if rec.get("verdict") in ("FLAG", "CLEAN"):
                    done.add(rec["id"])
    if ids_from:
        wanted = []
        for path in ids_from:
            with open(path) as f:
                for line in f:
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    if rec.get("verdict") in ("FLAG", "CLEAN"):
                        wanted.append(rec["id"])
        rows = [r for r in read_rows(LIVE_DB) if r["id"] in set(wanted)]
    else:
        rows = [r for r in read_rows(LIVE_DB) if r["id"] not in done]
    rows = [r for r in rows if r["id"] not in done]
    if shard:
        k, n = shard
        rows = [r for r in rows if r["id"] % n == k]
    if limit:
        rows = rows[:limit]
    print("resuming with %d already done, %d to go" % (len(done), len(rows)))

    out = open(out_path, "a")
    log = open(out_path.replace(".jsonl", ".log"), "a")
    t0 = time.time()
    for i, row in enumerate(rows, 1):
        t = time.time()
        rec = {"id": row["id"], "judge": judge, "ts": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        try:
            raw = chat(endpoint, build_prompt(row))
            got = parse(raw)
            if got is None:
                raw = chat(endpoint, build_prompt(row))  # one retry, then record the failure
                got = parse(raw)
            rec.update(got or {"verdict": "PARSE-FAIL", "evidence": raw[:120]})
        except Exception as e:
            rec.update({"verdict": "ERROR", "evidence": str(e)[:120]})
        rec["secs"] = round(time.time() - t, 2)
        out.write(json.dumps(rec) + "\n")
        out.flush()
        rate = (time.time() - t0) / i
        eta_h = (len(rows) - i) * rate / 3600
        log.write("[%d/%d] id=%d %s %.1fs eta %.1fh\n"
                  % (i, len(rows), rec["id"], rec.get("verdict"), rec["secs"], eta_h))
        log.flush()
        if i % 25 == 0 or i == len(rows):
            print("[%d/%d] %.1fs/item, eta %.1fh" % (i, len(rows), rate, eta_h), flush=True)
    print("DONE")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default="http://192.168.1.210:8087")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--judge", default=None, help="label recorded per row")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--shard", default=None, help="k/n: process only ids where id %% n == k")
    ap.add_argument("--ids-from", action="append", default=None,
                    help="re-judge only ids appearing in this JSONL (repeatable)")
    args = ap.parse_args()

    judge = args.judge or args.endpoint.rsplit("/", 1)[0].split("//")[-1].replace(".", "-")
    shard = None
    if args.shard:
        k, n = args.shard.split("/")
        shard = (int(k), int(n))
    if args.calibrate:
        calibrate(args.endpoint)
    if args.run:
        out = args.out or os.path.join(WORKDIR, "sweep-%s.jsonl" % judge)
        run(args.endpoint, out, judge, limit=args.limit, shard=shard, ids_from=args.ids_from)
    if not (args.calibrate or args.run):
        ap.print_help()


if __name__ == "__main__":
    main()
