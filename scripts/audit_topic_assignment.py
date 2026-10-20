#!/usr/bin/env python3
"""Keyword overlap between `topic` and row text. MEASURED ON 2026-10-20: NOT A VALIDITY TEST.

Verdict from running it: useless as a mislabel detector. It flags 786 rows at one
threshold and 1,268 at a stricter one, because the topic vocabulary is abstract and
seldom appears in the row ("Popular sovereignty" questions rarely say "sovereignty").
A high flag rate here is an artefact of the label style, not evidence of bad labels.

What IS certain, from reading the examples: rows are mislabelled in ways no keyword
test can size. A Literary Digest polling question carried "Interest groups and
lobbying"; a coattail-effect question and a C. Wright Mills elite-theory question
both carried "Federalism basics". Topic feeds per-topic mastery, the dashboard's weak
-topic list and the diagnostic results page, so a wrong label tells a student they are
weak in the wrong subject.

Use a semantic pass to measure this, not this script. Kept only so the next person
does not rebuild it and draw the same false conclusion.

Original intent follows.

---

Surfaced on 2026-10-20 while scanning for stem/key conflicts: rows about soft
power, House and Senate terms, and Truman's desegregation order all carried the
topic label "Tinker v Des Moines". The practice pages show the topic to students,
so a wrong label points a student at the wrong mental shelf.

Read-only. Heuristic, on purpose simple: take the distinctive words of the topic
(len >= 4, not stop words, not the case-style connectors) and check whether ANY of
them appears anywhere in the row's own text (stem, options, explanation, feedback).
Zero overlap is a review candidate, not a verdict: an abstract topic such as
"Citizen participation" can legitimately fail a keyword test because the row never
uses that phrase.

    python3 scripts/audit_topic_assignment.py
    python3 scripts/audit_topic_assignment.py --limit 40
"""
import argparse
import collections
import json
import re
import sqlite3

DB = "data/fcle.db"
STOP = set("""the of and for with from into about that this these those which what when where
who whom whose how why not are was were has have had does did can could should would will
case cases court supreme united states amendment clause act doctrine law rights right
political politics government federal state states national American America""".split())


def words(text):
    return {w for w in re.findall(r"[a-z]{4,}", (text or "").lower()) if w not in STOP}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM questions ORDER BY id").fetchall()

    by_topic = collections.Counter(r["topic"] for r in rows)
    print("distinct topics: %d" % len(by_topic))
    print("largest topics: %s\n" % by_topic.most_common(5))

    flagged = []
    for r in rows:
        topic_words = words(r["topic"])
        if not topic_words:
            continue
        body = " ".join(str(r[k] or "") for k in
                        ("question", "correct_answer", "wrong_answers", "explanation",
                         "wrong_explanations", "stimulus"))
        if not (topic_words & words(body)):
            flagged.append((r["id"], r["topic"], (r["question"] or "")[:90].replace("\n", " ")))

    print("rows whose topic shares no distinctive word with their own text: %d / %d (%.1f%%)"
          % (len(flagged), len(rows), 100.0 * len(flagged) / max(len(rows), 1)))
    print("(review candidates, not verdicts)\n")
    for qid, topic, q in flagged[:args.limit]:
        print("  id %-5d topic=%-28s %s" % (qid, topic[:28], q))
    if len(flagged) > args.limit:
        print("  ... %d more" % (len(flagged) - args.limit))


if __name__ == "__main__":
    main()
