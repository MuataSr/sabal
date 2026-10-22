"""An anonymous visitor must never be handed a link that bounces to a login form.

Mister K, 2026-10-22: "the flow for the FREE account is gated - when you click on
anything in the side menu." The public practice surface was reachable, but the
sidebar still offered Coach, Diagnostic, Stimulus Hub, My Account, Progress and
the four /quiz domain links - every one of them a 302 to /login for a visitor
with no account. A menu item that needs an account is fine; a menu item that
looks like more practice and silently asks for an email is the gate he hit.

These tests pin the anonymous sidebar to the practice surface plus a clearly
labelled, optional account path, and pin the signed-in sidebar to the full menu.
"""

import os
import re
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SLUGS = ("american-democracy", "us-constitution", "founding-documents", "landmark-impact")

# Destinations that require a session. None may appear in an anonymous page.
GATED = ("/coach", "/diagnostic", "/stimulus", "/account", "/stats", "/settings",
         "/quiz/", "/logout")


def _hrefs(page):
    return re.findall(r'href="([^"]*)"', page)


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
        self.tmp = tempfile.mkdtemp(prefix="sabal-nav-")
        self.mod.db.DB_PATH = os.path.join(self.tmp, "user_progress.db")
        self.mod.db.init_db()
        self.mod.db.init_diagnostic_table()
        self.mod.db.init_active_quizzes_table()
        self.client = self.mod.app.test_client()

    def tearDown(self):
        self.mod.db.DB_PATH = self._orig_db
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestAnonymousSidebar(_Base):
    def setUp(self):
        super().setUp()
        resp = self.client.get("/practice")
        self.assertEqual(200, resp.status_code)
        self.page = resp.get_data(as_text=True)
        self.hrefs = _hrefs(self.page)

    def test_no_menu_item_points_at_a_login_wall(self):
        offenders = [(h, g) for h in self.hrefs for g in GATED
                     if h == g or h.startswith(g)]
        self.assertEqual([], offenders,
                         "an anonymous page links to a gated destination")

    def test_the_practice_surface_is_all_still_there(self):
        for slug in SLUGS:
            self.assertIn("/practice/%s" % slug, self.hrefs)
        self.assertIn("/practice", self.hrefs)

    def test_the_account_is_offered_as_optional(self):
        self.assertIn("/signup", self.hrefs)
        self.assertIn("/login", self.hrefs)
        self.assertIn("Practising needs none of it", self.page)


class TestSignedInSidebar(_Base):
    def test_the_full_menu_returns_for_a_registered_student(self):
        user, _status = self.mod.db.create_user_capped(
            email="nav-check@example.com", display_name="Nav Check")
        self.assertIsNotNone(user, "the fixture account was not created")
        self.mod.db.update_user(user["id"], onboarding_done=1)
        with self.client.session_transaction() as sess:
            sess["user_id"] = user["id"]

        page = self.client.get("/").get_data(as_text=True)
        hrefs = _hrefs(page)
        for expected in ("/coach", "/diagnostic", "/stimulus", "/stats", "/settings"):
            self.assertIn(expected, hrefs)


if __name__ == "__main__":
    unittest.main()
