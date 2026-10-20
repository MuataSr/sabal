#!/usr/bin/env python3
"""One-off, explicit repairs for the four confirmed explanation defects (2026-10-20).

Found by rendering question 1365 on the new public practice page: its explanation
argued against three distractors that are not its options. A bank-wide sweep
followed. Lexical heuristics flagged 8 candidates; each was read against its own
options, and four were confirmed defects of the same family — prose assembled
against a different distractor set:

  1087  two of its three rebuttals address options that do not exist
        (First Amendment censorship, separation of powers); the third is real.
  1365  all three rebuttals address options that do not exist
        (Tenth Amendment school funding, exhaustion of remedies, Bible oath).
  1969  one garbled rebuttal referencing *Brown* and *Barnette*, and three
        wrong_explanations about school speech, none of which are its options.
  2136  a fourth rebuttal, "intermediate scrutiny but incorrectly states the
        burden", for a distractor the question does not contain.

Reviewed and deliberately NOT changed:
  2055  the rebuttal rebuts Helvering v. Davis, which IS one of its options.
  2138  the rebuttal restates that the keyed answer is correct; redundant, not wrong.
  150, 1425  rebuttal text is loose but does argue against a real option.

This script is an explicit record, not a heuristic: each edit names its row and
the exact surgical change. Re-running it is a no-op because every operation is
idempotent (it checks the current text first).

    python3 scripts/fix_20261020_explanation_mismatches.py --apply
"""
import argparse
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path("/home/papichulo/sabal/data/fcle.db")
BACKUP_DIR = Path("/home/papichulo/.hermes/cache/scratch/sabal-audit")

REWRITE_1969 = (
    "The Court in *Schenck* applied the 'clear and present danger' test: speech could be punished "
    "when it created a clear and present danger of bringing about the substantive evils Congress has "
    "a right to prevent. The case does not support a 'bad tendency' test that punishes speech merely "
    "because it might eventually lead to harm; it did not rest on Congress's Commerce Clause power "
    "over interstate distribution; and it did not describe a 'hard power' doctrine. The prosecution "
    "rested on the Espionage Act and the wartime draft."
)

WRONG_1969 = (
    '["A student might pick this by recalling the older bad-tendency approach, but *Schenck* '
    'announced the clear and present danger test; the bad-tendency test is associated with later '
    'cases rather than with this holding.", '
    '"A student might pick this because Congress often regulates interstate distribution under the '
    'Commerce Clause, but the *Schenck* prosecution rested on the Espionage Act and the wartime '
    'draft, not on the commerce power.", '
    '"A student might pick this by borrowing hard-power and soft-power vocabulary from foreign '
    'policy, but those terms describe instruments of national power; *Schenck* concerns the First '
    'Amendment standard for punishable speech."]'
)

EDITS = {
    1087: "drop_rebuttal_sentences:First Amendment by granting private donors,"
          "The assertion that this demonstrates a failure of the separation of powers",
    1365: "truncate_before:The claim that",
    2136: "drop_rebuttal_sentences:The claim that the court should apply intermediate scrutiny "
          "but incorrectly states the burden",
    1969: "replace_both",
}


def apply_edit(conn, qid, mode):
    row = conn.execute("SELECT explanation, wrong_explanations FROM questions WHERE id=?",
                       (qid,)).fetchone()
    ex, wxs = row
    original = (ex, wxs)

    if mode.startswith("truncate_before:"):
        marker = mode.split(":", 1)[1]
        if marker not in ex:
            print("   id %d: already clean" % qid)
            return False
        ex = ex.split(marker)[0].rstrip()

    elif mode.startswith("drop_rebuttal_sentences:"):
        # drop any sentence that CONTAINS one of the named fragments
        fragments = [f.strip() for f in mode.split(":", 1)[1].split(",") if f.strip()]
        parts = ex.split(". ")
        kept = [p for p in parts if not any(f in p for f in fragments)]
        ex = ". ".join(kept).strip()
        if not ex.endswith("."):
            ex += "."

    elif mode == "replace_both":
        ex, wxs = REWRITE_1969, WRONG_1969

    if (ex, wxs) == original:
        print("   id %d: no change" % qid)
        return False
    conn.execute("UPDATE questions SET explanation=?, wrong_explanations=? WHERE id=?",
                 (ex, wxs, qid))
    print("   id %d: %d -> %d chars in explanation" % (qid, len(original[0]), len(ex)))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not args.apply:
        print("dry run; pass --apply. Rows: %s" % sorted(EDITS))
        for qid, mode in sorted(EDITS.items()):
            print("   %d  %s" % (qid, mode[:80]))
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / ("fcle.db.bak-%s" % datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    shutil.copyfile(DB, backup)
    print("backup: %s" % backup)

    conn = sqlite3.connect(DB)
    changed = 0
    for qid, mode in sorted(EDITS.items()):
        if apply_edit(conn, qid, mode):
            changed += 1
    conn.commit()
    print("\n%d row(s) changed" % changed)


if __name__ == "__main__":
    main()
