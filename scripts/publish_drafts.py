#!/usr/bin/env python3
"""The only path from a draft item into the served bank.

Generation writes to `questions_draft`. This publisher gates each draft with
scripts/qc_item.py and only then inserts it into `questions`, recording provenance in
`question_provenance` (which model produced it, which prompt version, which gate version
accepted it). A blocked draft stays in the queue with its reasons attached, so the human
review sees exactly what the rules objected to.

    python3 scripts/publish_drafts.py            # dry run: gate and report
    python3 scripts/publish_drafts.py --apply    # insert the passing drafts
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qc_item  # noqa: E402

DB = "/home/papichulo/sabal/data/fcle.db"
DRAFT_DDL = """CREATE TABLE IF NOT EXISTS questions_draft (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payload TEXT NOT NULL,
    gen_model TEXT,
    prompt_ver TEXT,
    created_at TEXT,
    gate_status TEXT DEFAULT 'pending',
    gate_notes TEXT
)"""
PROV_DDL = """CREATE TABLE IF NOT EXISTS question_provenance (
    question_id INTEGER PRIMARY KEY,
    source_draft_id INTEGER,
    gen_model TEXT,
    prompt_ver TEXT,
    gate_ver TEXT,
    gated_at TEXT
)"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    conn.execute(DRAFT_DDL)
    conn.execute(PROV_DDL)
    conn.commit()

    stems, counts = qc_item.bank_context(conn)
    q = "SELECT * FROM questions_draft WHERE gate_status IN ('pending','blocked')"
    if args.limit:
        q += " LIMIT %d" % args.limit
    drafts = [dict(r) for r in conn.execute(q)]
    print("%d draft(s) in the queue" % len(drafts))

    passed = blocked = 0
    for d in drafts:
        item = json.loads(d["payload"])
        item["wrong_answers"] = json.dumps(item.get("wrong_answers") or [])
        res = qc_item.gate(item, existing_stems=stems, entity_counts=counts)
        notes = "; ".join(res["violations"] + ["warn: " + w for w in res["warnings"]])[:800]
        if res["passed"]:
            passed += 1
            print("  PASS  draft %-4d %s" % (d["id"], (item.get("question") or "")[:70]))
            if args.apply:
                cur = conn.execute(
                    """INSERT INTO questions
                       (fcle_domain, topic, difficulty, question, correct_answer,
                        wrong_answers, explanation, stimulus, wrong_explanations)
                       VALUES (?,?,?,?,?,?,?,?,?)""",
                    (item.get("fcle_domain"), item.get("topic"), item.get("difficulty"),
                     item.get("question"), item.get("correct_answer"),
                     item["wrong_answers"], item.get("explanation"),
                     item.get("stimulus") or "",
                     json.dumps(item.get("wrong_explanations") or [])))
                new_id = cur.lastrowid
                conn.execute(
                    "INSERT OR REPLACE INTO question_provenance "
                    "(question_id, source_draft_id, gen_model, prompt_ver, gate_ver, gated_at)"
                    " VALUES (?,?,?,?,?,?)",
                    (new_id, d["id"], d.get("gen_model"), d.get("prompt_ver"),
                     res["rules_version"], datetime.now(timezone.utc).isoformat()))
                conn.execute("DELETE FROM questions_draft WHERE id=?", (d["id"],))
                stems.append(item.get("question") or "")
        else:
            blocked += 1
            print("  BLOCK draft %-4d %s" % (d["id"], "; ".join(res["violations"])[:90]))
            if args.apply:
                conn.execute("UPDATE questions_draft SET gate_status='blocked', gate_notes=?"
                             " WHERE id=?", (notes, d["id"]))
        conn.commit()

    print("\n%d passed, %d blocked%s" % (passed, blocked,
                                         "" if args.apply else " (dry run; pass --apply)"))
    return 0 if blocked == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
