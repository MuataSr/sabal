#!/usr/bin/env python3
"""Targeted audit + surgical fix for the 'extra rebuttals' defect in the FCLE bank.

The shape, found by rendering question 1365 on a public practice page:

    the explanation argues against distractors that are not this question's
    distractors ("The claim that <scenario> is incorrect because..."), because
    the prose was assembled against a different option set. The key and the
    per-option wrong_explanations are fine; only the extra sentences are wrong.

Heuristic audit is not enough on its own: entity-based scans flag ~230 rows,
almost all of which legitimately name a doctrine the question tests without
naming it in the options ("violated the Equal Protection Clause"). So the test
here is narrower and two-sided: the explanation must carry MORE rebuttals than
the question has distractors, AND at least one rebuttal must name an instrument
(Amendment / Clause / Act) that no option mentions. That is the 1365 shape.

Run with --apply to write the fix (a backup is taken first, always).
Default is dry-run.
"""
import argparse
import json
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone

DB = "/home/papichulo/sabal/data/fcle.db"
BACKUP_DIR = "/home/papichulo/.hermes/cache/scratch/sabal-audit"

ORD = ("First Second Third Fourth Fifth Sixth Seventh Eighth Ninth Tenth Eleventh Twelfth Thirteenth "
       "Fourteenth Fifteenth Sixteenth Seventeenth Eighteenth Nineteenth Twentieth Twenty-First "
       "Twenty-Second Twenty-Third Twenty-Fourth Twenty-Fifth Twenty-Sixth Twenty-Seventh").split()
INSTR = re.compile(r"\b(?:%s)\s+Amendment\b|\b[A-Z][a-zA-Z]+\s+Clause\b|\b[A-Z][a-zA-Z]+\s+Act\b"
                   % "|".join(ORD))
REBUT = re.compile(r"the claim that (.{20,400}?)(?: is incorrect| is wrong| is false)", re.I | re.S)


def find(conn):
    out = []
    for r in conn.execute("SELECT * FROM questions ORDER BY id"):
        ex = r["explanation"] or ""
        wrongs = json.loads(r["wrong_answers"] or "[]")
        clauses = REBUT.findall(ex)
        if len(clauses) > len(wrongs) and len(clauses) >= 2:
            opts = " ".join([r["correct_answer"] or ""] + wrongs).lower()
            stray = sorted({i for i in INSTR.findall(" ".join(clauses)) if i.lower() not in opts})
            if stray:
                out.append((r["id"], len(clauses), len(wrongs), stray))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    shaped = find(conn)
    print("rows matching the excess-rebuttal shape: %d" % len(shaped))
    for qid, n_clauses, n_wrongs, stray in shaped:
        print("   id %-5d rebuttals=%d distractors=%d stray=%s"
              % (qid, n_clauses, n_wrongs, stray))

    if not args.apply:
        print("\ndry run; pass --apply to write the fix")
        return

    if not shaped:
        print("\nnothing to fix")
        return

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    import os
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup = "%s/fcle.db.bak-%s" % (BACKUP_DIR, ts)
    shutil.copyfile(DB, backup)
    print("\nbackup: %s" % backup)

    for qid, _n, _w, _s in shaped:
        row = conn.execute("SELECT explanation FROM questions WHERE id=?", (qid,)).fetchone()
        old = row["explanation"]
        keep = old.split("The claim that")[0].rstrip()
        if not keep.endswith(".") or len(keep) < 80:
            print("   SKIP id %d: split point looks wrong, leaving it alone" % qid)
            continue
        conn.execute("UPDATE questions SET explanation=? WHERE id=?", (keep, qid))
        print("   FIXED id %d: %d -> %d chars, dropped %d orphan rebuttals"
              % (qid, len(old), len(keep), len(re.findall(r"The claim that", old))))
    conn.commit()
    print("\ncommitted")


if __name__ == "__main__":
    sys.exit(main())
