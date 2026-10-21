#!/usr/bin/env python3
"""Gate for a single question item: the only door into the bank.

Why this exists: the 2026-10 audit found 248 structurally broken rows in a bank
that had already been generated, inserted and served. Every one of those defects
was introduced at insert time and discovered afterwards. This module runs at insert
time, fails closed, and is testable against every defect we have already found.

Severity model:
  - violations (ERROR) block the item. They are structural or provably wrong.
  - warnings are recorded for the human queue. They are judgement calls: an
    explanation that never engages its distractors, a key that is much longer than
    the others, an entity that appears nowhere else in the bank.

Deliberately NOT a hard rule: naming a case, statute or amendment the stem does not
mention. Options legitimately introduce cases. A judge, not a regex, settles meaning;
the regex only routes suspicious entities to that judge.

CLI:
    python3 scripts/qc_item.py --id 1234          # gate one live row
    python3 scripts/qc_item.py --draft            # gate everything in questions_draft
"""
from __future__ import annotations

import argparse
import collections
import difflib
import json
import re
import sqlite3
import sys

DB_PATH = "/home/papichulo/sabal/data/fcle.db"
RULES_VERSION = "qc-1"

CITES_TEXT = re.compile(
    r"(according to the (text|passage|excerpt|reference|references|stimulus|article|provided)"
    r"|based on the (text|excerpt|stimulus|reference|references|provided)"
    r"|in the (excerpt|passage) (above|below)|the following excerpt)", re.I)
BAKED_LETTER = re.compile(r"^\s*[A-D][\).]\s")
META_OPTION = re.compile(
    r"(this (option|distractor|choice|answer) (is|would be|incorrectly)"
    r"|^\s*this is (incorrect|wrong|correct) because"
    r"|^\s*(option )?[A-D]\b[^.]{0,40}\bis incorrect\b)", re.I)
# A whole option set written as mini-explanations: two or more options that both judge
# and justify ("is incorrect because...", "the argument fails because..."). One such
# option can be a legitimate answer; a set of them is commentary where answers belong.
EXPLAINER = re.compile(
    r"\b(incorrect|correct|wrong|flawed|fails?|false|true|valid|invalid)\b[^.]{0,60}\bbecause\b"
    r"|\bbecause\b[^.]{0,60}\b(incorrect|flawed|fails?)\b", re.I)
TEMPLATE_OPEN = re.compile(r"^\s*the claim that\b", re.I)
NAMES_OTHER_KEY = re.compile(
    r"(?:option\s+)?\b([B-D])\b\s+(?:is|as|would be)\s+(?:the\s+)?correct"
    r"|making\s+([B-D])\s+correct"
    r"|correct answer is\s+([B-D])\b", re.I)
ENTITY = re.compile(
    r"\b(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth"
    r"|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth"
    r"|Twenty-First|Twenty-Second|Twenty-Third|Twenty-Fourth|Twenty-Fifth|Twenty-Sixth"
    r"|Twenty-Seventh)\s+Amendment\b"
    r"|\b[A-Z][a-zA-Z]+\s+v\.?\s+[A-Z][a-zA-Z]+\b"
    r"|\b[A-Z][a-zA-Z]+\s+(?:Clause|Act)\b")

MAX_EXPLANATION_WORDS = 90
MIN_EXPLANATION_WORDS = 25
MAX_RATIONALE_WORDS = 40
OPTION_SIMILARITY_MAX = 0.75
STEM_OVERLAP_MAX = 0.88
MIN_STIMULUS_CHARS = 120


def as_list(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value]
    if value is None:
        return []
    s = str(value).strip()
    if not s:
        return []
    try:
        j = json.loads(s)
        if isinstance(j, list):
            return [str(x).strip() for x in j]
    except Exception:
        pass
    return [s]


def norm(text):
    return " ".join((text or "").lower().split())


def words(text):
    return len((text or "").split())


def shingles(text, n=5):
    toks = re.findall(r"[a-z0-9]+", (text or "").lower())
    if len(toks) < n:
        return {" ".join(toks)} if toks else set()
    return {" ".join(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def entities(text):
    return {m.group(0).strip() for m in ENTITY.finditer(text or "")}


def gate(item, existing_stems=None, entity_counts=None):
    """Return {"passed": bool, "violations": [...], "warnings": [...], "checks": int}.

    item keys: question, correct_answer, wrong_answers, explanation, stimulus,
               wrong_explanations, fcle_domain, difficulty, topic
    existing_stems: iterable of stems already in the bank (duplicate detection)
    entity_counts: Counter of entities across the bank (singleton detection)
    """
    v, w = [], []
    checks = 0

    def check(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            v.append(msg)

    question = (item.get("question") or "").strip()
    key = (item.get("correct_answer") or "").strip()
    wrongs = as_list(item.get("wrong_answers"))
    explanation = (item.get("explanation") or "").strip()
    stimulus = (item.get("stimulus") or "").strip()
    rationales = as_list(item.get("wrong_explanations"))

    # 1. required fields
    check(len(question) >= 15, "stem missing or too short")
    check(bool(key), "no keyed answer")
    check(len(wrongs) == 3, "exactly three distractors required, got %d" % len(wrongs))
    check(bool(explanation), "no explanation")

    # 2. options present and non-empty
    options = [key] + wrongs
    check(all(len(o) >= 2 for o in options), "an option is empty or one character")
    checks += 1

    # 3. the key must be a real option and must not be repeated among the distractors
    key_hits = [o for o in options if norm(o) == norm(key)]
    check(len(key_hits) == 1, "key is duplicated among the distractors")
    check(len({norm(o) for o in options}) == len(options),
          "two options are identical after normalisation")

    # 4. near-duplicate options
    worst = 0.0
    for i in range(len(options)):
        for j in range(i + 1, len(options)):
            worst = max(worst, difflib.SequenceMatcher(
                None, norm(options[i]), norm(options[j])).ratio())
    checks += 1
    if worst >= OPTION_SIMILARITY_MAX:
        v.append("options are near-duplicates (%.2f similarity)" % worst)

    # 5. option text must be answer text, not commentary or a lettered label
    explainer = 0
    for o in options:
        checks += 1
        if BAKED_LETTER.match(o):
            v.append("option text carries a baked-in letter: %r" % o[:40])
        elif META_OPTION.search(o):
            v.append("option text is a rebuttal, not an answer: %r" % o[:40])
        if EXPLAINER.search(o):
            explainer += 1
    checks += 1
    if explainer >= 2:
        w.append("%d options are written as evaluative arguments; verify the key is "
                 "defensible on its merits" % explainer)

    # 6. a stem that cites a text must carry that text
    if CITES_TEXT.search(question):
        checks += 1
        if len(stimulus) < MIN_STIMULUS_CHARS:
            v.append("stem cites a text but stimulus is missing or under %d characters"
                     % MIN_STIMULUS_CHARS)

    # 7. explanation must exist and be substantial; length is advisory above the floor.
    # A long explanation is not a defect (row 1000 is 232 words and correct). A very
    # short one usually means truncated output, which is a defect.
    checks += 1
    if words(explanation) < 15:
        v.append("explanation is %d words, too short to teach anything" % words(explanation))
    elif not explanation.rstrip().endswith((".", "?", "!", '"', "'")):
        v.append("explanation does not end a sentence (truncated output?)")
    elif words(explanation) < MIN_EXPLANATION_WORDS:
        w.append("explanation is %d words, brief" % words(explanation))
    elif words(explanation) > MAX_EXPLANATION_WORDS:
        w.append("explanation is %d words, above the %d-word guide"
                 % (words(explanation), MAX_EXPLANATION_WORDS))
    checks += 1
    if TEMPLATE_OPEN.match(explanation):
        v.append("explanation opens with the banned 'The claim that' frame")

    # 8. the explanation must not call a different option the correct one
    checks += 1
    m = NAMES_OTHER_KEY.search(explanation)
    if m:
        v.append("explanation names another option as correct (%r)"
                 % next(g for g in m.groups() if g))

    # 9. rationales, when present, must be short
    checks += 1
    absurd_r = [r for r in rationales if words(r) > 2 * MAX_RATIONALE_WORDS]
    if absurd_r:
        v.append("%d rationale(s) exceed %d words" % (len(absurd_r), 2 * MAX_RATIONALE_WORDS))
    long_r = [r for r in rationales if MAX_RATIONALE_WORDS < words(r) <= 2 * MAX_RATIONALE_WORDS]
    if long_r:
        w.append("%d rationale(s) run long (over %d words)"
                 % (len(long_r), MAX_RATIONALE_WORDS))

    # 10. duplicate stem against the existing bank. Callers that gate a row already in
    # the bank must pass stems with that row's own stem removed; a draft never is.
    # Sequence similarity, not shingle overlap: a one-word change in a 23-word stem
    # scores 0.58 on 5-grams but 0.97 here, and it is plainly the same item.
    if existing_stems:
        checks += 1
        target = norm(question)
        same = sum(1 for s in existing_stems if norm(s) == target)
        sh = shingles(question)
        best = 0.0
        for s in existing_stems:
            ns = norm(s)
            if ns == target:
                continue
            if jaccard(sh, shingles(s)) < 0.20:
                continue  # cheap prefilter; unrelated stems never reach difflib
            best = max(best, difflib.SequenceMatcher(None, target, ns).ratio())
            if best >= STEM_OVERLAP_MAX:
                break
        if same:
            v.append("an identical stem is already in the bank")
        elif best >= STEM_OVERLAP_MAX:
            v.append("near-duplicate of an existing stem (%.2f similarity)" % best)

    # ---- warnings: routed to a human, never silently dropped ----
    if len(rationales) and len(rationales) != len(wrongs):
        w.append("%d rationales for %d distractors" % (len(rationales), len(wrongs)))
    if explanation and wrongs:
        engaged = sum(1 for r in wrongs if len(set(re.findall(r"[a-z]{5,}", norm(r)))
                                             & set(re.findall(r"[a-z]{5,}", norm(explanation)))) >= 2)
        if engaged == 0:
            w.append("explanation does not appear to engage any distractor")
    longest = max(len(o) for o in options) if options else 0
    if longest and len(key) >= longest and len(key) > 1.4 * (sum(len(o) for o in options) / 4):
        w.append("key is much longer than the other options (length bias)")
    if entity_counts:
        stray = [e for e in entities(explanation) if entity_counts.get(e, 0) <= 1]
        if stray:
            w.append("entity named nowhere else in the bank: %s" % ", ".join(sorted(stray)[:3]))

    return {"passed": not v, "violations": v, "warnings": w, "checks": checks,
            "rules_version": RULES_VERSION}


def bank_context(conn):
    rows = conn.execute("SELECT question, explanation FROM questions").fetchall()
    counts = collections.Counter()
    for q, _ in rows:
        counts.update(entities(q))
    for _, e in rows:
        counts.update(entities(e))
    return [r[0] for r in rows], counts


def stems_excluding(stems, question):
    """Drop one copy of a row's own stem, for gating a row that is already in the bank."""
    out, dropped = [], False
    target = norm(question)
    for s in stems:
        if not dropped and norm(s) == target:
            dropped = True
            continue
        out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB_PATH)
    ap.add_argument("--id", type=int)
    ap.add_argument("--draft", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    stems, counts = bank_context(conn)

    if args.id:
        row = dict(conn.execute("SELECT * FROM questions WHERE id=?", (args.id,)).fetchone())
        res = gate(row, stems_excluding(stems, row["question"]), counts)
        print(json.dumps({"id": args.id, **res}, indent=2))
        return 0 if res["passed"] else 1

    if args.draft:
        try:
            drafts = [dict(r) for r in conn.execute("SELECT * FROM questions_draft")]
        except sqlite3.OperationalError:
            print("no questions_draft table yet")
            return 0
        failed = 0
        for d in drafts:
            res = gate(d, stems, counts)
            failed += 0 if res["passed"] else 1
            print("%-5s id=%-6s %s" % ("PASS" if res["passed"] else "BLOCK",
                                       d["id"], "; ".join(res["violations"])[:120]))
        print("\n%d drafts, %d blocked" % (len(drafts), failed))
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
