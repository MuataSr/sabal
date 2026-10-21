#!/usr/bin/env python3
"""Build the gate's regression fixtures from evidence we already have.

known_bad  : every row quarantined on 2026-10-20/21, payload intact, tagged with
             whether the deterministic rules should catch it or whether it needs the
             semantic stage. The rules subset must be rejected 100%.
verified   : rows read by hand and confirmed sound. Must be accepted 100%.
candidates : rows that passed both 2026-10-20 gates. Used as a recall check on live
             content, asserted at a threshold rather than absolutely.

    python3 scripts/build_gate_fixtures.py
"""
import json
import os
import sqlite3

DB = "/home/papichulo/sabal/data/fcle.db"
OUT = "/home/papichulo/sabal/tests/fixtures/gate"
APPLIED = "/home/papichulo/.hermes/workspace/sabal-sweep/applied-20261020T195641Z.jsonl"
VERIFIED_IDS = [1000, 2256, 962]
RULE_REASONS = ("near-duplicate", "malformed", "no text is present", "option text")
FIELDS = ("fcle_domain", "topic", "difficulty", "question", "correct_answer",
          "wrong_answers", "explanation", "stimulus", "wrong_explanations")


def item_of(row):
    return {k: row.get(k) for k in FIELDS}


def main():
    os.makedirs(OUT, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    known = []
    for r in conn.execute("SELECT payload, reason FROM questions_quarantine"):
        payload = json.loads(r["payload"])
        known.append({"id": payload["id"], "reason": r["reason"],
                      "detectable_by": "rules" if any(
                          k in r["reason"] for k in RULE_REASONS) else "semantic",
                      "item": item_of(payload)})
    with open(os.path.join(OUT, "known_bad.json"), "w") as f:
        json.dump(known, f, indent=1)

    verified = []
    for qid in VERIFIED_IDS:
        row = conn.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()
        if row:
            verified.append({"id": qid, "item": item_of(dict(row))})
    with open(os.path.join(OUT, "verified.json"), "w") as f:
        json.dump(verified, f, indent=1)

    ids = [json.loads(line)["id"] for line in open(APPLIED)] if os.path.exists(APPLIED) else []
    cands = []
    for qid in ids:
        row = conn.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()
        if row:
            cands.append({"id": qid, "item": item_of(dict(row))})
    with open(os.path.join(OUT, "candidates.json"), "w") as f:
        json.dump(cands, f, indent=1)

    rules = sum(1 for k in known if k["detectable_by"] == "rules")
    print("fixtures in %s" % OUT)
    print("  known_bad: %d (%d rules-detectable, %d semantic)"
          % (len(known), rules, len(known) - rules))
    print("  verified : %d" % len(verified))
    print("  candidates: %d" % len(cands))


if __name__ == "__main__":
    main()
