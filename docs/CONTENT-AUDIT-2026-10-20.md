# Content audit: detached explanation rebuttals

**Date:** 2026-10-20 · **Scope:** all 2,350 questions in `data/fcle.db`
**Trigger:** rendering question 1365 on the new public practice page. Its explanation argued
against a Tenth Amendment school-funding scenario, a failure to exhaust administrative remedies,
and a Bible-oath Establishment Clause scenario. Its four options contain none of those things.

## The defect family

An explanation is assembled against a *different distractor set* from the one the question
actually ships. The stem and the key are usually fine, and the per-option `wrong_explanations`
are usually fine; the damage is in `explanation`, which rebuts options nobody can see. A student
reads a confident paragraph about a scenario that is not on the screen, which is worse than no
explanation, because it teaches the wrong contrast.

## Method, and what each stage was worth

| Stage | Rows flagged | Verdict |
|---|---|---|
| `detect_mismatched_explanations.py` (keyword overlap, in-repo) | 1 (id 2260, an unrelated overlap artefact) | too blunt to see this class |
| Named-entity scan: instruments in the explanation absent from the options | 636, then 229 after normalising articles | **almost entirely legitimate**: explanations routinely name the doctrine the question tests without naming it in the options ("violated the Equal Protection Clause") |
| Two-sided claim mapping (unmatched rebuttals vs unrebutted options) | 79 | still mostly false positives; legal vocabulary overlaps too heavily |
| **Decisive rules**: more rebuttals than the 3 possible distractors, OR an instrument named inside a rebuttal that no option mentions | **8** | every one read by hand |

The lesson worth keeping: **lexical similarity cannot separate a wrong rebuttal from a right one
in this corpus.** Both quote statutes, clauses and case names, and the real options share most of
their vocabulary with the phantom ones. The reliable instrument is a semantic judge, not a regex.

## Confirmed and repaired

| id | Defect | Repair |
|---|---|---|
| **1365** | three rebuttals, none of which match its options (Tenth Amendment funding, exhaustion of remedies, Bible oath) | kept the correct-answer rationale; dropped all three (1,682 → 491 chars) |
| **2136** | a fourth rebuttal ("intermediate scrutiny but incorrectly states the burden") for a distractor the question does not contain | dropped that sentence; the three real rebuttals remain (2,448 → 2,132) |
| **1087** | two of three rebuttals address non-existent options (First Amendment censorship, separation of powers) | kept the rationale and the majority-rule rebuttal (1,653 → 834) |
| **1969** | one garbled rebuttal referencing *Brown* and *Barnette*, plus three `wrong_explanations` about school speech, none of which are its options | explanation rewritten against its actual options (bad tendency, Commerce Clause, hard power) and all three wrong-explanations rewritten to match |

`1969`'s replacement text was written by Ann-E on 2026-10-20 and is flagged for Mister K's review
like any other authored item.

## Reviewed and deliberately left alone

| id | Why |
|---|---|
| **2055** | the rebuttal rebuts Helvering v. Davis, which *is* one of its options. The General Welfare Clause is context, not a phantom. |
| **2138** | the rebuttal restates that the keyed answer is correct. Redundant, not wrong. |
| **150, 1425** | the rebuttal text is loose but does argue against a real option. |

## Verification

- The decisive-signal scan now returns no unexplained rows: the residual hits are 2055 (legitimate),
  2138 (redundant), 150 and 1425 (reviewed).
- Backup taken before any write: `~/.hermes/cache/scratch/sabal-audit/fcle.db.bak-20261020T131737Z`
  (plus the earlier `…131727Z`).
- The repair is a named script, not an ad-hoc edit:
  `scripts/fix_20261020_explanation_mismatches.py` (idempotent, `--apply` writes, dry-run by default).
- Broad auditors kept for future use: `scripts/audit_detached_explanations.py`,
  `scripts/audit_excess_rebuttals.py`.

## Exhaustive sweep, same day

The targeted pass above could not measure the class, so a semantic sweep followed.

| Stage | Result |
|---|---|
| Questions judged by Qwen3.5-9B, one narrow question each | 2,350, zero parse failures |
| Flagged | **413 (17.6%)**, spread 15-21% across all four domains |
| Random 60 re-judged by gemma-4-12b | 72% agreement, so roughly 300 real |
| Regenerated against their own four options | 413 of 413 |
| Independent gate (gemma-4-12b re-judge) | **396 CLEAN, 17 held** |
| Applied to the bank | 396 rows, backup `fcle.db.bak-20261020T195641Z` |

Regeneration, not sentence deletion, because sentence-level patching provably failed: a
mechanical proposal covering only 41 of 413 rows wanted to delete legitimate rebuttals
(136, 267, 278). Prose written with the four options in view is the honest repair.

The 17 held rows were not written to the bank. They carry a mix of judge noise and real
generation faults, including one invented case name, "Tinker v. Delaware". A prompt rule
does not enforce anything, so the generator now rejects any output naming a case, statute
or amendment that is absent from the row, and retries.

Two operational defects were found and fixed while running this:
- output overran `max_tokens` and truncated mid-JSON (112 rows in one pass);
- the model returns `finish_reason: stop` while omitting the final closing brace, which
  discarded complete, valid answers. Brace repair recovered about 50 rows per pass, with
  a punctuation check so a genuinely cut sentence is still refused.

Scripts: `sweep_explanations.py`, `regenerate_explanations.py`, `verify_regeneration.py`,
`apply_regeneration.py`, `propose_explanation_repairs.py` (the failed shortcut, kept as a
record).

## Residual risk, stated plainly

This was a targeted sweep, not an exhaustive one. Four rows are fixed because they carried a
decisive structural marker; rows where the phantom rebuttal happens to share vocabulary with a real
option would not be caught this way. A complete pass needs a model judge over all 2,350 rows, the
shape the September audit used (2,350 rows through a local model, results in `~/fcle_audit/`). That
is hours of GPU time, not minutes, and it should be run before the next directory submission rather
than claimed as done.

The new public practice page also makes this class visible to students for the first time, and its
"something wrong with this question" route now accepts anonymous reports. That is the durable fix:
the bank gets read by the people who will notice.
