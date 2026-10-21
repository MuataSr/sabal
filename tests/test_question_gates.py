#!/usr/bin/env python3
"""The gate's proof: every defect we have found must be refused, and sound rows accepted.

Two kinds of test here.

Mutation tests build a sound item and inject one defect at a time. They prove each rule
actually fires on realistic content, not just on a toy string.

Fixture tests run the gate over rows we already know the answer to: the 248 rows
quarantined on 2026-10-20/21, two rows verified by hand, and 336 rows that passed the
semantic gates. The expectations are per defect class, because a single aggregate number
would hide the important fact: structural rules cannot see a wrong key, and the suite says
so out loud instead of implying the gate is sufficient.
"""
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import qc_item  # noqa: E402

FIX = os.path.join(ROOT, "tests", "fixtures", "gate")


def load(name):
    with open(os.path.join(FIX, name)) as f:
        return json.load(f)


def sound_item():
    return {
        "fcle_domain": 1,
        "topic": "Federalism",
        "difficulty": "medium",
        "question": "Which clause of the Constitution gives Congress the power to pass "
                    "laws necessary for carrying out its enumerated powers?",
        "correct_answer": "The Necessary and Proper Clause",
        "wrong_answers": json.dumps([
            "The Commerce Clause",
            "The Supremacy Clause",
            "The Establishment Clause",
        ]),
        "explanation": "The Necessary and Proper Clause lets Congress pass laws needed to "
                       "carry out its listed powers. The Commerce Clause covers trade "
                       "between states, the Supremacy Clause settles conflicts between "
                       "federal and state law, and the Establishment Clause bars laws "
                       "respecting an establishment of religion.",
        "stimulus": "",
        "wrong_explanations": json.dumps([
            "The Commerce Clause regulates trade, not Congress's implied powers.",
            "The Supremacy Clause orders conflicting laws, not new powers.",
            "The Establishment Clause concerns religion, not legislative power.",
        ]),
    }


def test_a_sound_item_passes():
    res = qc_item.gate(sound_item())
    assert res["passed"], res["violations"]
    assert res["checks"] >= 10


# ---------------------------------------------------------------- mutation tests

def mutated(**changes):
    item = sound_item()
    item.update(changes)
    return qc_item.gate(item)


@pytest.mark.parametrize("changes,needle", [
    ({"wrong_answers": json.dumps(["The Commerce Clause", "The Commerce Clause",
                                   "The Supremacy Clause"])},
     "identical after normalisation"),
    ({"wrong_answers": json.dumps(["The Supremacy Clause", "The Establishment Clause",
                                   "A. The Necessary and Proper Clause"])},
     "baked-in letter"),
    ({"wrong_answers": json.dumps(["This distractor is incorrect because trade differs",
                                   "The Supremacy Clause",
                                   "The Establishment Clause"])},
     "rebuttal, not an answer"),
    ({"explanation": "Option C is correct because the clause is implied."},
     "names another option as correct"),
    ({"explanation": "The claim that this is right is mistaken."},
     "The claim that"),
    ({"explanation": "Too short."},
     "too short to teach anything"),
    ({"question": "According to the provided text, which clause covers implied powers?",
      "stimulus": ""},
     "cites a text but stimulus is missing"),
])
def test_each_rule_fires(changes, needle):
    res = mutated(**changes)
    assert not res["passed"], "gate accepted an item it should refuse"
    assert any(needle in v for v in res["violations"]), res["violations"]


def test_near_duplicate_options_are_refused():
    res = mutated(wrong_answers=json.dumps([
        "The Necessary and Proper Clause",
        "The necessary and proper clause",
        "The Supremacy Clause"]))
    assert not res["passed"]
    assert any("near-duplicates" in v for v in res["violations"])


def test_duplicate_stem_against_the_bank_is_refused():
    item = sound_item()
    # exact copy of a stem already in the bank
    res = qc_item.gate(item, existing_stems=[item["question"]])
    assert not res["passed"]
    assert any("identical stem" in v for v in res["violations"])
    # near copy: one word changed, so it is not identical but is clearly the same item
    near = item["question"].replace("enumerated", "delegated")
    assert near != item["question"]
    res = qc_item.gate(item, existing_stems=[near])
    assert not res["passed"]
    assert any("near-duplicate of an existing stem" in v for v in res["violations"])


def test_long_explanation_warns_but_does_not_block():
    item = sound_item()
    item["explanation"] = item["explanation"] + " " + ("Context. " * 60)
    res = qc_item.gate(item)
    assert res["passed"], res["violations"]
    assert any("above the" in w for w in res["warnings"])


# ---------------------------------------------------------------- fixture recall

def classify(entry):
    reason = entry["reason"]
    if "near-duplicate" in reason:
        return "near-duplicate"
    if "no text" in reason:
        return "missing text"
    if "malformed" in reason:
        return "malformed options"
    if "no option answers" in reason:
        return "no valid option"
    return "wrong key"


def rate(entries):
    """(rejected, total) over the fixture."""
    rejected = sum(1 for e in entries if not qc_item.gate(e["item"])["passed"])
    return rejected, len(entries)


def test_mechanical_classes_are_caught_completely():
    bad = load("known_bad.json")
    for cls in ("near-duplicate", "missing text"):
        hit, n = rate([b for b in bad if classify(b) == cls])
        assert n >= 80, "%s fixture shrank unexpectedly (%d)" % (cls, n)
        assert hit == n, "%s: %d of %d caught" % (cls, hit, n)


def test_malformed_options_are_mostly_caught():
    """Measured recall is 25 of 36 (69%). The bar is 0.65: if a change drops it, the
    rule lost teeth, and the fixture says so rather than the number drifting silently."""
    bad = [b for b in load("known_bad.json") if classify(b) == "malformed options"]
    hit, n = rate(bad)
    assert n >= 30
    assert hit / n >= 0.65, "malformed option recall fell to %d/%d" % (hit, n)


def test_semantic_classes_are_NOT_caught_by_rules():
    """The gate cannot see a wrong key, and must not pretend it can.

    This asserts the gap rather than hiding it: those rows need the semantic stage or a
    human, so a future change that claims rules coverage for them is a regression in
    honesty, not an improvement.
    """
    bad = load("known_bad.json")
    for cls in ("wrong key", "no valid option"):
        hit, n = rate([b for b in bad if classify(b) == cls])
        assert n >= 10, "%s fixture shrank unexpectedly (%d)" % (cls, n)
        assert hit / n <= 0.25, "%s: rules caught %d of %d, which should be impossible" % (
            cls, hit, n)


def test_hand_verified_rows_are_accepted():
    verified = load("verified.json")
    assert len(verified) >= 2
    for v in verified:
        res = qc_item.gate(v["item"])
        assert res["passed"], "gate refused verified row %s: %s" % (v["id"], res["violations"])


def test_rows_that_passed_the_semantic_gates_mostly_pass():
    cands = load("candidates.json")
    assert len(cands) >= 300
    rejected, n = rate(cands)
    assert (n - rejected) / n >= 0.95, "only %d of %d previously gated rows pass the rules" % (
        n - rejected, n)
