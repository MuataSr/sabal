#!/usr/bin/env python3
"""Second repair batch from the 2026-10-20 sweep calibration.

id 1266 (judicial activism vs restraint): the stem, the key and all three
rebuttals in `explanation` are coherent and map to B, C and D. Its three
`wrong_explanations`, however, are federalism essays about the Tenth Amendment,
commandeering and state sovereignty — attached to options about judicial
philosophy. A student who picks B is told about state sovereignty.

Rewritten to address the options that actually ship:
  B  reverses the two philosophies while borrowing both vocabularies
  C  treats activism as legislating and restraint as a duty to vote on every case
  D  inverts which philosophy enforces the Tenth Amendment

Key, stem, options and explanation are unchanged.

    python3 scripts/fix_20261020_batch2.py --apply
"""
import argparse
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path("/home/papichulo/sabal/data/fcle.db")
BACKUP_DIR = Path("/home/papichulo/.hermes/cache/scratch/sabal-audit")

FEEDBACK_1266 = [
    ("A student might pick this because it uses the vocabulary of both philosophies, but it "
     "reverses them: judicial activism reads the text expansively to protect rights it treats as "
     "fundamental, while judicial restraint is the philosophy that defers to the elected branches "
     "and stays closer to the enacted text."),
    ("A student might pick this because activism does shape policy, but judges do not create "
     "statutes. The option also misstates restraint: it means deference to the other branches, "
     "not a duty to vote on every case regardless of the legal arguments."),
    ("A student might pick this because the Tenth Amendment is a real limit on federal power, but "
     "enforcing it strictly is a restraint-oriented, textualist move, not activism. The option "
     "inverts which philosophy is doing what."),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT wrong_explanations FROM questions WHERE id=1266").fetchone()
    current = json.loads(row["wrong_explanations"] or "[]")
    print("id 1266 current feedback (first 120 chars each):")
    for x in current:
        print("   -", x[:120])
    print("\nreplacement:")
    for x in FEEDBACK_1266:
        print("   +", x[:120])

    if not args.apply:
        print("\ndry run; pass --apply")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / ("fcle.db.bak-%s" % datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    shutil.copyfile(DB, backup)
    print("\nbackup: %s" % backup)
    conn.execute("UPDATE questions SET wrong_explanations=? WHERE id=1266",
                 (json.dumps(FEEDBACK_1266),))
    conn.commit()
    print("committed: id 1266")


if __name__ == "__main__":
    main()
