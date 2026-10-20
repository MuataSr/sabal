"""Public practice: an OER Commons criterion, implemented and pinned.

OER Commons rejected Sabal on 2026-10-16 because a student had to hand over an
email address before reaching the questions. Their Collection Policy, in the
Openness section, prohibits "requiring users to provide personal information,
creating an account to access". The librarian's own words were that making the
materials accessible without registration "would address that particular
barrier". This surface is that fix, and these tests hold it in place:

  1. every domain serves real questions with full explanations to a visitor who
     is not logged in,
  2. nothing about that visitor is stored and no cookie is set,
  3. a visitor can still report a broken question without an account,
  4. the pages are indexable and listed for crawlers.

Behaviour runs against a throwaway database; the runtime DB is never touched.
"""

import html as html_mod
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SLUGS = ("american-democracy", "us-constitution", "founding-documents",
         "landmark-impact", "mixed")


class _Base(unittest.TestCase):
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
        self.tmp = tempfile.mkdtemp(prefix="sabal-practice-")
        self.mod.db.DB_PATH = os.path.join(self.tmp, "user_progress.db")
        self.mod.db.init_db()
        self.mod.db.init_active_quizzes_table()
        self.client = self.mod.app.test_client()

    def tearDown(self):
        self.mod.db.DB_PATH = self._orig_db
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- helpers ----------------------------------------------------------
    def _question_from_page(self, slug="american-democracy"):
        """(question_id, option texts in the order the page presented them)."""
        page = self.client.get("/practice/%s" % slug).get_data(as_text=True)
        qid = re.search(r'name="question_id" value="(\d+)"', page).group(1)
        opts = [html_mod.unescape(o) for o in re.findall(r'name="opt\d" value="([^"]*)"', page)]
        return qid, opts

    def _counts(self):
        conn = sqlite3.connect(self.mod.db.DB_PATH)
        out = {}
        for table in ("users", "quiz_sessions", "answers", "question_reports"):
            try:
                out[table] = conn.execute("SELECT COUNT(*) FROM %s" % table).fetchone()[0]
            except sqlite3.OperationalError:
                out[table] = None
        conn.close()
        return out

    def _answer(self, slug, qid, opts, selected, c=0, t=0):
        data = {"question_id": qid, "selected": selected, "c": str(c), "t": str(t)}
        for i, text in enumerate(opts):
            data["opt%d" % i] = text
        return self.client.post("/practice/%s/answer" % slug, data=data)


class TestNoAccountIsRequired(_Base):
    def test_the_hub_renders_for_a_visitor_with_no_account(self):
        resp = self.client.get("/practice")
        self.assertEqual(200, resp.status_code)
        page = resp.get_data(as_text=True)
        self.assertIn("No account, no email", page)
        for slug, _name, _blurb in self.mod._PUBLIC_PRACTICE:
            self.assertIn("/practice/%s" % slug, page)

    def test_every_domain_serves_a_real_question_without_logging_in(self):
        for slug in SLUGS:
            resp = self.client.get("/practice/%s" % slug)
            self.assertEqual(200, resp.status_code, "%s did not serve a question" % slug)
            page = resp.get_data(as_text=True)
            self.assertIn('name="selected"', page, "%s has no answerable options" % slug)
            self.assertEqual(4, page.count("name=\"opt"), "%s must present four options" % slug)

    def test_a_mangled_domain_redirects_instead_of_erroring(self):
        resp = self.client.get("/practice/not-a-domain")
        self.assertEqual(302, resp.status_code)
        self.assertIn("/practice", resp.headers.get("Location", ""))

    def test_the_public_page_points_at_the_account_as_optional(self):
        page = self.client.get("/practice").get_data(as_text=True)
        self.assertIn("Want your scores kept", page)
        self.assertIn("/signup", page)


class TestAnsweringWorks(_Base):
    def test_a_correct_answer_is_graded_correct(self):
        qid, opts = self._question_from_page()
        correct = self.mod.kb.get_shaped_question_by_id(int(qid))["correct_answer"]
        page = self._answer("american-democracy", qid, opts, correct).get_data(as_text=True)
        self.assertIn("Correct.", page)
        self.assertIn("Why the answer is right", page)

    def test_a_wrong_answer_explains_why_that_option_was_tempting(self):
        qid, opts = self._question_from_page()
        shaped = self.mod.kb.get_shaped_question_by_id(int(qid))
        wrong = [o for o in opts if o != shaped["correct_answer"]][0]
        page = self._answer("american-democracy", qid, opts, wrong).get_data(as_text=True)
        self.assertIn("Not quite", page)
        self.assertIn("Why your choice was tempting", page)

    def test_the_visit_tally_carries_forward(self):
        qid, opts = self._question_from_page()
        correct = self.mod.kb.get_shaped_question_by_id(int(qid))["correct_answer"]
        page = self._answer("american-democracy", qid, opts, correct, c=3, t=4).get_data(as_text=True)
        self.assertIn("4 of 5 correct this visit", page)

    def test_the_options_keep_the_order_the_visitor_saw(self):
        qid, opts = self._question_from_page()
        correct = self.mod.kb.get_shaped_question_by_id(int(qid))["correct_answer"]
        shuffled = [opts[2], opts[0], opts[3], opts[1]]
        page = self._answer("american-democracy", qid, shuffled, correct).get_data(as_text=True)
        self.assertLess(page.index(html_mod.escape(shuffled[0], quote=False)),
                        page.index(html_mod.escape(shuffled[1], quote=False)),
                        "the answered page re-ordered the options the visitor just saw")

    def test_a_bad_question_id_does_not_error(self):
        resp = self.client.post("/practice/american-democracy/answer",
                                data={"question_id": "999999", "selected": "x"})
        self.assertEqual(302, resp.status_code)


class TestNothingAboutTheVisitorIsStored(_Base):
    def test_a_full_visit_writes_no_per_visitor_rows(self):
        before = self._counts()
        self.client.get("/practice")
        qid, opts = self._question_from_page()
        self._answer("american-democracy", qid, opts, opts[0])
        self.client.get("/practice/mixed")
        self.assertEqual(before, self._counts(),
                         "public practice must not create users, sessions, answers or reports")

    def test_no_cookie_is_set(self):
        responses = [self.client.get("/practice"),
                     self.client.get("/practice/american-democracy")]
        qid, opts = self._question_from_page()
        responses.append(self._answer("american-democracy", qid, opts, opts[0]))
        for resp in responses:
            self.assertNotIn("Set-Cookie", resp.headers,
                             "public practice must not set a cookie")


class TestAnAnonymousVisitorCanReportABrokenQuestion(_Base):
    def test_a_report_is_accepted_with_no_account_and_recorded_with_no_user(self):
        qid, opts = self._question_from_page()
        resp = self.client.post("/report-question", data={
            "question_id": qid, "reason": "typo", "selected": opts[0],
            "domain": "american-democracy", "next": "/practice/american-democracy",
            "note": "option text looks truncated",
        })
        self.assertEqual(200, resp.status_code)
        conn = sqlite3.connect(self.mod.db.DB_PATH)
        rows = conn.execute("SELECT user_id, question_id, reason FROM question_reports").fetchall()
        conn.close()
        self.assertEqual(1, len(rows))
        self.assertIsNone(rows[0][0], "an anonymous report must store no user")
        self.assertEqual(int(qid), rows[0][1])

    def test_a_report_for_a_question_that_does_not_exist_is_dropped(self):
        self.client.post("/report-question", data={"question_id": "999999", "reason": "typo"})
        conn = sqlite3.connect(self.mod.db.DB_PATH)
        n = conn.execute("SELECT COUNT(*) FROM question_reports").fetchone()[0]
        conn.close()
        self.assertEqual(0, n)


class TestThePracticePagesAreCrawlable(_Base):
    def test_robots_allows_practice(self):
        body = self.client.get("/robots.txt").get_data(as_text=True)
        self.assertIn("Allow: /practice", body)

    def test_the_sitemap_lists_the_practice_pages(self):
        body = self.client.get("/sitemap.xml").get_data(as_text=True)
        self.assertIn("/practice</loc>", body)
        for slug in ("american-democracy", "us-constitution", "founding-documents", "landmark-impact"):
            self.assertIn("/practice/%s</loc>" % slug, body)
        self.assertNotIn("/practice/mixed</loc>", body,
                         "mixed practice is a random selection, not a page to index")

    def test_the_pages_ask_to_be_indexed(self):
        for path in ("/practice", "/practice/american-democracy"):
            page = self.client.get(path).get_data(as_text=True)
            self.assertIn('content="index, follow"', page, "%s is not indexable" % path)
            self.assertIn('rel="canonical"', page, "%s has no canonical" % path)


if __name__ == "__main__":
    unittest.main()
