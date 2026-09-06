# FCLE Study Buddy — Project Status

**Last Updated:** 2026-05-14 by Ann-E
**Project Path:** `/home/muatasr/.nanobot/workspace/fcle-study-app/`
**Current Phase:** Pre-deployment (feature-complete MVP)

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
- Tables: users, quiz_sessions, answers, topic_mastery, review_queue, diagnostic_baselines

---

## App Stack

| Component | Details |
|-----------|---------|
| Backend | Flask, `app.py` (1,031 lines) |
| Templates | 16 HTML templates in `templates/` |
| CSS | `static/css/fcle.css` (editorial/print style) + `themes.css` |
| Port | 5002, host 0.0.0.0, debug=False |
| Dependencies | Flask, python3 stdlib — no heavy frameworks |

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
- [x] User accounts (login/register) with progress persistence
- [x] Stats dashboard
- [x] Settings page
- [x] Clean navbar (trimmed to brand + login/logout only, May 14)
- [x] Editorial print-style CSS (non-AI-slop design)
- [x] Cloudflare tunnel tested (May 14 — accessible from external network)

---

## Recent Changes (May 14, 2026)

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
| `templates/quiz.html` | Quiz UI + feedback breakdown |
| `templates/results.html` | Quiz results summary |
| `static/css/fcle.css` | Main stylesheet (editorial style) |
| `data/fcle.db` | Question database (2,175 questions) |
| `data/user_progress.db` | User accounts + progress tracking |
