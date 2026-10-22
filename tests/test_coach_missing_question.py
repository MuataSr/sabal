"""A question that left the bank must not take the Coach down with it.

The 2026-10-21 quarantine moved 250 rows out of `questions`. Every historical
answer pointing at one of them stopped resolving, so `_load_answers` handed the
readiness engine `domain=None`, and `int(a.get("domain", 0))` raised
`TypeError: int() argument must be ... not 'NoneType'`. `/coach` returned 500 for
any student with that history; a live account (id 79) hit it on 2026-10-22.

The fix skips answers whose question can no longer be resolved. These tests hold
both the unit behaviour and the page.
"""

import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


class TestReadinessSkipsUnresolvableAnswers(unittest.TestCase):
    def test_domain_readiness_tolerates_a_missing_domain(self):
        from coach import readiness

        now = datetime.now(timezone.utc)
        answers = [
            {"question_id": 1, "domain": None, "topic": None, "is_correct": True,
             "confidence": 3, "answered_at": (now - timedelta(days=1)).isoformat()},
            {"question_id": 2, "domain": 1, "topic": "Natural rights", "is_correct": True,
             "confidence": 2, "answered_at": (now - timedelta(days=2)).isoformat()},
        ]
        result = readiness.domain_readiness(answers, 1, now)
        self.assertEqual(1, result.attempted, "only the resolvable answer counts")

    def test_summarise_does_not_raise(self):
        from coach import readiness

        now = datetime.now(timezone.utc)
        answers = [{"question_id": 9, "domain": None, "topic": None, "is_correct": False,
                    "confidence": 3, "answered_at": (now - timedelta(days=3)).isoformat()}]
        summary = readiness.summarise(answers, now)
        self.assertFalse(summary["has_data"])


class TestCoachPageSurvivesMissingQuestion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as app_module
        cls.mod = app_module
        cls._orig_db = app_module.db.DB_PATH
        os.environ.pop("PILOT_SIGNUP_CAP", None)

    @classmethod
    def tearDownClass(cls):
        cls.mod.db.DB_PATH = cls._orig_db

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sabal-coach-")
        self.mod.db.DB_PATH = os.path.join(self.tmp, "user_progress.db")
        self.mod.db.init_db()
        self.mod.db.init_diagnostic_table()
        self.mod.db.init_active_quizzes_table()
        self.client = self.mod.app.test_client()
        user, _status = self.mod.db.create_user_capped(
            email="coach-check@example.com", display_name="Coach Check")
        self.assertIsNotNone(user, "the fixture account was not created")
        self.user_id = user["id"]
        # A question id that is not in the content bank, exactly like a
        # quarantined row: the answer resolves to no domain.
        session_id = self.mod.db.create_session(self.user_id, 1, 5)
        self.mod.db.record_answer(self.user_id, session_id, 999999,
                                  "A question that has left the bank", "a", "a", 0, 5, 3)
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.user_id

    def tearDown(self):
        self.mod.db.DB_PATH = self._orig_db
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_the_coach_renders(self):
        resp = self.client.get("/coach")
        self.assertEqual(200, resp.status_code)
        self.assertNotIn("Traceback", resp.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
