"""The no-account door must be the front door, not a footnote.

The public practice surface exists and works (`/practice`), but on 2026-10-22 the
live landing page still sent every prominent button to `/signup`, which asks for
an email address. A visitor clicking the obvious button hit the email form while
the no-account path sat in fine print underneath it. Mister K's report was
"the live website does not reflect the changes ... access it without using an
email address" - the route was live, the affordance was not.

These tests pin the affordance:

  1. the header and hero primary actions point at /practice,
  2. no signup-flavoured CTA ("Start free", "Start Practicing", "Check My FCLE
     Readiness") points at /signup,
  3. /signup itself offers the no-account escape hatch in both branches.

Behaviour runs against a throwaway database; the runtime DB is never touched.
"""

import html as html_mod
import os
import re
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

ANCHOR = re.compile(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.S)
TAGS = re.compile(r"<[^>]+>")

SIGNUP_CTA_PHRASES = ("Start free", "Start Practicing", "Check My FCLE Readiness")


def _anchors(page):
    """[(href, visible text)] with tags stripped and entities decoded."""
    out = []
    for href, inner in ANCHOR.findall(page):
        text = html_mod.unescape(TAGS.sub(" ", inner))
        out.append((href, re.sub(r"\s+", " ", text).strip()))
    return out


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
        self.tmp = tempfile.mkdtemp(prefix="sabal-landing-")
        self.mod.db.DB_PATH = os.path.join(self.tmp, "user_progress.db")
        self.mod.db.init_db()
        self.mod.db.init_active_quizzes_table()
        self.client = self.mod.app.test_client()

    def tearDown(self):
        self.mod.db.DB_PATH = self._orig_db
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestLandingSendsVisitorsToPractice(_Base):
    def setUp(self):
        super().setUp()
        resp = self.client.get("/")
        self.assertEqual(200, resp.status_code)
        self.page = resp.get_data(as_text=True)
        self.anchors = _anchors(self.page)

    def test_hero_primary_action_starts_practice(self):
        links = [(h, t) for h, t in self.anchors if t.startswith("Start Practicing Free")]
        self.assertTrue(links, "the hero's primary action is missing")
        self.assertEqual({"/practice"}, {h for h, _t in links},
                         "every 'Start Practicing' action must start practice, not signup")

    def test_header_action_starts_practice(self):
        links = [h for h, t in self.anchors if t == "Practice free"]
        self.assertEqual(["/practice"], links)

    def test_no_signup_flavoured_cta_points_at_signup(self):
        offenders = [(h, t) for h, t in self.anchors
                     if h.startswith("/signup") and t.startswith(SIGNUP_CTA_PHRASES)]
        self.assertEqual([], offenders,
                         "these CTAs promise practice but land on the email form")

    def test_the_page_states_no_account_is_needed(self):
        self.assertIn("No account, no email", html_mod.unescape(self.page))


class TestSignupOffersTheEscapeHatch(_Base):
    def test_signup_links_to_practice_without_an_account(self):
        page = self.client.get("/signup").get_data(as_text=True)
        anchors = _anchors(page)
        hrefs = [h for h, _t in anchors if h.startswith("/practice")]
        self.assertEqual(["/practice"], hrefs,
                         "the signup page must offer the no-account path")
        self.assertIn("No email needed", html_mod.unescape(page))


if __name__ == "__main__":
    unittest.main()
