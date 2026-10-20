#!/usr/bin/env python3
"""Propose sentence-level repairs for the flagged explanations, from the sweep evidence.

The sweep found 413 candidate rows. A second model agrees on 72% of a random 60, so
the list is actionable but not clean. Re-running the whole set through the slower
judge would cost hours to remove noise that still has to be read one row at a time.

This turns the existing evidence into PROPOSED EDITS instead:

  * split each flagged explanation into sentences
  * keep only sentences that are rebuttal-shaped ("The claim that ...", "The
    statement that ...", "The assertion that ...", "... is incorrect because ...")
  * score each against the four options using distinctive words only (>=5 chars,
    stop words removed), because legal prose shares "state", "law", "court"
  * a rebuttal sentence that matches NO option on at least two distinctive words is
    a candidate for deletion
  * the sweep's own evidence string is used as corroboration, never as the sole
    reason

Output is a JSONL of proposed edits plus a human-readable summary. NOTHING is
written to the database here. Apply only after review.

    python3 scripts/propose_explanation_repairs.py
    python3 scripts/propose_explanation_repairs.py --min-words 3 --show 15
"""
import argparse
import collections
import glob
import json
import re
import sqlite3

DB = "data/fcle.db"
SWEEP = "/home/papichulo/.hermes/workspace/sabal-sweep/shard*.jsonl"
OUT = "/home/papichulo/.hermes/workspace/sabal-sweep/proposed-repairs.jsonl"

STOP = set("""their there these those which while where about because between through during
without within against among above after again before below under until being other another
however therefore since would could should shall might must does have been were was are this
that with from into what when whom whose they them then than only also more most some such
option options answer answers claim claims statement statements assertion assertions explanation
correct incorrect wrong false true question questions""".split())

REBUTTAL = re.compile(
    r"^(the (claim|statement|assertion|option|answer|idea)\b|.*\bis (incorrect|wrong|false)\b)",
    re.I)


def words(t):
    return {w for w in re.findall(r"[a-z]{5,}", (t or "").lower()) if w not in STOP}


def sentences(text):
    # keep the period with each sentence; legal prose has few abbreviations here
    parts = re.split(r"(?<=[.?!])\s+", (text or "").strip())
    return [p.strip() for p in parts if p.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-words", type=int, default=2,
                    help="distinctive words a rebuttal must share with an option to count as matched")
    ap.add_argument("--show", type=int, default=12)
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    flagged = {}
    for f in sorted(glob.glob(SWEEP)):
        with open(f) as fh:
            for line in fh:
                rec = json.loads(line)
                if rec.get("verdict") == "FLAG":
                    flagged[rec["id"]] = rec

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = {r["id"]: r for r in conn.execute("SELECT * FROM questions")}

    proposals = []
    for qid, rec in sorted(flagged.items()):
        row = rows.get(qid)
        if row is None:
            continue  # retired
        opts = [row["correct_answer"]] + json.loads(row["wrong_answers"] or "[]")
        opt_words = [words(o) for o in opts]
        evidence = (rec.get("evidence") or "").lower()

        drop = []
        for s in sentences(row["explanation"]):
            if not REBUTTAL.match(s):
                continue
            sw = words(s)
            best = max((len(sw & ow) for ow in opt_words), default=0)
            if best >= args.min_words:
                continue
            # corroboration: the evidence and the sentence must share a rare-ish word
            shared = (sw & words(evidence))
            drop.append({"sentence": s, "best_option_overlap": best,
                         "evidence_shared_words": sorted(shared)[:4]})

        if drop:
            proposals.append({"id": qid, "n_drop": len(drop), "drops": drop,
                              "evidence": rec.get("evidence", "")})

    with open(args.out, "w") as f:
        for p in proposals:
            f.write(json.dumps(p) + "\n")

    counts = collections.Counter(p["n_drop"] for p in proposals)
    print("flagged rows: %d" % len(flagged))
    print("rows with a proposed deletion: %d (%.0f%%)" % (len(proposals), 100.0 * len(proposals) / max(len(flagged), 1)))
    print("deletions per row: %s" % dict(sorted(counts.items())))
    print("total sentences proposed for deletion: %d" % sum(p["n_drop"] for p in proposals))
    print("rows needing manual authoring (no mechanical deletion found): %d"
          % (len(flagged) - len(proposals)))
    print("\nproposals written to %s" % args.out)

    for p in proposals[:args.show]:
        row = rows[p["id"]]
        print("\n--- id %d | %s" % (p["id"], (row["question"] or "")[:80]))
        for d in p["drops"]:
            print("    DROP (overlap %d): %s" % (d["best_option_overlap"], d["sentence"][:170]))


if __name__ == "__main__":
    main()
