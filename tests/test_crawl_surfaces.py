"""Crawl surfaces: can a search engine find the page, and does a shared link look like anything?

Written after a live audit on 2026-10-15 found `/robots.txt` and `/sitemap.xml` both
404, the landing page carrying no canonical, no Open Graph tags and no structured
data, and the top-ranking competitors ranking on phrases the page never used.

Two things are locked here beyond mere presence:
  * the Open Graph title and description are the APPROVED title and meta
    description, so this block cannot smuggle in unapproved copy or a new number;
  * the FAQPage structured data mirrors questions that are actually visible on
    the page, which is what schema.org and Google both require.
"""

import json
import os
import re
import shutil
import struct
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

LANDING = os.path.join(ROOT, "templates", "landing.html")
OG_IMAGE = os.path.join(ROOT, "static", "img", "sabal-og-card.png")
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError("%s is not a PNG" % path)
    return struct.unpack(">II", head[16:24])


class TestRobotsTxt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as app_module
        cls.client = app_module.app.test_client()
        cls.resp = cls.client.get("/robots.txt")
        cls.body = cls.resp.get_data(as_text=True)

    def test_it_is_served_as_plain_text(self):
        self.assertEqual(self.resp.status_code, 200)
        self.assertIn("text/plain", self.resp.headers["Content-Type"])

    def test_it_points_at_the_absolute_sitemap(self):
        self.assertRegex(self.body, r"(?m)^Sitemap: https://[^\s]+/sitemap\.xml$")

    def test_it_offers_the_door_and_closes_the_interior(self):
        self.assertIn("Allow: /$", self.body)
        self.assertIn("Allow: /signup", self.body)
        for path in ("/quiz/", "/admin/", "/stats", "/account", "/results/"):
            self.assertIn("Disallow: %s" % path, self.body,
                          "%s must stay out of an index" % path)


class TestSitemap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as module
        cls.resp = module.app.test_client().get("/sitemap.xml")
        cls.body = cls.resp.get_data(as_text=True)
        cls.root = ET.fromstring(cls.body)
        cls.locs = [el.text for el in cls.root.iter(SITEMAP_NS + "loc")]

    def test_it_is_valid_xml_with_the_right_content_type(self):
        self.assertEqual(self.resp.status_code, 200)
        self.assertIn("xml", self.resp.headers["Content-Type"])

    def test_every_url_is_absolute_and_public(self):
        self.assertTrue(self.locs)
        for loc in self.locs:
            self.assertTrue(loc.startswith("https://"), loc)
        joined = " ".join(self.locs)
        self.assertTrue(joined.rstrip("/").endswith("solutions") or "fcle.mu2.solutions" in joined)
        self.assertIn("https://fcle.mu2.solutions/", joined)

    def test_it_never_offers_a_student_page(self):
        joined = " ".join(self.locs)
        for private in ("/quiz/", "/account", "/stats", "/admin", "/results/", "/registered"):
            self.assertNotIn(private, joined, "%s must not be in the sitemap" % private)

    def test_lastmod_is_a_date(self):
        for el in self.root.iter(SITEMAP_NS + "lastmod"):
            self.assertRegex(el.text or "", r"^\d{4}-\d{2}-\d{2}$")

    def test_lastmod_is_not_stale(self):
        """It must never claim the site is older than the files that build it.

        The first shipped version read MAX(created_at) from the bank and reported
        2026-09-13 while the bank had been rebuilt and the page changed since.
        """
        from datetime import datetime
        bank = os.path.join(ROOT, "data", "fcle.db")
        landing = os.path.join(ROOT, "templates", "landing.html")
        today = datetime.utcnow().date().isoformat()
        newest = max(datetime.utcfromtimestamp(os.path.getmtime(p)).date().isoformat()
                     for p in (bank, landing))
        dates = {el.text for el in self.root.iter(SITEMAP_NS + "lastmod")}
        self.assertTrue(dates)
        for value in dates:
            self.assertLessEqual(value, today, "lastmod %s is in the future" % value)
            if newest <= today:      # only meaningful when the clock is not skewed
                self.assertGreaterEqual(value, newest,
                                        "lastmod %s is older than the newest source file" % value)


class TestLandingHead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as module
        cls.client = module.app.test_client()
        html = cls.client.get("/").get_data(as_text=True)
        cls.html = html
        cls.head = html.split("</head>")[0]

    def _content(self, pattern):
        m = re.search(pattern, self.head, re.I | re.S)
        return m.group(1) if m else None

    def test_canonical_is_absolute(self):
        self.assertEqual(self._content(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)'),
                         "https://fcle.mu2.solutions/")

    def test_it_is_indexable_on_purpose(self):
        self.assertEqual(self._content(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)'),
                         "index, follow")

    def test_open_graph_block_is_complete_and_absolute(self):
        for prop in ("og:type", "og:site_name", "og:url", "og:title",
                     "og:description", "og:image"):
            self.assertIsNotNone(
                self._content(r'<meta[^>]+property=["\']%s["\'][^>]*content=["\']([^"\']+)' % prop),
                "missing %s" % prop)
        self.assertTrue(self._content(r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)')
                        .startswith("https://"))
        self.assertEqual(self._content(r'<meta[^>]+property=["\']og:image:width["\'][^>]*content=["\']([^"\']+)'), "1200")
        self.assertEqual(self._content(r'<meta[^>]+property=["\']og:image:height["\'][^>]*content=["\']([^"\']+)'), "630")

    def test_twitter_card_is_present(self):
        self.assertEqual(self._content(r'<meta[^>]+name=["\']twitter:card["\'][^>]*content=["\']([^"\']+)'),
                         "summary_large_image")

    def test_the_og_copy_is_the_approved_copy_verbatim(self):
        """No new claims and no new numbers may enter through a share tag."""
        title = self._content(r"<title>([^<]*)</title>")
        desc = self._content(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']+)')
        self.assertEqual(self._content(r'<meta[^>]+property=["\']og:title["\'][^>]*content=["\']([^"\']+)'), title)
        self.assertEqual(self._content(r'<meta[^>]+property=["\']og:description["\'][^>]*content=["\']([^"\']+)'), desc)

    def test_no_claim_the_product_cannot_make(self):
        self.assertNotIn("real practice questions", self.head.lower())
        self.assertNotIn("official", self.head.lower())
        self.assertIn("FCLE-style", self.head)

    def test_any_question_count_in_the_head_is_a_floor(self):
        for count in re.findall(r"\b\d[\d,]{2,}\s*(?:\+\s*)?questions", self.head, re.I):
            self.assertIn("+", count, "%r is a hard number; use a floor" % count)


class TestStructuredData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as module
        cls.html = module.app.test_client().get("/").get_data(as_text=True)
        m = re.search(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', cls.html, re.S | re.I)
        cls.raw = m.group(1) if m else ""
        cls.data = json.loads(cls.raw) if cls.raw else {}
        cls.graph = {node["@type"]: node for node in cls.data.get("@graph", [])}

    def test_it_is_valid_json(self):
        self.assertTrue(self.raw, "landing.html carries no ld+json block")
        self.assertIn("@graph", self.data)

    def test_the_app_is_described_as_a_free_web_application(self):
        app_node = self.graph.get("WebApplication", {})
        self.assertEqual(app_node.get("name"), "Sabal")
        self.assertEqual(app_node.get("url"), "https://fcle.mu2.solutions/")
        self.assertEqual(app_node.get("offers", {}).get("price"), "0")
        self.assertEqual(app_node.get("offers", {}).get("priceCurrency"), "USD")
        self.assertIn("Mu2 Solutions", str(app_node.get("publisher", {})))

    def test_every_faq_question_is_visible_on_the_page(self):
        faq = self.graph.get("FAQPage", {})
        questions = [q["name"] for q in faq.get("mainEntity", [])]
        self.assertGreaterEqual(len(questions), 3)
        visible = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", self.html))
        for q in questions:
            self.assertIn(q, visible, "%r is in the structured data but not on the page" % q)

    def test_answers_are_plain_text(self):
        for q in self.graph.get("FAQPage", {}).get("mainEntity", []):
            text = q["acceptedAnswer"]["text"]
            self.assertNotRegex(text, r"<[a-z/]", "structured-data answers must be plain text")


class TestOgImage(unittest.TestCase):
    def test_the_share_image_exists_at_the_social_card_size(self):
        self.assertTrue(os.path.exists(OG_IMAGE), "og:image must ship in static/img/")
        self.assertEqual(png_size(OG_IMAGE), (1200, 630))

    def test_the_og_url_matches_the_shipped_file(self):
        with open(LANDING, encoding="utf-8") as fh:
            landing = fh.read()
        self.assertIn("/static/img/sabal-og-card.png", landing)
        self.assertIn("sabal-og-card.png", os.listdir(os.path.join(ROOT, "static", "img")))


class TestNothingElseRegressed(unittest.TestCase):
    """The crawl routes are unauthenticated by design; they must leak nothing."""

    @classmethod
    def setUpClass(cls):
        import app as module
        cls.client = module.app.test_client()

    def test_the_crawl_routes_need_no_session(self):
        for path in ("/robots.txt", "/sitemap.xml"):
            self.assertEqual(self.client.get(path).status_code, 200)

    def test_the_sitemap_does_not_expose_the_admin_keys(self):
        body = self.client.get("/sitemap.xml").get_data(as_text=True)
        for secret in ("PILOT_ADMIN_KEY", "PILOT_BYPASS_KEY", "RESEND", "FLASK_SECRET"):
            self.assertNotIn(secret, body)


class TestLicenceIsStatedOnTheSite(unittest.TestCase):
    """OER Commons marks this Required: the site itself must state licensing/usage rights.

    Before 2026-10-14 the licence lived only in the repo (`LICENSE`,
    `LICENSE-CONTENT`, `ATTRIBUTION.md`): a student reading "free to use, adapt
    and share" was never told the terms, and an OER Commons submission that fails
    a Required criterion is disqualified automatically.
    """

    @classmethod
    def setUpClass(cls):
        import app as module
        cls.html = module.app.test_client().get("/").get_data(as_text=True)

    def test_the_page_names_both_licences_and_links_them(self):
        for token in ("CC BY-NC-SA 4.0", "Apache-2.0",
                      "creativecommons.org/licenses/by-nc-sa/4.0",
                      "apache.org/licenses/LICENSE-2.0"):
            self.assertIn(token, self.html, "%r must be stated on the site" % token)

    def test_it_states_what_the_app_is_not(self):
        self.assertIn("Not affiliated with the Florida Department of Education", self.html)

    def test_the_structured_data_carries_the_same_licence(self):
        m = re.search(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', self.html, re.S | re.I)
        data = json.loads(m.group(1))
        node = [n for n in data["@graph"] if n["@type"] == "WebApplication"][0]
        self.assertEqual(node.get("license"), "https://creativecommons.org/licenses/by-nc-sa/4.0/")


class TestThePageSaysWhatStudentsSearch(unittest.TestCase):
    """The ranking gap: competitors own "Florida Civic Literacy Exam practice test"
    and the page never used the phrase at all. Approved by Mister K 2026-10-15."""

    @classmethod
    def setUpClass(cls):
        import app as module
        cls.html = module.app.test_client().get("/").get_data(as_text=True)
        cls.low = cls.html.lower()

    def test_the_exam_is_named_in_full_on_the_page(self):
        self.assertGreaterEqual(self.low.count("florida civic literacy exam"), 2,
                                "the exam name must appear more than once")

    def test_the_title_leads_with_what_students_type(self):
        title = re.search(r"<title>([^<]*)</title>", self.html).group(1)
        self.assertTrue(title.startswith("FCLE Practice Test"), title)
        self.assertIn("Florida Civic Literacy Exam", title)

    def test_the_hero_carries_the_lede_sentence(self):
        self.assertIn("Free FCLE practice test questions for the Florida Civic Literacy Exam.",
                      self.html)

    def test_the_two_new_faqs_are_visible(self):
        for question in ("Is there a free FCLE practice test?", "How many questions are on the FCLE?"):
            self.assertIn(question, self.html)

    def test_the_faq_answer_states_the_publicly_documented_exam_facts(self):
        self.assertIn("80 multiple-choice questions", self.html)
        self.assertIn("48 correct answers to pass", self.html)


if __name__ == "__main__":
    unittest.main()
