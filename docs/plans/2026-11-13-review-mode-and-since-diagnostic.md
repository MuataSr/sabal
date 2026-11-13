# Sabal: serve the review queue, and show the since-diagnostic comparison

> **For Hermes:** implement task by task, TDD, commit after each task. Deploy is a separate gate.

**Goal:** make two things the DB already knows visible to students: the spaced-repetition
queue (written on every answer, never read by any page) and the signup diagnostic baseline
(written once, shown once, never compared).

**Corrected premise (verified 2026-11-13 against prod):** `review_queue` is NOT broken. Kelsey
had 35 answers on 35 distinct questions and 35 rows with `times_correct=0`, which is exactly
right for one attempt per card. User 87 has 120 distinct questions, 7 repeated, and 6 rows
with `times_correct>0`. The write path works. The defect is that **nothing reads the table**:
`grep review_queue app.py` returns the write call and nothing else, while 165 rows across five
users are already due. Same shape for baselines: `db.get_diagnostic_baseline()` is defined and
called from nowhere.

**Architecture:** no new tables, no new columns, no new quiz engine. Review rides the existing
`/quiz/<slug>` flow as the slug `review`, so `quiz.html`, `quiz_answer()` and `results.html`
work unchanged. The comparison is computed at request time on `/stats` from
`diagnostic_baselines` plus the `answers` table (not `topic_mastery`, which files mixed-quiz
answers under `domain='mixed'` and would silently drop them).

**Tech stack:** Flask 3.1.1, SQLite, Jinja, pytest (`venv/bin/python -m pytest`).

---

## Scope, and what this plan deliberately does not do

Not building: a review scheduler page, per-card intervals the student can see, notification or
email reminders, a "review streak", a new dashboard section, changes to the SM-2 maths, or a
fix for `mixed` answers landing in `topic_mastery.domain='mixed'` (that is a data-behavior change
for existing users and needs its own decision).

Two known quirks left alone, named so nobody rediscovers them:
- A NEW review row is inserted with `times_correct=0` even when the first answer was correct.
  Fixing it changes the first interval for every card; out of scope here.
- A correct answer at confidence 1 does `interval = max(interval, 1.0)`, so a guessed-right card
  never advances. That is the SM-2 variant working as written, not a bug.

---

## Task 1: two read helpers in `db.py`

**Objective:** fetch due question ids and count them.

**Files:**
- Modify: `db.py` (after `update_review_queue`, around line 664)
- Test: `tests/test_review_mode.py` (new)

**Step 1: write the failing test**

Create `tests/test_review_mode.py`:

```python
"""Review mode: the SRS queue is served, not just written."""

import os
import shutil
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta

from tests import fixtures


class ReviewDbTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app as app_module
        cls.mod = app_module

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sabal-review-")
        self.mod.db.DB_PATH = os.path.join(self.tmp, "user_progress.db")
        self.mod.db.init_db()
        self.mod.db.init_active_quizzes_table()
        self.mod.db.init_diagnostic_table()
        self.uid = self.mod.db.create_user(email="r@example.com", display_name="R")["id"]

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

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

    def test_due_ids_exclude_cards_scheduled_for_the_future(self):
        a, b, c = self._real_question_ids(3)
        self._seed_review(a, -1)   # due yesterday
        self._seed_review(b, -5)   # due five days ago
        self._seed_review(c, +3)   # not due for three days
        ids = self.mod.db.get_due_review_ids(self.uid)
        self.assertEqual(len(ids), 2)
        self.assertEqual(self.mod.db.count_due_reviews(self.uid), 2)

    def test_due_ids_are_capped(self):
        for qid in self._real_question_ids(25):
            self._seed_review(qid, -1)
        self.assertEqual(len(self.mod.db.get_due_review_ids(self.uid, limit=20)), 20)
        self.assertEqual(self.mod.db.count_due_reviews(self.uid), 25)
```

**Step 2: run it, expect failure**

```
cd ~/sabal && venv/bin/python -m pytest tests/test_review_mode.py -q
```
Expected: `AttributeError: module 'db' has no attribute 'get_due_review_ids'`.

**Step 3: implement**

```python
def get_due_review_ids(user_id, limit=20):
    """Question ids whose next_review has passed, soonest first."""
    now_iso = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT question_id FROM review_queue WHERE user_id=? AND next_review<=?"
            " ORDER BY next_review LIMIT ?",
            (user_id, now_iso, int(limit)),
        ).fetchall()
        return [r["question_id"] for r in rows]


def count_due_reviews(user_id):
    now_iso = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM review_queue WHERE user_id=? AND next_review<=?",
            (user_id, now_iso),
        ).fetchone()
        return row["c"] or 0
```

**Step 4: run again**

```
cd ~/sabal && venv/bin/python -m pytest tests/test_review_mode.py -q
```
Expected: `2 passed`.

**Step 5: commit**

```bash
cd ~/sabal && git add db.py tests/test_review_mode.py && git commit -m "feat: read due review cards from the SRS queue"
```

---

## Task 2: `/quiz/review` runs the existing quiz flow

**Objective:** a student can start and finish a review session.

**Files:**
- Modify: `app.py` (`quiz_start` ~423, `quiz_question` ~492, `quiz_answer` ~604, `results` ~713)
- Test: `tests/test_review_mode.py`

**Step 1: write the failing tests** (append to the class in Task 1)

```python
    def _login(self):
        c = self.mod.app.test_client()
        with c.session_transaction() as s:
            s["user_id"] = self.uid
        return c

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
        loc = c.get("/quiz/review").headers["Location"]
        quiz_id = loc.split("/")[3]
        quiz = self.mod.db.load_quiz(quiz_id)
        q = quiz["questions"][0]
        before = self.mod.db._get_conn().execute(
            "SELECT interval_days FROM review_queue WHERE user_id=? AND question_id=?",
            (self.uid, q["id"]),
        ).fetchone()["interval_days"]

        c.post(f"/quiz/review/{quiz_id}/0/answer",
               data={"selected": q["correct_answer"], "confidence": 3})

        row = self.mod.db._get_conn().execute(
            "SELECT interval_days, times_correct, next_review FROM review_queue"
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
```

**Step 2: run, expect failure** (`404` on `/quiz/review`, since the slug falls through to
`_get_domain_info` and redirects).

**Step 3: implement**

3a. Display-name helper, next to `_get_domain_info`:

```python
_QUIZ_DISPLAY_NAMES = {"mixed": "Mixed Review", "review": "Review"}


def _quiz_display_name(domain_slug):
    info = _get_domain_info(domain_slug)
    return _QUIZ_DISPLAY_NAMES.get(domain_slug) or (info or {}).get("name") or domain_slug
```

3b. Replace the three duplicated blocks with one call each:

```python
    domain_name = _quiz_display_name(domain_slug)
```
at `quiz_question` (lines 492-495), `quiz_answer` (604-607), `results` (713-716).

3c. Branch in `quiz_start` right after the `mixed` branch:

```python
    if domain_slug == "review":
        return quiz_start_review()
```

3d. New function after `quiz_start_mixed`:

```python
def quiz_start_review():
    """Serve cards the SRS says are due, through the normal quiz flow."""
    user_id = session["user_id"]
    ids = db.get_due_review_ids(user_id, limit=20)
    # A quarantined question keeps its review row, so skip ids the bank no longer has.
    questions = [q for q in (kb.get_shaped_question_by_id(i) for i in ids) if q]
    if not questions:
        flash("Nothing is due for review right now. Answer a few new questions and they will come back here.")
        return redirect("/stats")

    quiz_id = uuid.uuid4().hex[:12]
    db.save_quiz(quiz_id, {
        "user_id": user_id,
        "domain": "review",
        "questions": questions,
        "current_index": 0,
        "answers": [],
        "started_at": datetime.now().isoformat(),
        "session_id": None,
    })
    return redirect(f"/quiz/review/{quiz_id}/0")
```

3e. In `quiz_answer`, put mastery and the SRS row in the question's real domain:

```python
    # "review" is a route slug, not a domain: a review answer belongs to the domain
    # of the question it came from, or topic_mastery grows a phantom domain.
    mastery_domain = quiz["domain"]
    if mastery_domain == "review":
        mastery_domain = next(
            (s for s, i in _DOMAIN_GETTERS.items() if i["id"] == question.get("domain_id")),
            mastery_domain,
        )
```
use `mastery_domain` in `db.update_topic_mastery(...)` and as the `domain=` argument to
`db.update_review_queue(...)`. Leave `mixed` behaviour exactly as it is.

**Step 4: run**

```
cd ~/sabal && venv/bin/python -m pytest tests/test_review_mode.py -q
```
Expected: `6 passed`.

**Step 5: commit**

```bash
cd ~/sabal && git add app.py tests/test_review_mode.py && git commit -m "feat: review mode serves due SRS cards through the quiz flow"
```

---

## Task 3: due count on `/stats`

**Objective:** the student can see there is something waiting and start it.

**Files:**
- Modify: `app.py` (`stats()` ~734), `templates/stats.html`
- Test: `tests/test_review_mode.py`

**Step 1: failing test**

```python
    def test_stats_shows_the_due_count_and_a_way_in(self):
        self._seed_review(self._real_question_ids(1)[0], -1)
        c = self._login()
        html = c.get("/stats").get_data(as_text=True)
        self.assertIn("due for review", html)
        self.assertIn('href="/quiz/review"', html)
```

**Step 2: run, expect failure.**

**Step 3: implement**

In `stats()`, add before the render:

```python
    due_reviews = db.count_due_reviews(user_id)
```
and pass `due_reviews=due_reviews` to `render_template`.

In `templates/stats.html`, after the readiness/streak block and before `By Domain`:

```html
  {% if due_reviews %}
  <div style="margin-top: 18px; padding: 16px 18px; border: 1px solid var(--border); border-radius: 12px;">
    <div style="font-weight: 700; font-family: var(--font-heading);">
      {{ due_reviews }} question{{ "" if due_reviews == 1 else "s" }} due for review
    </div>
    <div class="text-muted" style="font-size: 0.85rem; margin: 4px 0 12px;">
      Ones you have already seen. Spacing them out is what makes them stick.
    </div>
    <a href="/quiz/review" class="btn-a">Review now</a>
  </div>
  {% endif %}
```

If `.btn-a` is not available inside `stats.html`, use the same inline anchor styling the file
already uses; do not invent a class.

**Step 4: run, commit**

```bash
cd ~/sabal && venv/bin/python -m pytest tests/test_review_mode.py -q && \
git add app.py templates/stats.html tests/test_review_mode.py && \
git commit -m "feat: show the due review count on the progress page"
```

---

## Task 4: since-diagnostic comparison on `/stats`

**Objective:** one honest before/after: the signup diagnostic against current unassisted practice.

**Files:**
- Modify: `app.py` (`stats()` and one helper), `templates/stats.html`
- Test: `tests/test_review_mode.py`

**Design rule:** compare raw accuracy to raw accuracy. `overall_readiness` is confidence- and
decay-weighted; putting a weighted 22% next to a raw diagnostic 60% would read as a regression
that did not happen. Baseline and practice are both raw counts.

**As shipped:** practice is read from `answers` (`get_answer_records`) joined to the bank for
domain/topic, not from `topic_mastery`. Reason found while verifying against Kelsey's record:
`topic_mastery` files every mixed-quiz answer under `domain='mixed'`, so it held 15 of her 35
answers and the card read 67% instead of 71%. `answers` holds all 35 and the diagnostic never
writes there. Per-topic rows skip topics she had already aced at signup (>= 80%).

**Step 1: failing test**

```python
    def test_since_diagnostic_compares_raw_to_raw(self):
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.mod.db.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO diagnostic_baselines (user_id, domain, topic, total, correct, pct, taken_at)"
                " VALUES (?, 'landmark-impact', 'Civil Rights Act 1964', 1, 0, 0.0, ?)", (self.uid, now))
            conn.execute(
                "INSERT INTO diagnostic_baselines (user_id, domain, topic, total, correct, pct, taken_at)"
                " VALUES (?, 'us-constitution', 'Federalism', 1, 1, 100.0, ?)", (self.uid, now))
            conn.execute(
                "INSERT INTO topic_mastery (user_id, domain, topic, total_attempted, total_correct)"
                " VALUES (?, 'landmark-impact', 'Civil Rights Act 1964', 5, 3)", (self.uid,))
            conn.execute(
                "INSERT INTO topic_mastery (user_id, domain, topic, total_attempted, total_correct)"
                " VALUES (?, 'us-constitution', 'Federalism', 4, 4)", (self.uid,))
        c = self._login()
        html = c.get("/stats").get_data(as_text=True)
        self.assertIn("Since your diagnostic", html)
        # Tie each number to its own label: another 50% elsewhere on the page must not pass this.
        self.assertRegex(html, r"Diagnostic on \S+: <strong>50%</strong>\s+of 2 questions")
        self.assertRegex(html, r"Unassisted practice since: <strong>78%</strong>\s+of 9 answers")
```

**Step 2: run, expect failure.**

**Step 3: implement**

In `stats()`, inside the existing `for slug in _DOMAIN_GETTERS` loop, collect the topic map so
the helper does not re-query four domains:

```python
    topic_now = {}
    ...
    for t in d_stats.get("topics", []):
        topic_now[(slug, t["topic"])] = (t["correct"], t["total"])
```

After the loop:

```python
    since_diagnostic = _since_diagnostic(user_id, topic_now)
```
pass it to the template.

Helper, near `_weak_areas`:

```python
def _since_diagnostic(user_id, topic_now):
    """Signup diagnostic vs current unassisted practice. Raw counts on both sides.

    Readiness is confidence- and decay-weighted, so it is not comparable to a raw
    diagnostic percentage; mixing them would show a regression that did not happen.
    """
    baselines = db.get_diagnostic_baseline(user_id)
    if not baselines:
        return None
    b_total = sum(b["total"] for b in baselines)
    b_correct = sum(b["correct"] for b in baselines)
    if not b_total:
        return None

    rows = []
    for b in baselines:
        correct, total = topic_now.get((b["domain"], b["topic"]), (0, 0))
        if total:
            rows.append({
                "topic": b["topic"],
                "before": int(round(b["pct"])),
                "after": int(round(100.0 * correct / total)),
                "attempts": total,
            })
    rows.sort(key=lambda r: (r["before"], -r["attempts"]))

    attempted = sum(t for _, t in topic_now.values())
    earned = sum(c for c, _ in topic_now.values())
    return {
        "taken_on": max(b["taken_at"] for b in baselines)[:10],
        "before_pct": int(round(100.0 * b_correct / b_total)),
        "before_total": b_total,
        "after_pct": int(round(100.0 * earned / attempted)) if attempted else None,
        "after_total": attempted,
        "topics": rows[:6],
    }
```

Template block, directly under the review block:

```html
  {% if since_diagnostic %}
  <div style="margin-top: 18px; padding: 16px 18px; border: 1px solid var(--border); border-radius: 12px;">
    <h2 class="section-title" style="margin-bottom: 6px;">Since your diagnostic</h2>
    <div class="text-muted" style="font-size: 0.85rem; margin-bottom: 10px;">
      Diagnostic on {{ since_diagnostic.taken_on }}: <strong>{{ since_diagnostic.before_pct }}%</strong>
      of {{ since_diagnostic.before_total }} questions.
      {% if since_diagnostic.after_pct is not none %}
      Unassisted practice since: <strong>{{ since_diagnostic.after_pct }}%</strong>
      of {{ since_diagnostic.after_total }} answers.
      {% endif %}
    </div>
    {% for t in since_diagnostic.topics %}
    <div style="display: flex; align-items: center; gap: 8px; padding: 6px 0; border-top: 1px solid var(--border); font-size: 0.84rem;">
      <span style="flex: 1;">{{ t.topic }}</span>
      <span class="text-muted">{{ t.before }}%</span>
      <span class="text-muted">-></span>
      <span style="font-weight: 600;">{{ t.after }}%</span>
      <span class="text-muted">({{ t.attempts }})</span>
    </div>
    {% endfor %}
    <div class="text-muted" style="font-size: 0.78rem; margin-top: 10px;">
      Topics you were weakest on at signup. Not a score prediction.
    </div>
  </div>
  {% endif %}
```

**Step 4: full suite, three times** (the bank samples randomly)

```
cd ~/sabal && for i in 1 2 3; do venv/bin/python -m pytest tests/ -q --tb=short 2>&1 | tail -3; done
```
Expected: 287-ish passed each run, no failures.

**Step 5: commit**

```bash
cd ~/sabal && git add app.py templates/stats.html tests/test_review_mode.py && \
git commit -m "feat: compare the signup diagnostic with current practice on the progress page"
```

---

## Verification on real data (read-only, no deploy)

Point a preview server at a COPY of the prod runtime DB and read Kelsey's `/stats` as her, so
the card is checked against the numbers that started this work:

```bash
# on the OG Rig, copy the runtime DB down (never the content DB)
scp root@142.93.201.242:/opt/fcle-study-app/data/user_progress.db ~/sabal/data/preview_progress.db
# then, from ~/sabal: FLASK_SECRET from prod env, db.DB_PATH -> the copy, fuser -k 5055/tcp
```
Expected on her page: `60%` of 20 at signup, `71%` of 35 since, and Civil Rights Act 1964
`0% -> 40%` with 5 attempts.

## Execution order

1. Task 1 (db reads) - nothing depends on it yet, 5 minutes.
2. Task 2 (review route) - depends on Task 1.
3. Task 3 (stats card) - depends on Task 1 only.
4. Task 4 (comparison) - independent of 1-3; touches the same file as 3, so run after it.

## Deploy (separate gate, needs your yes)

`git push origin main`, then on the droplet `/opt/fcle-study-app`: `git pull --ff-only`,
restart the service, then verify as a signed-in session that `/stats` renders and
`/quiz/review` starts. No schema migration and no content DB change, so nothing to back up
beyond the standing runtime DB snapshot.
