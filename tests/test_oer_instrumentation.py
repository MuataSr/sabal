"""OER instrumentation: the open door, the wrinkle loop, and the funnel.

Written for the 2026-10-14 ruling that Sabal is 100% OER, permanently. Three
properties are locked here:

  1. NO STUDENT IS REFUSED A SEAT. The signup cap defaults to OFF; the seat
     machinery survives only as an emergency brake, and the page a student sees
     when it is on no longer talks about pilot cohorts or reserved seats.
  2. A STUDENT CAN FLAG A BAD QUESTION, from the feedback page they are already
     looking at, and the report keeps the option they picked. A "the marked
     answer looks wrong" report is undiagnosable later without it.
  3. THE FUNNEL IS DERIVED, NOT TRACKED. Every number comes from rows the app
     already writes, so "nobody came" and "they came, hit a wall, and left"
     stop looking identical.

Behaviour is exercised against a throwaway database; the real runtime DB is
never touched.
"""

import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


class _Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as app_module
        cls.mod = app_module
        cls._orig_db = app_module.db.DB_PATH
        cls._orig_cap = os.environ.pop("PILOT_SIGNUP_CAP", None)
        cls._orig_admin = os.environ.pop("PILOT_ADMIN_KEY", None)

    @classmethod
    def tearDownClass(cls):
        if cls._orig_cap is not None:
            os.environ["PILOT_SIGNUP_CAP"] = cls._orig_cap
        if cls._orig_admin is not None:
            os.environ["PILOT_ADMIN_KEY"] = cls._orig_admin

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sabal-oer-")
        self.mod.db.DB_PATH = os.path.join(self.tmp, "user_progress.db")
        self.mod.db.init_db()
        self.mod.db.init_active_quizzes_table()
        self.client = self.mod.app.test_client()
        os.environ.pop("PILOT_SIGNUP_CAP", None)
        os.environ.pop("PILOT_ADMIN_KEY", None)

    def tearDown(self):
        self.mod.db.DB_PATH = self._orig_db
        shutil.rmtree(self.tmp, ignore_errors=True)

    # helpers -------------------------------------------------------------
    def _email_count(self, email):
        con = self.mod.db._get_conn()
        try:
            return con.execute("SELECT COUNT(*) FROM users WHERE email = ?",
                               (email,)).fetchone()[0]
        finally:
            con.close()

    def _login(self, email="student@example.com", name="Student"):
        user, status = self.mod.db.create_user_capped(email=email, display_name=name)
        self.assertEqual(status, "ok")
        with self.client.session_transaction() as sess:
            sess["user_id"] = user["id"]
        return user


class TestNoSeatLimit(_Base):
    def test_signup_is_open_by_default(self):
        html = self.client.get("/signup").get_data(as_text=True)
        self.assertNotIn("Registration is paused", html)
        self.assertNotIn("pilot cohort", html)
        self.assertIn("Create your Sabal account", html)

    def test_two_clean_registrations_are_both_accepted(self):
        for addr in ("a@example.com", "b@example.com"):
            resp = self.client.post("/signup", data={"email": addr, "display_name": "S"})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.headers["Location"], "/registered")
        self.assertEqual(self._email_count("a@example.com"), 1)
        self.assertEqual(self._email_count("b@example.com"), 1)

    def test_the_cap_still_brakes_when_explicitly_set(self):
        """The emergency brake must still work, and must speak plainly."""
        os.environ["PILOT_SIGNUP_CAP"] = "1"
        first = self.client.post("/signup", data={"email": "first@example.com"})
        self.assertEqual(first.status_code, 302)
        second = self.client.post("/signup", data={"email": "second@example.com"})
        self.assertEqual(second.status_code, 200)
        html = second.get_data(as_text=True)
        self.assertIn("Registration is paused", html)
        self.assertNotIn("pilot cohort", html)
        self.assertEqual(self._email_count("second@example.com"), 0,
                         "the cap must be enforced server-side, not just hidden")

    def test_no_student_facing_template_mentions_a_pilot_cohort(self):
        templates = os.path.join(ROOT, "templates")
        for name in sorted(os.listdir(templates)):
            if not name.endswith(".html"):
                continue
            with open(os.path.join(templates, name), encoding="utf-8") as fh:
                text = fh.read().lower()
            self.assertNotIn("pilot cohort", text, "%s still promises a cohort" % name)


class TestQuestionReports(_Base):
    def test_reporting_requires_a_session(self):
        resp = self.client.post("/report-question", data={"question_id": 5})
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.headers["Location"])
        self.assertEqual(self.mod.db.count_question_reports("all"), 0)

    def test_a_report_is_stored_with_the_option_the_student_picked(self):
        self._login()
        resp = self.client.post("/report-question", data={
            "question_id": "42",
            "reason": "wrong-answer",
            "selected": "Divine right of kings",
            "note": "the stem asks for the source of authority and this contradicts it",
            "domain": "american-democracy",
            "next": "/results/american-democracy/abc",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn("report sent", resp.get_data(as_text=True))

        rows = self.mod.db.list_question_reports(status="all")
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["question_id"], 42)
        self.assertEqual(row["reason"], "wrong-answer")
        self.assertEqual(row["selected"], "Divine right of kings")
        self.assertEqual(row["domain"], "american-democracy")
        self.assertEqual(row["status"], "open")
        self.assertEqual(row["reporter"], "student@example.com")

    def test_a_report_without_a_question_id_is_ignored(self):
        self._login()
        resp = self.client.post("/report-question", data={"question_id": "", "reason": "typo"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.mod.db.count_question_reports("all"), 0)

    def test_a_long_note_is_truncated_not_rejected(self):
        self._login()
        resp = self.client.post("/report-question", data={
            "question_id": "7", "reason": "other", "note": "x" * 900})
        self.assertEqual(resp.status_code, 200)
        row = self.mod.db.list_question_reports(status="all")[0]
        self.assertEqual(len(row["note"]), 600)

    def test_the_control_renders_on_the_real_feedback_page(self):
        """Rendered through the app's own route, not read off the template."""
        user = self._login()
        questions = [
            {"id": 4242, "question_text": "Which principle holds that government derives "
                                          "its power from the people?",
             "options": ["Popular sovereignty", "Divine right of kings",
                         "Judicial review", "Federal supremacy"],
             "correct_answer": "Popular sovereignty",
             "wrong_answers": ["Divine right of kings", "Judicial review", "Federal supremacy"],
             "wrong_explanations": ["authority in a monarch", "courts assess laws",
                                    "which level prevails"],
             "explanation": "Popular sovereignty means power rests with the people.",
             "topic": "Natural rights and social contract", "domain": "american-democracy",
             "difficulty": "medium", "stimulus": None},
            {"id": 4243, "question_text": "Second item", "options": ["A", "B", "C", "D"],
             "correct_answer": "A", "wrong_answers": ["B", "C", "D"],
             "wrong_explanations": ["b", "c", "d"], "explanation": "because",
             "topic": "Natural rights and social contract", "domain": "american-democracy",
             "difficulty": "medium", "stimulus": None},
        ]
        con = self.mod.db._get_conn()
        cur = con.execute(
            "INSERT INTO quiz_sessions (user_id, domain, num_questions, started_at) "
            "VALUES (?, ?, ?, ?)",
            (user["id"], "american-democracy", 2, datetime.utcnow().isoformat()))
        session_id = cur.lastrowid
        con.commit()
        con.close()

        self.mod.db.save_quiz("oerquiz", {
            "user_id": user["id"], "session_id": session_id, "domain": "american-democracy",
            "questions": questions, "answers": [],
            "started_at": datetime.utcnow().isoformat(),
        })
        html = self.client.post(
            "/quiz/american-democracy/oerquiz/0/answer",
            data={"selected": "Divine right of kings", "confidence": 1, "time_elapsed": 4.0},
        ).get_data(as_text=True)
        self.assertIn('action="/report-question"', html)
        self.assertIn('name="question_id" value="4242"', html)
        self.assertIn('value="Divine right of kings"', html)


class TestAdminSurfaces(_Base):
    def test_they_are_unreachable_without_the_key(self):
        self.assertEqual(self.client.get("/admin/reports").status_code, 404)
        self.assertEqual(self.client.get("/admin/reports?key=guess").status_code, 404)
        self.assertEqual(self.client.get("/admin/funnel").status_code, 404)

    def test_reports_list_csv_export_and_resolve(self):
        os.environ["PILOT_ADMIN_KEY"] = "k3y"
        self._login()
        self.client.post("/report-question", data={
            "question_id": "4242", "reason": "typo", "note": "stray bracket"})

        page = self.client.get("/admin/reports?key=k3y")
        self.assertEqual(page.status_code, 200)
        self.assertIn("question reports", page.get_data(as_text=True))

        csv = self.client.get("/admin/reports?key=k3y&status=all&format=csv")
        self.assertIn("text/csv", csv.headers["Content-Type"])
        self.assertIn("sabal-question-reports.csv", csv.headers["Content-Disposition"])
        self.assertIn("student_picked", csv.get_data(as_text=True))

        rid = self.mod.db.list_question_reports(status="all")[0]["id"]
        resp = self.client.post("/admin/reports?key=k3y",
                                data={"key": "k3y", "status": "all", "resolve": str(rid)})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.mod.db.count_question_reports("open"), 0)
        self.assertEqual(self.mod.db.count_question_reports("resolved"), 1)

    def test_funnel_page_renders_the_derived_counts(self):
        os.environ["PILOT_ADMIN_KEY"] = "k3y"
        user = self._login()
        con = self.mod.db._get_conn()
        con.execute("UPDATE users SET onboarding_done = 1 WHERE id = ?", (user["id"],))
        con.commit()
        con.close()
        resp = self.client.get("/admin/funnel?key=k3y")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("Accounts registered", html)
        self.assertIn("Came back another day", html)


class TestPageCounters(_Base):
    def test_anonymous_arrivals_are_counted_aggregately(self):
        self.client.get("/")
        self.client.get("/")
        self.client.get("/signup")
        totals = {v["page"]: v["hits"] for v in self.mod.db.page_view_totals(days=30)}
        self.assertEqual(totals.get("landing"), 2)
        self.assertEqual(totals.get("signup"), 1)

    def test_nothing_identifying_is_stored_by_the_counter(self):
        self.client.get("/")
        con = self.mod.db._get_conn()
        try:
            cols = [r[1] for r in con.execute("PRAGMA table_info(page_views)")]
        finally:
            con.close()
        self.assertEqual(sorted(cols), ["day", "hits", "page"])


class TestFunnelCounts(_Base):
    def test_the_funnel_is_derived_from_rows_the_app_already_writes(self):
        user = self._login("one@example.com")
        con = self.mod.db._get_conn()
        now = datetime.utcnow()
        con.execute("UPDATE users SET onboarding_done = 1 WHERE id = ?", (user["id"],))
        con.execute("INSERT INTO quiz_sessions (user_id, domain, num_questions, started_at) "
                    "VALUES (?, ?, ?, ?)", (user["id"], "american-democracy", 5, now.isoformat()))
        con.execute("INSERT INTO quiz_sessions (user_id, domain, num_questions, started_at) "
                    "VALUES (?, ?, ?, ?)",
                    (user["id"], "american-democracy", 5,
                     (now - timedelta(days=2)).isoformat()))
        con.execute("INSERT INTO answers (user_id, session_id, question_id, question_text, "
                    "selected_answer, correct_answer, is_correct, time_elapsed, answered_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user["id"], 1, 4242, "q", "b", "a", 0, 4, now.isoformat()))
        con.commit()
        con.close()

        f = self.mod.db.funnel_counts(active_days=7)
        self.assertEqual(f["registered"], 1)
        self.assertEqual(f["onboarding_done"], 1)
        self.assertEqual(f["with_quiz_session"], 1)
        self.assertEqual(f["with_answer"], 1)
        self.assertEqual(f["returning"], 1, "two sessions on two days is a return")
        self.assertEqual(f["active_7d"], 1)
        self.assertEqual(f["answers"], 1)
        self.assertEqual(f["by_source"][0]["source"], "(none)")

    def test_internal_addresses_never_count_as_students(self):
        self._login("founder@example.com")
        os.environ["PILOT_INTERNAL_EMAILS"] = "founder@example.com"
        try:
            f = self.mod.db.funnel_counts(internal_emails=self.mod._pilot_internal_emails())
        finally:
            os.environ.pop("PILOT_INTERNAL_EMAILS", None)
        self.assertEqual(f["registered"], 0)


if __name__ == "__main__":
    unittest.main()
