"""Review mode: the SRS queue is served, not just written."""

import os
import shutil
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta


class ReviewModeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as app_module
        cls.mod = app_module
        cls._orig_db = app_module.db.DB_PATH

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sabal-review-")
        self.mod.db.DB_PATH = os.path.join(self.tmp, "user_progress.db")
        self.mod.db.init_db()
        self.mod.db.init_active_quizzes_table()
        self.mod.db.init_diagnostic_table()
        self.uid = self.mod.db.create_user(email="r@example.com", display_name="R")["id"]

    def tearDown(self):
        self.mod.db.DB_PATH = self._orig_db
        shutil.rmtree(self.tmp, ignore_errors=True)

    # helpers ---------------------------------------------------------------
    def _seed_review(self, qid, days_ago):
        when = (datetime.utcnow() + timedelta(days=days_ago)).isoformat()
        with sqlite3.connect(self.mod.db.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO review_queue (user_id, question_id, domain, topic, next_review)"
                " VALUES (?, ?, 'american-democracy', 'Federalism basics', ?)",
                (self.uid, qid, when),
            )

    def _real_question_ids(self, n):
        """Ids that exist in the content bank, so review can shape them."""
        return [q["id"] for q in self.mod.kb.get_all_quiz_questions(count=n)]

    def _login(self):
        c = self.mod.app.test_client()
        with c.session_transaction() as s:
            s["user_id"] = self.uid
        return c

    # due-card reads --------------------------------------------------------
    def test_due_ids_exclude_cards_scheduled_for_the_future(self):
        a, b, c = self._real_question_ids(3)
        self._seed_review(a, -1)
        self._seed_review(b, -5)
        self._seed_review(c, +3)
        ids = self.mod.db.get_due_review_ids(self.uid)
        self.assertEqual(len(ids), 2)
        self.assertEqual(self.mod.db.count_due_reviews(self.uid), 2)

    def test_due_ids_are_capped(self):
        for qid in self._real_question_ids(25):
            self._seed_review(qid, -1)
        self.assertEqual(len(self.mod.db.get_due_review_ids(self.uid, limit=20)), 20)
        self.assertEqual(self.mod.db.count_due_reviews(self.uid), 25)

    def test_other_students_cards_are_not_returned(self):
        other = self.mod.db.create_user(email="o@example.com", display_name="O")["id"]
        self._seed_review(self._real_question_ids(1)[0], -1)
        self.assertEqual(self.mod.db.get_due_review_ids(other), [])

    # the route -------------------------------------------------------------
    def test_review_route_starts_a_quiz(self):
        self._seed_review(self._real_question_ids(1)[0], -1)
        c = self._login()
        resp = c.get("/quiz/review", follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertRegex(resp.headers["Location"], r"^/quiz/review/[0-9a-f]{12}/0$")

    def test_nothing_due_sends_the_student_to_stats(self):
        c = self._login()
        resp = c.get("/quiz/review", follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/stats")

    def test_answering_a_review_card_moves_it_forward(self):
        self._seed_review(self._real_question_ids(1)[0], -1)
        c = self._login()
        quiz_id = c.get("/quiz/review").headers["Location"].split("/")[3]
        q = self.mod.db.load_quiz(quiz_id)["questions"][0]
        before = self.mod.db._get_conn().execute(
            "SELECT interval_days FROM review_queue WHERE user_id=? AND question_id=?",
            (self.uid, q["id"]),
        ).fetchone()["interval_days"]

        resp = c.post(f"/quiz/review/{quiz_id}/0/answer",
                      data={"selected": q["correct_answer"], "confidence": 3})
        self.assertEqual(resp.status_code, 200)

        row = self.mod.db._get_conn().execute(
            "SELECT interval_days, next_review FROM review_queue"
            " WHERE user_id=? AND question_id=?", (self.uid, q["id"])
        ).fetchone()
        self.assertGreater(row["interval_days"], before)
        self.assertGreater(row["next_review"], datetime.utcnow().isoformat())

    def test_review_answers_land_in_the_real_domain_not_in_review(self):
        self._seed_review(self._real_question_ids(1)[0], -1)
        c = self._login()
        quiz_id = c.get("/quiz/review").headers["Location"].split("/")[3]
        q = self.mod.db.load_quiz(quiz_id)["questions"][0]
        c.post(f"/quiz/review/{quiz_id}/0/answer",
               data={"selected": q["correct_answer"], "confidence": 3})
        domains = {r["domain"] for r in self.mod.db._get_conn().execute(
            "SELECT domain FROM topic_mastery WHERE user_id=?", (self.uid,))}
        self.assertNotIn("review", domains)
        self.assertEqual(len(domains), 1)

    # the stats card --------------------------------------------------------
    def test_stats_shows_the_due_count_and_a_way_in(self):
        self._seed_review(self._real_question_ids(1)[0], -1)
        c = self._login()
        html = c.get("/stats").get_data(as_text=True)
        self.assertIn("due for review", html)
        self.assertIn('href="/quiz/review"', html)
        self.assertNotIn("background: ;", html)   # domain colours must reach the template

    # diagnostic comparison -------------------------------------------------
    def test_since_diagnostic_compares_raw_to_raw(self):
        qids = self._real_question_ids(9)
        meta = self.mod.kb.get_question_topics(qids)
        slug_by_id = {i["id"]: s for s, i in self.mod._DOMAIN_GETTERS.items()}
        topic_domain, topic_name = meta[qids[0]]
        sid = self.mod.db.create_session(user_id=self.uid, domain="mixed", num_questions=9)
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.mod.db.DB_PATH) as conn:
            for i, qid in enumerate(qids):
                conn.execute(
                    "INSERT INTO answers (user_id, session_id, question_id, question_text,"
                    " selected_answer, correct_answer, is_correct, confidence, time_elapsed, answered_at)"
                    " VALUES (?, ?, ?, 'q', 'a', 'a', ?, 3, 5, ?)",
                    (self.uid, sid, qid, 1 if i < 7 else 0, now))
            conn.execute(
                "INSERT INTO diagnostic_baselines (user_id, domain, topic, total, correct, pct, taken_at)"
                " VALUES (?, ?, ?, 1, 0, 0.0, ?)",
                (self.uid, slug_by_id[topic_domain], topic_name, now))
            conn.execute(
                "INSERT INTO diagnostic_baselines (user_id, domain, topic, total, correct, pct, taken_at)"
                " VALUES (?, 'us-constitution', 'Topic aced at signup', 1, 1, 100.0, ?)", (self.uid, now))

        html = self._login().get("/stats").get_data(as_text=True)
        self.assertIn("Since your diagnostic", html)
        # Tie each number to its own label: a 50% elsewhere on the page must not satisfy this.
        self.assertRegex(html, r"Diagnostic on \S+: <strong>50%</strong>\s+of 2 questions")
        self.assertRegex(html, r"Unassisted practice since: <strong>78%</strong>\s+of 9 answers")
        self.assertIn(topic_name, html)


if __name__ == "__main__":
    unittest.main()
