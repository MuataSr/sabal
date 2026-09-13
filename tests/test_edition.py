"""Edition separation and the no-caps promise are product guarantees.

These lock the two faults found on the live box:

1. `APP_EDITION` defaulted to the PAID edition, so a deploy that forgot the
   variable silently served paid surfaces (and AI copy) to students. It now
   fails closed: unset means free, and the paid edition must be named.

2. The account page computed the daily question count by calling
   platform_lib.questions_remaining() directly, ignoring both the edition and
   launch mode, and rendered "0 / 10 free" beside copy promising no limits.
   The free edition has no caps.

If someone later re-opens either hole, these fail.
"""

import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Any string that must never reach a student in the free OER edition.
BANNED = [
    "AI Tutor",
    "AI tutor",
    "Sabal Premium",
    "Premium analytics",
    "Unlock with Premium",
    "Upgrade for unlimited practice",
    "questions/day",
    "one-time FCLE pass",
]


def _edition_with(value):
    """Load the app in a fresh process with APP_EDITION set to `value`."""
    env = dict(os.environ)
    if value is None:
        env.pop("APP_EDITION", None)
    else:
        env["APP_EDITION"] = value
    code = "import app;print('%s|%s' % (app.APP_EDITION, app.FREE_EDITION))"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True,
                         text=True, cwd=ROOT, env=env, timeout=120)
    return out.stdout.strip()


class TestEditionFailsClosed(unittest.TestCase):
    def test_unset_means_free_not_paid(self):
        self.assertEqual(_edition_with(None), "free|True",
                         "an unset APP_EDITION must serve the FREE edition")

    def test_misspelled_means_free(self):
        for value in ("typo", "", "FREE ", "1"):
            self.assertTrue(_edition_with(value).endswith("|True"),
                            "APP_EDITION=%r must fall back to free" % value)

    def test_paid_edition_must_be_named(self):
        for value in ("pro", "full"):
            self.assertTrue(_edition_with(value).endswith("|False"),
                            "APP_EDITION=%r must be the paid edition" % value)

    def test_source_no_longer_defaults_to_full(self):
        with open(os.path.join(ROOT, "app.py"), encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn('os.environ.get("APP_EDITION", "full")', src,
                         "the fail-open default must not come back")


class TestFreeEditionSurface(unittest.TestCase):
    """Render the real app in the free edition and sweep every anon-reachable page."""

    @classmethod
    def setUpClass(cls):
        os.environ.pop("APP_EDITION", None)          # fail-closed -> free
        os.environ["FCLE_FREE_LAUNCH"] = "1"
        sys.path.insert(0, ROOT)
        import app as app_module
        cls.mod = app_module
        if not app_module.FREE_EDITION:
            raise unittest.SkipTest("app did not load in the free edition")
        cls.client = app_module.app.test_client()

    def _text(self, path):
        resp = self.client.get(path, follow_redirects=True)
        html = resp.get_data(as_text=True)
        body = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
        body = re.sub(r"(?s)<[^>]+>", " ", body)
        return resp.status_code, re.sub(r"\s+", " ", body)

    def test_anon_pages_carry_no_paid_or_ai_surface(self):
        for path in ("/", "/signup", "/login"):
            _code, text = self._text(path)
            leaked = [b for b in BANNED if b in text]
            self.assertEqual(leaked, [], "%s leaked %s" % (path, leaked))

    def test_no_link_to_a_route_that_404s_here(self):
        for path in ("/", "/signup", "/login"):
            _code, text = self._text(path)
            for dead in ("/pricing", "/tutor"):
                self.assertNotIn('href="%s"' % dead, self.client.get(path).get_data(as_text=True),
                                 "%s advertises %s, which is 404 in the free edition" % (path, dead))

    def test_paid_routes_do_not_exist(self):
        for path in ("/pricing", "/tutor"):
            self.assertEqual(self.client.get(path).status_code, 404,
                             "%s must be absent, not hidden, in the free edition" % path)

    def test_no_daily_cap(self):
        self.assertIsNone(self.mod._questions_remaining_for({"id": 1}),
                          "the free edition has no caps")
        self.assertIsNone(self.mod._questions_left_today(),
                          "the free edition has no caps")

    def test_account_page_shows_unlimited_not_a_quota(self):
        """The exact regression: '0 / 10 free' beside copy promising no limits."""
        import sqlite3
        db_path = os.path.join(ROOT, "data", "user_progress.db")
        if not os.path.exists(db_path):
            self.skipTest("no user db on this machine")
        con = sqlite3.connect(db_path)
        row = con.execute("SELECT id FROM users ORDER BY id LIMIT 1").fetchone()
        con.close()
        if not row:
            self.skipTest("no users on this machine")
        with self.client.session_transaction() as sess:
            sess["user_id"] = row[0]
        _code, text = self._text("/account")
        self.assertIn("Unlimited", text)
        self.assertNotRegex(text, r"\d+\s*/\s*\d+\s*free")
        self.assertEqual([b for b in BANNED if b in text], [], "account page leaked paid copy")


if __name__ == "__main__":
    unittest.main()
