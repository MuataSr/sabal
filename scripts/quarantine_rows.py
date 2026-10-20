#!/usr/bin/env python3
"""Move structurally defective rows out of the served bank, payload intact.

Same pattern as retirement: the payload is archived rather than edited away, so the row
can be repaired and reinserted with its id intact. Deleting is chosen over an `active`
column on purpose: a row that is absent cannot be served, while a filter that someone
forgets to add can.

    python3 scripts/quarantine_rows.py --reasons FILE.json     # dry run
    python3 scripts/quarantine_rows.py --reasons FILE.json --apply

FILE.json is {"<id>": "<reason>", ...}.
"""
import argparse
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path("/home/papichulo/sabal/data/fcle.db")
BACKUP_DIR = Path("/home/papichulo/.hermes/cache/scratch/sabal-audit")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reasons", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    reasons = {int(k): v for k, v in json.load(open(args.reasons)).items()}
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    present = [i for i in reasons
               if conn.execute("SELECT 1 FROM questions WHERE id=?", (i,)).fetchone()]
    print("requested: %d | present in the bank: %d | already gone: %d"
          % (len(reasons), len(present), len(reasons) - len(present)))
    if not args.apply:
        print("dry run; pass --apply")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = BACKUP_DIR / ("fcle.db.bak-%s" % ts)
    shutil.copyfile(DB, backup)
    print("backup: %s" % backup)

    conn.execute("""CREATE TABLE IF NOT EXISTS questions_quarantine (
        id INTEGER PRIMARY KEY,
        payload TEXT NOT NULL,
        reason TEXT NOT NULL,
        quarantined_at TEXT NOT NULL)""")

    now = datetime.now(timezone.utc).isoformat()
    moved = 0
    for qid in present:
        row = dict(conn.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone())
        conn.execute("INSERT OR REPLACE INTO questions_quarantine (id, payload, reason, quarantined_at)"
                     " VALUES (?,?,?,?)", (qid, json.dumps(row), reasons[qid], now))
        conn.execute("DELETE FROM questions WHERE id=?", (qid,))
        moved += 1
    conn.commit()

    left = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    quar = conn.execute("SELECT COUNT(*) FROM questions_quarantine").fetchone()[0]
    print("quarantined this run: %d" % moved)
    print("bank now: %d | quarantine table: %d" % (left, quar))


if __name__ == "__main__":
    main()
