#!/usr/bin/env python3
"""Apply a regeneration JSONL to a throwaway copy of the bank, then re-judge it.

Nothing here touches data/fcle.db. The point is to answer one question before any
real edit: does the regenerated prose pass the same audit that condemned the original?

    python3 scripts/verify_regeneration.py --pilot pilot20.jsonl
prints the copy path and writes <pilot>.ids.jsonl for the sweep to re-judge.
"""
import argparse
import json
import shutil
import sqlite3
from pathlib import Path

DB = Path("/home/papichulo/sabal/data/fcle.db")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", required=True)
    ap.add_argument("--out-db", default=None)
    args = ap.parse_args()

    pilot = Path(args.pilot)
    out_db = Path(args.out_db or str(pilot).replace(".jsonl", ".db"))
    ids_path = Path(str(pilot).replace(".jsonl", ".ids.jsonl"))

    recs = [json.loads(l) for l in pilot.open() if l.strip()]
    ok = [r for r in recs if r.get("ok") and "after" in r]
    print("pilot rows: %d, generated ok: %d, failed: %d" % (len(recs), len(ok), len(recs) - len(ok)))

    shutil.copyfile(DB, out_db)
    conn = sqlite3.connect(out_db)
    applied = 0
    for r in ok:
        cur = conn.execute("UPDATE questions SET explanation=?, wrong_explanations=? WHERE id=?",
                           (r["after"]["explanation"], json.dumps(r["after"]["wrong_explanations"]),
                            r["id"]))
        applied += cur.rowcount
    conn.commit()
    print("applied to throwaway copy %s: %d rows" % (out_db, applied))

    with ids_path.open("w") as f:
        for r in ok:
            f.write(json.dumps({"id": r["id"], "verdict": "FLAG"}) + "\n")
    print("ids for re-judge: %s (%d)" % (ids_path, len(ok)))


if __name__ == "__main__":
    main()
