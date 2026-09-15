# FCLE Study Buddy — Project Status

**Last Updated:** 2026-09-06 by Ann-E
**Project Path:** `/home/muatasr/.nanobot/workspace/fcle-study-app/`
**Current Phase:** Pre-deployment (feature-complete MVP) — ORDER-faithful auth live in code (ee5ef9f), not yet deployed

---

## What Is This

A web-based study app for the Florida Civic Literacy Exam (FCLE). Students practice multiple-choice questions across 4 civic literacy domains with adaptive feedback modes (quiz, hint, teach). Tracks progress, mastery, and spaced review.

---

## Database Status

**Question DB:** `data/fcle.db` — 2,175 questions, zero nulls, zero duplicates

| Domain | Count |
|--------|-------|
| D1 — American Democracy | 675 |
| D2 — U.S. Constitution | 496 |
| D3 — Federal Government | 503 |
| D4 — Rights & Responsibilities | 501 |

- All 2,175 questions have `wrong_explanations` populated (per-choice "why this is wrong" text)
- All explanations verified clean (68 mismatched explanations fixed May 14)
- Question types: MCQ with A/B/C/D, distractors grounded in real misconceptions

**User Progress DB:** `data/user_progress.db`
- Tables: users, quiz_sessions, answers, topic_mastery, review_queue, diagnostic_baselines, tutor_messages, active_quizzes
- **Auth model (Sep 6, 2026): registered users ONLY — no anonymous accounts.** 141 legacy anonymous rows + child data purged; DB is a clean slate (0 users at purge). Every user has a 32-char `access_token` (dashboard link).

---

## App Stack

| Component | Details |
|-----------|---------|
| Backend | Flask, `app.py` (~1,500 lines) |
| Templates | 22 HTML templates in `templates/` |
| CSS | `static/css/fcle.css` + `app.css` (Template A navy/gold) |
| Port | 5002, host 0.0.0.0, debug=False |
| Dependencies | Flask, python3 stdlib, requests — no heavy frameworks |

---

## Feature Checklist

- [x] 4-domain + mixed review quiz mode
- [x] 10/25/50 question count options
- [x] 3 confidence-based feedback modes (quiz / hint / teach)
- [x] Per-choice explanation breakdown (added May 14)
  - Each answer shown as a card with letter badge, correct/wrong indicator, and individual explanation
  - Wrong answers show strikethrough with "why this is wrong" text
  - Teach mode shows all 4 choices; quiz/hint modes show only relevant ones
- [x] Spaced repetition review queue
- [x] Topic mastery tracking
- [x] Diagnostic baseline quiz
- [x] User accounts — **ORDER-faithful: email + display name registration, NO password; personal dashboard link (`/?token=...`) is the login**
- [x] Stats dashboard
- [x] Settings page
- [x] Clean navbar (trimmed to brand + login/logout only, May 14)
- [x] Editorial print-style CSS (non-AI-slop design)
- [x] Cloudflare tunnel tested (May 14 — accessible from external network)

---

## Recent Changes

### Sep 6, 2026 — ORDER-faithful auth (registered-only, no anonymous users) — commit `ee5ef9f`

Mister K directive: no anonymous users; visitors must register, then get a personal dashboard link automatically (ORDER-portal model). Full rebuild:

- **Anonymous auto-create removed.** `/` redirects anonymous → `/login?next=/`; no silent user rows on any visit.
- **Registration = email + display name only (no password).** New account gets a 32-char `access_token`; post-registration `/registered` handoff page shows the personal dashboard link (`/?token=...`) with Copy Link + Go to My Dashboard CTA.
- **Login = email only** (no password): returning users re-receive their dashboard link.
- **Token resolution:** session first, then `?token=` query param, then `access_token` cookie — ORDER style. Stale/anonymous session ids are dropped, never honored.
- **Tutor routes gated:** `/tutor`, `/tutor/chat`, `/tutor/history` now require login.
- **Schema:** `users.access_token` + unique index; `db.init_db()` runs at import so gunicorn/wsgi also migrate (not just `python3 app.py`).
- **Purged 141 legacy anonymous users + child data** (approved by Mister K) — DB clean at 0 users.
- **Template bug fixes:** `current_user` is a dict so `.is_authenticated` was always falsy (Settings showed logged-out branch; onboarding redirect dead) — fixed to dict-safe checks; added missing `/settings/exam-date` POST route; new users get `onboarding_done=1` so registration lands straight on the dashboard.
- **Email leg:** `_try_email_dashboard_link()` sends the link only when `SMTP_HOST`/`SMTP_PORT`/`SMTP_FROM`/`SMTP_USER`/`SMTP_PASS` env vars exist. No SMTP creds configured yet (Mister K will add at deploy). On-screen link is the only delivery channel until then; the page only says "emailed" when a send actually succeeds.

### May 14, 2026

1. **Per-choice explanation breakdown** — replaced wall-of-text explanation with individual answer cards showing why each choice is right or wrong. Uses `wrong_explanations` data from DB.
2. **Fixed 68 mismatched explanations** — questions where explanation didn't match correct_answer; all corrected.
3. **Navbar cleanup** — removed Home/Stats/Settings links from top navbar (they're in the footer); kept only brand name + login/logout.
4. **Tunnel tested** — cloudflared quick tunnel confirmed app works over public internet.

---

## Remaining Roadmap

- [ ] **PWA support** — service worker + manifest.json for install-to-homescreen
- [ ] **Cloud deployment** — move off dev server to production hosting
- [ ] **Mobile polish** — verify responsive layout on small screens
- [ ] **Data cleanup** — archive generation scripts in `data/` that are no longer needed
- [ ] **Production WSGI** — swap Flask dev server for gunicorn/waitress before deployment

---

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application (routes, quiz logic, auth) |
| `kb.py` | Question loading from SQLite |
| `db.py` | User progress DB operations |
| `templates/base.html` | Base layout (navbar, footer, nav drawer) |
| `templates/registered.html` | Post-registration / returning-user handoff — shows the personal dashboard link (`/?token=...`), Copy Link + Go to My Dashboard (added Sep 6, 2026) |
| `templates/login.html` / `signup.html` | Email-only auth pages (no password) |
| `templates/quiz.html` | Quiz UI + feedback breakdown |
| `templates/results.html` | Quiz results summary |
| `static/css/fcle.css` | Main stylesheet (editorial style) |
| `data/fcle.db` | Question database (2,175 questions) |
| `data/user_progress.db` | User accounts + progress tracking |
