"""Evidence provenance: a result is three-state, and help is not cold mastery.

Three properties are locked here, all from the 2026-11-06 decision to take
DeepTutor's evidence-separation pattern without taking its scheduler:

  1. `answers` carries `result` (correct / partial / incorrect), and
     `is_correct` stays derived from it so every existing reader keeps working.
  2. An answer given right after a tutor conversation is recorded, but it never
     moves topic mastery, the review queue, or the readiness percentage.
  3. Old rows backfill from `is_correct`, so the migration is safe on the live DB.

Behaviour runs against a throwaway database; the runtime DB is never touched.
"""

import os
import shutil
import sqlite3
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


class _Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as app_module
        cls.mod = app_module
        cls._orig_db = app_module.db.DB_PATH

    @classmethod
    def tearDownClass(cls):
        cls.mod.db.DB_PATH = cls._orig_db

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sabal-provenance-")
        self.mod.db.DB_PATH = os.path.join(self.tmp, "user_progress.db")
        self.mod.db.init_db()
        self.mod.db.init_active_quizzes_table()
        self.client = self.mod.app.test_client()

    def tearDown(self):
        self.mod.db.DB_PATH = self._orig_db
        shutil.rmtree(self.tmp, ignore_errors=True)

    # helpers -------------------------------------------------------------
    def _login(self, email="student@example.com"):
        user, status = self.mod.db.create_user_capped(email=email, display_name="Student")
        self.assertEqual(status, "ok")
        with self.client.session_transaction() as sess:
            sess["user_id"] = user["id"]
        return user

    def _rows(self, sql, params=()):
        con = sqlite3.connect(self.mod.db.DB_PATH)
        con.row_factory = sqlite3.Row
        try:
            return con.execute(sql, params).fetchall()
        finally:
            con.close()

    def _quiz(self, user_id, quiz_id="q1", qid=1):
        quiz = {
            "user_id": user_id, "session_id": None, "domain": "american-democracy",
            "questions": [{
                "id": qid, "question_text": "Which principle?", "topic": "Popular sovereignty",
                "correct_answer": "Popular sovereignty", "options": ["A", "B", "C", "Popular sovereignty"],
                "explanation": "", "wrong_explanations": [],
            }],
            "answers": [],
        }
        self.mod.db.save_quiz(quiz_id, quiz)
        return quiz_id

    def _answer(self, quiz_id, selected="Popular sovereignty", confidence=3):
        return self.client.post(
            "/quiz/american-democracy/%s/0/answer" % quiz_id,
            data={"selected": selected, "time_elapsed": 4, "confidence": confidence},
        )


class TestSchemaAndBackfill(_Base):
    def test_the_three_columns_exist(self):
        cols = {r["name"] for r in self._rows("PRAGMA table_info(answers)")}
        self.assertLessEqual({"result", "assistance_used", "assistance_context"}, cols)

    def test_old_correct_rows_backfill_to_correct(self):
        uid = self._login()["id"]
        con = sqlite3.connect(self.mod.db.DB_PATH)
        con.row_factory = sqlite3.Row
        session_id = self.mod.db.create_session(uid, "american-democracy", 1)
        con.execute(
            "INSERT INTO answers (user_id, session_id, question_id, question_text, selected_answer,"
            " correct_answer, is_correct, time_elapsed, answered_at, result)"
            " VALUES (?, ?, 1, 'q', 'a', 'a', 1, 3, '2026-01-01T00:00:00', 'incorrect')",
            (uid, session_id),
        )
        con.commit()
        con.close()

        self.mod.db.init_db()   # the migration is what replays the backfill

        row = self._rows("SELECT result FROM answers WHERE session_id=?", (session_id,))[0]
        self.assertEqual(row["result"], "correct")

    def test_record_answer_derives_is_correct_from_result(self):
        uid = self._login()["id"]
        session_id = self.mod.db.create_session(uid, "american-democracy", 1)
        self.mod.db.record_answer(
            user_id=uid, session_id=session_id, question_id=7, question_text="q",
            selected="24x", correct="24x-18", is_correct=True, time_elapsed=2,
            result="partial",
        )
        row = self._rows("SELECT result, is_correct FROM answers WHERE question_id=7")[0]
        self.assertEqual(row["result"], "partial")
        self.assertEqual(row["is_correct"], 0)


class TestTutorWindow(_Base):
    def test_no_tutor_history_means_no_assistance(self):
        self.assertFalse(self.mod.db.recent_tutor_help(1))

    def test_a_fresh_student_message_counts_as_assistance(self):
        con = sqlite3.connect(self.mod.db.DB_PATH)
        con.execute("INSERT INTO tutor_messages (user_id, role, content, domain) VALUES (1, 'student', 'explain this', 2)")
        con.commit()
        con.close()
        self.assertTrue(self.mod.db.recent_tutor_help(1))

    def test_an_old_message_does_not(self):
        con = sqlite3.connect(self.mod.db.DB_PATH)
        con.execute(
            "INSERT INTO tutor_messages (user_id, role, content, domain, created_at)"
            " VALUES (1, 'student', 'explain this', 2, datetime('now', '-2 hours'))"
        )
        con.commit()
        con.close()
        self.assertFalse(self.mod.db.recent_tutor_help(1))

    def test_a_tutor_reply_alone_is_not_the_learner_asking(self):
        con = sqlite3.connect(self.mod.db.DB_PATH)
        con.execute("INSERT INTO tutor_messages (user_id, role, content, domain) VALUES (1, 'tutor', 'here you go', 2)")
        con.commit()
        con.close()
        self.assertFalse(self.mod.db.recent_tutor_help(1))


class TestGateOnTheQuizPath(_Base):
    def test_a_cold_answer_moves_mastery(self):
        user = self._login()
        quiz_id = self._quiz(user["id"])
        self._answer(quiz_id)
        self.assertEqual(len(self._rows("SELECT * FROM topic_mastery")), 1)
        self.assertEqual(len(self._rows("SELECT * FROM review_queue")), 1)

    def test_a_help_assisted_answer_is_recorded_but_not_counted(self):
        user = self._login()
        quiz_id = self._quiz(user["id"])
        con = sqlite3.connect(self.mod.db.DB_PATH)
        con.execute("INSERT INTO tutor_messages (user_id, role, content, domain) VALUES (?, 'student', 'explain', 2)", (user["id"],))
        con.commit()
        con.close()

        self._answer(quiz_id)

        answers = self._rows("SELECT result, assistance_used, assistance_context FROM answers")
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0]["result"], "correct")
        self.assertEqual(answers[0]["assistance_used"], 1)
        self.assertEqual(answers[0]["assistance_context"], "tutor_chat_15m")
        self.assertEqual(self._rows("SELECT * FROM topic_mastery"), [])
        self.assertEqual(self._rows("SELECT * FROM review_queue"), [])

    def test_readiness_ignores_assisted_answers(self):
        user = self._login()
        session_id = self.mod.db.create_session(user["id"], "american-democracy", 2)
        for qid, assisted in ((1, 0), (2, 1)):
            self.mod.db.record_answer(
                user_id=user["id"], session_id=session_id, question_id=qid,
                question_text="q", selected="a", correct="a", is_correct=False,
                time_elapsed=1, assistance_used=assisted,
            )
        # No topic_mastery rows, so this exercises the answers fallback.
        self.assertEqual(self.mod.db.get_readiness(user["id"], "american-democracy"), 0.0)


if __name__ == "__main__":
    unittest.main()
