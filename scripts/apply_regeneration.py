#!/usr/bin/env python3
"""Apply gate-passed regenerated explanations to the real bank.

Only rows the independent judge marked CLEAN are written. Everything else stays as
it was and comes to hand review. A backup is taken first, and a full before/after
record is written for the audit trail.

    python3 scripts/apply_regeneration.py            # dry run
    python3 scripts/apply_regeneration.py --apply
"""
import argparse
import glob
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path("/home/papichulo/sabal/data/fcle.db")
W = Path("/home/papichulo/.hermes/workspace/sabal-sweep")
BACKUP_DIR = Path("/home/papichulo/.hermes/cache/scratch/sabal-audit")


def load():
    gen = {}
    for line in (W / "gen-all.jsonl").open():
        r = json.loads(line)
        if r.get("ok"):
            gen[r["id"]] = r
    gate = {}
    for f in glob.glob(str(W / "gate*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            gate[r["id"]] = r
    return gen, gate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    gen, gate = load()
    clean = [i for i in gen if gate.get(i, {}).get("verdict") == "CLEAN"]
    held = sorted(i for i in gen if i not in clean)
    print("generated: %d | gate CLEAN: %d | held for hand review: %d %s"
          % (len(gen), len(clean), len(held), held))

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    present = [i for i in clean if conn.execute("SELECT 1 FROM questions WHERE id=?", (i,)).fetchone()]

    if not args.apply:
        print("would update %d rows; dry run, pass --apply" % len(present))
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = BACKUP_DIR / ("fcle.db.bak-%s" % ts)
    shutil.copyfile(DB, backup)
    print("backup: %s" % backup)

    record = W / ("applied-%s.jsonl" % ts)
    rec_f = record.open("w")
    changed = 0
    for qid in present:
        row = conn.execute("SELECT explanation, wrong_explanations FROM questions WHERE id=?",
                           (qid,)).fetchone()
        before = {"explanation": row["explanation"],
                  "wrong_explanations": json.loads(row["wrong_explanations"] or "[]")}
        after = gen[qid]["after"]
        conn.execute("UPDATE questions SET explanation=?, wrong_explanations=? WHERE id=?",
                     (after["explanation"], json.dumps(after["wrong_explanations"]), qid))
        rec_f.write(json.dumps({"id": qid, "judge": gate[qid].get("judge"),
                                "before": before, "after": after}) + "\n")
        changed += 1
    conn.commit()
    rec_f.close()
    print("updated %d rows" % changed)
    print("record: %s" % record)

    print("\nheld rows, unchanged and awaiting hand repair: %s" % held)


if __name__ == "__main__":
    main()
