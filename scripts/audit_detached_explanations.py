#!/usr/bin/env python3
"""Find explanations that argue about content absent from the question they explain.

The defect this targets is specific and was found in the wild on 2026-10-20:
question 1365 (judicial activism) carried an explanation discussing a Tenth
Amendment state-sovereignty scenario, a failure to exhaust administrative
remedies, and a Bible-oath Establishment Clause scenario — none of which are
among that question's four options. The question and its key were coherent; the
prose had been assembled against a different distractor set.

`detect_mismatched_explanations.py` looks for the opposite shape: explanations
with NO keyword overlap. That misses a mixed explanation, which shares most of
its vocabulary with the question while carrying a paragraph about a scenario
nobody can see.

This is read-only. It extracts named entities from the explanation side
(amendments, case names, X Clause / X Act / X Doctrine) and reports any that
appear nowhere in the question, its options, its topic or its stimulus. A
contextual mention ("Marbury v. Madison established judicial review") is
legitimate, so the output is a review list, not a verdict.

Usage:
    python3 scripts/audit_detached_explanations.py            # summary + flagged rows
    python3 scripts/audit_detached_explanations.py --json     # machine-readable
    python3 scripts/audit_detached_explanations.py --id 1365  # one row in full
"""

import argparse
import json
import re
import sqlite3

DB_PATH = "data/fcle.db"

ORDINALS = ("First Second Third Fourth Fifth Sixth Seventh Eighth Ninth Tenth "
            "Eleventh Twelfth Thirteenth Fourteenth Fifteenth Sixteenth "
            "Seventeenth Eighteenth Nineteenth Twentieth Twenty-First "
            "Twenty-Second Twenty-Third Twenty-Fourth Twenty-Fifth "
            "Twenty-Sixth Twenty-Seventh").split()

ENTITY_PATTERNS = [
    re.compile(r"\b(?:%s)\s+Amendment\b" % "|".join(ORDINALS)),
    re.compile(r"\b[A-Z][a-zA-Z]+\s+v\.\s+[A-Z][a-zA-Z]+\b"),
    re.compile(r"\b(?:[A-Z][a-zA-Z-]+\s+){1,3}(?:Clause|Act|Doctrine|Amendment)\b"),
    re.compile(r"\b(?:[A-Z][a-zA-Z-]+\s+){2,3}(?:Court|Case)\b"),
]


def entities(text):
    found = set()
    for pat in ENTITY_PATTERNS:
        for m in pat.finditer(text or ""):
            found.add(re.sub(r"\s+", " ", m.group(0)).strip())
    return found


def audit_row(row):
    """Return the entities the explanation side uses that the question side never does."""
    question_side = " ".join(str(row[k] or "") for k in
                             ("question", "correct_answer", "wrong_answers", "topic", "stimulus"))
    explanation_side = " ".join(str(row[k] or "") for k in
                                ("explanation", "wrong_explanations"))
    known = {e.lower() for e in entities(question_side)}
    absent = sorted(e for e in entities(explanation_side) if e.lower() not in known)
    return absent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--id", type=int, default=None)
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if args.id:
        rows = conn.execute("SELECT * FROM questions WHERE id = ?", (args.id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM questions ORDER BY id").fetchall()

    flagged = []
    for row in rows:
        absent = audit_row(row)
        if absent:
            flagged.append({"id": row["id"], "domain": row["fcle_domain"],
                            "topic": row["topic"], "absent_entities": absent,
                            "question": (row["question"] or "")[:180]})

    checked = len(rows)
    if args.json:
        print(json.dumps({"checked": checked, "flagged": flagged}, indent=1))
        return

    print("checked %d questions, %d carry entities the question side never mentions"
          % (checked, len(flagged)))
    print("(a contextual mention is legitimate; this is a review list)\n")
    for f in flagged[:args.limit]:
        print("id %-5d [domain %s] %s" % (f["id"], f["domain"], f["absent_entities"]))
        print("        %s..." % f["question"].replace("\n", " ")[:150])
    if len(flagged) > args.limit:
        print("\n... %d more (use --limit or --json)" % (len(flagged) - args.limit))


if __name__ == "__main__":
    main()
