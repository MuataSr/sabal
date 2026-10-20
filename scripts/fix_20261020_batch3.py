#!/usr/bin/env python3
"""Batch 3: stem/key conflicts, found by the Class-3 rule from the 2026-10-20 audit.

The rule, agreed 2026-10-20:
  * a stem may speak of "a violation of a student's rights"; it may NOT speak of
    "a violation of the First Amendment" when the keyed answer is the protected
    expression, because that teaches the rule backwards
  * REWRITE the stem when the options support exactly one defensible key
  * RETIRE when no honest stem gives a single key, because the options are split
    between protected and restrictable choices

Applied here:

  2138  REWRITE. Options: black armbands (the Tinker fact pattern), red armbands,
        non-offensive graphic shirt, non-disruptive slogan hat. Under "most closely
        matches the expression the Court protected", A is uniquely best. Key and
        options untouched.

  1954  RETIRE. Its own feedback says the quiet part out loud: "which action the
        court would rule as a First Amendment violation, meaning which student
        action is protected". A (armbands) and B (pro-war button) are both
        protected; C (hate-speech flyers) and D (obscene drawing) are both
        restrictable. Whichever way the stem is read, two options fit. No rewrite
        can rescue it, so it moves to `questions_retired` with its reason rather
        than being deleted.

    python3 scripts/fix_20261020_batch3.py            # dry run, prints the diff
    python3 scripts/fix_20261020_batch3.py --apply    # writes, with a backup
"""
import argparse
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path("/home/papichulo/sabal/data/fcle.db")
BACKUP_DIR = Path("/home/papichulo/.hermes/cache/scratch/sabal-audit")

STEM_2138_OLD = ("Consider the principle of the Equal Protection Clause as applied in "
                 "*Tinker v. Des Moines Independent Community School District*. Which of the "
                 "following student actions would a court MOST likely determine is a violation "
                 "of the First Amendment rights protected by this principle, assuming the "
                 "context of a school setting?")

STEM_2138_NEW = ("Consider the First Amendment principle applied in *Tinker v. Des Moines "
                 "Independent Community School District* (1969). Which of the following student "
                 "actions most closely matches the expression the Court held to be protected?")

SENT_2138_OLD = ("The claim that wearing black armbands to express silent opposition to the "
                 "Vietnam War without disrupting classwork is correct because it describes the "
                 "exact factual scenario from the case that was found to be a violation of "
                 "First Amendment rights despite occurring in a school.")

SENT_2138_NEW = ("Wearing black armbands to express silent opposition to the Vietnam War "
                 "without disrupting classwork is the exact factual scenario in the case, where "
                 "the Court held the expression was protected by the First Amendment even inside "
                 "a school.")

RETIRE_1954_REASON = ("Stem asked which action was a violation of the First Amendment while the "
                      "key was the protected expression; options split two protected (A, B) and "
                      "two restrictable (C, D), so no stem yields a single defensible key. "
                      "Retired 2026-10-20 by the Class-3 rule.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    row = conn.execute("SELECT question, explanation FROM questions WHERE id=2138").fetchone()
    stem_ok = row["question"].strip() == STEM_2138_OLD.strip()
    sent_ok = SENT_2138_OLD in row["explanation"]
    print("2138 stem matches expected text:", stem_ok)
    print("2138 sentence found:", sent_ok)

    base = conn.execute("SELECT COUNT(*) FROM questions WHERE id=1954").fetchone()[0]
    print("1954 present in bank:", bool(base))

    if not args.apply:
        print("\n--- 2138 new stem ---\n" + STEM_2138_NEW)
        print("\n--- 2138 new sentence ---\n" + SENT_2138_NEW)
        print("\n--- 1954 ---\nretire: " + RETIRE_1954_REASON)
        print("\ndry run; pass --apply")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / ("fcle.db.bak-%s" % datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    shutil.copyfile(DB, backup)
    print("\nbackup: %s" % backup)

    if stem_ok and sent_ok:
        conn.execute("UPDATE questions SET question=?, explanation=? WHERE id=2138",
                     (STEM_2138_NEW, row["explanation"].replace(SENT_2138_OLD, SENT_2138_NEW)))
        print("2138: stem and sentence rewritten")
    else:
        print("2138: SKIPPED, text did not match the expected original")

    if base:
        conn.execute("""CREATE TABLE IF NOT EXISTS questions_retired (
                          id INTEGER PRIMARY KEY,
                          payload TEXT NOT NULL,
                          reason TEXT NOT NULL,
                          retired_at TEXT NOT NULL
                        )""")
        full = conn.execute("SELECT * FROM questions WHERE id=1954").fetchone()
        payload = json.dumps({k: full[k] for k in full.keys()})
        conn.execute("INSERT OR REPLACE INTO questions_retired (id, payload, reason, retired_at) "
                     "VALUES (?, ?, ?, ?)",
                     (1954, payload, RETIRE_1954_REASON,
                      datetime.now(timezone.utc).isoformat(timespec="seconds")))
        conn.execute("DELETE FROM questions WHERE id=1954")
        print("1954: moved to questions_retired")

    conn.commit()
    print("\ncommitted")


if __name__ == "__main__":
    main()
