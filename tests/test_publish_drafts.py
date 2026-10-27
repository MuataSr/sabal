#!/usr/bin/env python3
"""The pipeline test: a broken draft cannot reach the served bank.

Builds a throwaway database with one sound draft and three broken ones, runs the
publisher exactly as the operator would, and asserts what landed: the sound row in
`questions` with provenance recorded, the broken rows still in the queue carrying their
reasons, and the bank unchanged for them.
"""
import json
import os
import shutil
import sqlite3
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLISH = os.path.join(ROOT, "scripts", "publish_drafts.py")


def child_python():
    """Interpreter to run the publisher with.

    sys.executable is empty under stripped environments (cron, systemd units, some
    sandboxes). Passing that empty string to subprocess fails with a bare
    "PermissionError: [Errno 13] Permission denied: ''", which names nothing and
    reads like a permissions bug in the pipeline. Resolve a real interpreter so the
    suite reports on the publisher rather than on how the suite was started.
    """
    candidates = [
        sys.executable,
        shutil.which("python3"),
        os.path.join(sys.exec_prefix, "bin", "python3"),
        "/usr/bin/python3",
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return "python3"

SCHEMA = """
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fcle_domain INTEGER, topic TEXT, difficulty TEXT, question TEXT,
    correct_answer TEXT, wrong_answers TEXT, explanation TEXT, stimulus TEXT,
    created_at TEXT, wrong_explanations TEXT);
CREATE TABLE questions_draft (
    id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT NOT NULL, gen_model TEXT,
    prompt_ver TEXT, created_at TEXT, gate_status TEXT DEFAULT 'pending',
    gate_notes TEXT);
"""

SOUND = {
    "fcle_domain": 1, "topic": "Federalism", "difficulty": "medium",
    "question": "Which clause of the Constitution lets Congress pass laws needed to "
                "carry out its enumerated powers?",
    "correct_answer": "The Necessary and Proper Clause",
    "wrong_answers": ["The Commerce Clause", "The Supremacy Clause",
                      "The Establishment Clause"],
    "explanation": "The Necessary and Proper Clause lets Congress pass laws needed to "
                   "carry out its listed powers. The Commerce Clause covers trade "
                   "between states, the Supremacy Clause settles conflicts between "
                   "federal and state law, and the Establishment Clause bars laws "
                   "respecting an establishment of religion.",
    "stimulus": "",
    "wrong_explanations": ["The Commerce Clause regulates trade, not implied powers.",
                           "The Supremacy Clause orders conflicting laws, not powers.",
                           "The Establishment Clause concerns religion."],
}

BROKEN = [
    {**SOUND, "wrong_answers": ["The Commerce Clause", "The commerce clause",
                                "The Supremacy Clause"]},
    {**SOUND, "explanation": "Too short."},
    {**SOUND, "question": "According to the provided text, which clause applies?",
     "stimulus": ""},
]


@pytest.fixture()
def db(tmp_path):
    path = str(tmp_path / "bank.db")
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    for item in [SOUND] + BROKEN:
        conn.execute(
            "INSERT INTO questions_draft (payload, gen_model, prompt_ver, created_at)"
            " VALUES (?,?,?,?)",
            (json.dumps(item), "test-model", "gen-test", "2026-10-21T00:00:00Z"))
    conn.commit()
    conn.close()
    return path


def run(db, apply=False):
    cmd = [child_python(), PUBLISH, "--db", db] + (["--apply"] if apply else [])
    return subprocess.run(cmd, capture_output=True, text=True)


def test_dry_run_changes_nothing(db):
    before = sqlite3.connect(db).execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    res = run(db, apply=False)
    assert res.returncode == 1, res.stdout + res.stderr
    after = sqlite3.connect(db).execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    assert before == after == 0
    assert "1 passed, 3 blocked" in res.stdout


def test_apply_lands_only_the_sound_row(db):
    res = run(db, apply=True)
    assert res.returncode == 1, res.stdout + res.stderr

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM questions").fetchall()
    assert len(rows) == 1, "only the sound draft may be published"
    assert rows[0]["correct_answer"] == SOUND["correct_answer"]
    assert json.loads(rows[0]["wrong_answers"]) == SOUND["wrong_answers"]

    prov = conn.execute("SELECT * FROM question_provenance").fetchall()
    assert len(prov) == 1
    assert prov[0]["question_id"] == rows[0]["id"]
    assert prov[0]["gen_model"] == "test-model"
    assert prov[0]["prompt_ver"] == "gen-test"
    assert prov[0]["gate_ver"].startswith("qc-")

    queue = conn.execute("SELECT gate_status, gate_notes FROM questions_draft").fetchall()
    assert len(queue) == 3, "blocked drafts stay in the queue for review"
    assert all(q["gate_status"] == "blocked" for q in queue)
    assert all(q["gate_notes"] for q in queue), "every block records why"


def test_generator_no_longer_writes_to_the_served_table():
    """The bypass is the bug. This asserts the generator's insert target."""
    src = open(os.path.join(ROOT, "scripts", "generate_questions.py")).read()
    assert "INSERT INTO questions_draft" in src
    assert "INSERT INTO questions\n" not in src, "generator still inserts into the bank"
