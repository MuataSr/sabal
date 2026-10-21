# The question pipeline

The bank that shipped on 2026-10-21 had 248 structurally broken rows and 413 detached
explanations, all inserted directly and discovered afterwards. This pipeline exists so the
next bank cannot do that. The gate is the only door.

## Flow

```
generate  ->  questions_draft  ->  publish_drafts.py  ->  questions  ->  served
                    |                    |
                    |                    +-- question_provenance (model, prompt, gate ver)
                    +-- blocked rows stay here with the reason attached
```

`scripts/generate_questions.py` no longer inserts into `questions`. It writes a JSON
payload into `questions_draft` stamped with `gen_model` and `prompt_ver`.

`scripts/publish_drafts.py` gates every queued row with `scripts/qc_item.py`. Passing rows
are inserted into `questions` and recorded in `question_provenance`. Failing rows stay in
the queue as `blocked` with their violations in `gate_notes`.

## Commands

```bash
python3 scripts/publish_drafts.py              # dry run: what would pass, what would not
python3 scripts/publish_drafts.py --apply      # publish the passing drafts
python3 scripts/qc_item.py --id 1234           # gate one live row
python3 scripts/qc_item.py --draft             # gate the whole queue, no writes
python3 scripts/build_gate_fixtures.py         # rebuild the regression fixtures
python3 -m pytest tests/test_question_gates.py tests/test_publish_drafts.py -q
```

## What the rules catch, measured on our own defects

| Defect class | Rows known | Caught by rules |
|---|---|---|
| Stem cites a text, no text present | 80 | **80 (100%)** |
| Near-duplicate options | 87 | **87 (100%)** |
| Malformed option text | 36 | 26 (72%) |
| No option answers the question | 34 | 1 (3%) |
| Wrong answer key | 11 | **0 (0%)** |

The last two rows are the point. **A structural gate cannot see a wrong key.** Those
classes need the semantic stage: a judge asked whether the claimed answer holds, plus a
human for anything it disputes. The test suite asserts this gap explicitly
(`test_semantic_classes_are_NOT_caught_by_rules`) so nobody mistakes the gate for proof.

## Rules that are deliberately warnings, not blocks

Each of these was a hard block until it rejected sound content, and was demoted:

- **Explanation over 90 words.** Row 1000 is 232 words and correct. Only an under-25-word
  floor blocks, because that usually means truncated output.
- **Long distractor rationales.** Over 40 words warns; over 80 blocks.
- **Options written as evaluative arguments** ("The argument is flawed because..."). This
  is a legitimate item format, so it warns and the human verifies the key.
- **An entity named nowhere else in the bank.** A warning routes it to review; it cannot be
  a hard rule because options legitimately introduce cases. This is the signal that would
  have surfaced "Tinker v. Delaware".

## Regression fixtures

`tests/fixtures/gate/` holds three sets:

- `known_bad.json` — all 248 quarantined rows with their reason and class.
- `verified.json` — rows read by hand and confirmed sound. Grows as humans verify.
- `candidates.json` — rows that passed the 2026-10-20 semantic gates.

Any change to a rule, a prompt or a model must keep: 100 percent rejection of the two
mechanical classes, at least 70 percent of malformed options, 100 percent acceptance of
verified rows, and at least 95 percent acceptance of candidates. The suite enforces all four.

## Still to build

- The semantic stage as a callable service, so `publish_drafts.py` can run the key test and
  the explanation-correspondence test inline rather than leaving those classes to a human.
- Grow `verified.json` from 2 rows to a real golden set; it is the only absolute truth the
  suite has today, and 2 is too thin.
- A weekly sweep of live rows through the gate to catch drift in content added by other
  paths.
