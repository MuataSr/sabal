# FCLE Study App — Formal Build Plan

**Created:** May 11, 2026
**Status:** Phase 0 complete — question bank done (2,175 questions)
**Next:** Phase 1 — Flask App Build

---

## Target Audience

Florida college students who must pass the FCLE to graduate. Many are first-gen, working part-time, studying between shifts or classes. They've tried Quizlet decks and free YouTube tests — nothing treats civic literacy as a serious study discipline. They don't need gamification; they need **clarity, structure, and a real shot at passing**.

**Our edge:** Professional-grade OER that is free, open source, and better than the paid alternatives. David Tran philosophy — rich man's quality at a poor man's price.

---

## Existing Codebase (What We Have)

| Component | Lines | Status |
|-----------|-------|--------|
| `app.py` | 675 | ✅ Routes: auth, quiz flow, results, stats, settings |
| `db.py` | 453 | ✅ Schema: users, quiz_sessions, answers, topic_mastery, review_queue |
| `kb.py` | 185 | ✅ Question retrieval, domain helpers, mixed quiz distribution |
| `templates/` | 9 files | ✅ base, dashboard, quiz, results, stats, login/signup, onboarding, settings |
| `static/css/themes.css` | 1 file | ✅ Editorial design system (navy/cream/forest palette) |
| `data/fcle.db` | 2,175 Qs | ✅ All 4 domains, 308 with stimulus passages, 354 misconceptions, 315 key terms |
| `data/user_progress.db` | Schema ready | ✅ 5 tables, empty (no users yet) |

**What's already working:**
- Quiz flow (start → answer → next → results)
- Domain/topic/difficulty filtering
- Anonymous user creation (no signup required)
- Topic mastery tracking (per-topic accuracy)
- Review queue with spaced repetition fields (ease_factor, interval_days)
- Mixed-domain quiz distribution
- Editorial design system with Libre Baskerville + Source Sans 3

---

## Build Phases

### Phase 1: Core App Hardening (Days 1–2)

**Goal:** Make the existing skeleton into a working, testable app.

- [ ] **1.1** Audit existing routes end-to-end — run `flask run`, test every page, fix broken links
- [ ] **1.2** Verify kb.py reads correctly from fcle.db (domain IDs, stimulus passages, wrong_answers JSON)
- [ ] **1.3** Fix domain naming mismatch — PROJECT_BRIEF says "American Democracy / US Constitution / Founding Documents / Landmark Impact" but fcle.db domains may differ
- [ ] **1.4** Ensure onboarding flow works (anonymous user → exam date → target score → dashboard)
- [ ] **1.5** Test quiz flow: start quiz → answer questions → submit → see results → review wrong answers
- [ ] **1.6** Verify localStorage/session persistence — closing and reopening browser keeps progress

**Exit criteria:** App runs locally, full quiz cycle works, no 500 errors.

---

### Phase 2: Pre-Test Diagnostic (Day 3)

**Goal:** Personalized study plan before students start studying.

- [ ] **2.1** Build diagnostic quiz: 20 questions (5 per domain, mixed difficulty, shuffled)
- [ ] **2.2** No feedback during diagnostic — just answer, answer, answer
- [ ] **2.3** Results screen shows: per-domain score, per-topic score, strengths, weaknesses
- [ ] **2.4** Generate a recommended study order — weakest domain first, strongest last
- [ ] **2.5** Save diagnostic results as baseline — all future scores compare against this
- [ ] **2.6** "Skip diagnostic" option for returning users who already know their weak spots

**Why this matters:** No professional test prep skips diagnostics. It gives students direction and motivation ("I'm 85% in D4 but only 52% in D3 — let's fix that").

**Exit criteria:** New user takes diagnostic → sees personalized study plan → dashboard reflects baseline scores.

---

### Phase 3: Stimulus Literacy Training (Day 4)

**Goal:** Teach students how to read and analyze primary source passages — the #1 skill gap on the real FCLE.

- [ ] **3.1** Create a dedicated "Stimulus Practice" mode separate from quiz mode
- [ ] **3.2** Pull the 308 questions with stimulus passages into a filtered pool
- [ ] **3.3** Show the stimulus passage first with guided reading prompts:
  - "Who wrote this? When?"
  - "What is the author's main argument?"
  - "What constitutional principle does this relate to?"
- [ ] **3.4** Student answers the prompts (free text, not graded) → then sees the question + answers
- [ ] **3.5** After answering, show a breakdown: which part of the stimulus points to the correct answer
- [ ] **3.6** Track stimulus-specific accuracy separately from general quiz accuracy

**Why this matters:** Students don't fail FCLE because they don't know civics. They fail because they can't extract meaning from a Federalist Paper excerpt under time pressure. This mode is our differentiator — nobody offers this for free.

**Exit criteria:** Stimulus Practice mode works, 308 questions available, guided prompts show, post-answer breakdown links stimulus text to correct answer.

---

### Phase 4: Distractor Explanations (Day 5)

**Goal:** Every wrong answer gets an explanation — what separates us from Quizlet.

- [ ] **4.1** Generate wrong-answer explanations for all 2,175 questions (3 distractor explanations each = 6,525 explanations)
  - Use cloud LLM (Z.AI glm-5.1) via subagent batches
  - Format: "This is incorrect because [specific reason]. [Distractor] actually refers to [accurate detail]."
- [ ] **4.2** Add `wrong_explanations` JSON column to questions table
- [ ] **4.3** Update quiz results screen to show: correct explanation + all 3 wrong-answer explanations
- [ ] **4.4** Quality spot-check: sample 50 questions, verify distractor explanations are accurate and distinct

**Why this matters:** Right now we explain why the right answer is right. Professional products (Barron's, Kaplan) also explain why each wrong answer is wrong. This is the single highest-value content upgrade we can make.

**Content generation plan:** ~15 items per subagent batch, ~145 batches. Run in parallel spawns of 5.

**Exit criteria:** All 2,175 questions have 3 distractor explanations each, quiz results show them.

---

### Phase 5: Mastery Tracking & Smart Recommendations (Days 6–7)

**Goal:** Replace "here's your score" with "here's what to do next."

- [ ] **5.1** **Mastery bars per topic** — a topic is "mastered" only after 3+ correct answers across different sessions (not just once)
- [ ] **5.2** **Leitner system for flashcards** — upgrade the existing review_queue (which already has ease_factor and interval_days) into a proper 3-box Leitner system:
  - Box 1 (new/unseen): always shown
  - Box 2 (got right once): shown every other session
  - Box 3 (got right twice): shown every 4th session
  - Wrong answer: drops back to Box 1
- [ ] **5.3** **Smart recommendations** after each session:
  - "You missed 3/5 questions on Federalism. Here's a 5-question Federalism practice set."
  - "D3 History is your weakest domain (62%). Focus here next."
  - "You've mastered 8/12 topics in D4 — 4 remaining."
- [ ] **5.4** **Bookmark system** — star/unstar questions during quiz review for later study, even if answered correctly
- [ ] **5.5** **Study streak calendar** — GitHub-style contribution grid showing daily study activity

**Why this matters:** Spaced repetition + mastery tracking is the core of professional test prep. The existing review_queue schema already supports this — we're activating what's dormant.

**Exit criteria:** Mastery bars fill based on consistent correctness, Leitner boxes work, recommendations appear after sessions, bookmarks persist.

---

### Phase 6: Exam Simulation Mode (Day 8)

**Goal:** Practice under realistic conditions.

- [ ] **6.1** Build "Exam Sim" mode: 40 questions, all 4 domains mixed, no feedback until end
- [ ] **6.2** Optional timer (60 minutes, matching typical test center pace) — student chooses timed or untimed
- [ ] **6.3** Results page mirrors real FCLE score report: per-domain breakdown, pass/fail indicator (60% threshold)
- [ ] **6.4** Compare exam sim scores to diagnostic baseline — show improvement trajectory
- [ ] **6.5** After exam sim, auto-generate a practice set from missed questions

**Why this matters:** Students need to practice under pressure. A calm untimed quiz feels different from "I have 40 questions and I need 60%." This builds exam-day confidence.

**Exit criteria:** 40-question exam sim works, timed/untimed toggle, pass/fail shown, comparison to baseline.

---

### Phase 7: Interleaved Practice & Quickfire (Day 9)

**Goal:** Mixed-domain practice that builds cross-topic recall.

- [ ] **7.1** **Interleaved mode** — random questions from all domains, weighted toward weaker topics (pull more from low-mastery topics)
- [ ] **7.2** **Quickfire mode** — rapid-fire single-question popups (no multi-question session commitment). Good for 2-minute study moments between classes.
- [ ] **7.3** **Topic filter** — "I only want to practice Federalism questions" from any mode
- [ ] **7.4** **Difficulty filter** — "Give me only hard questions" for students close to exam day

**Why this matters:** Interleaving is backed by learning science. The real FCLE doesn't separate by topic. Quickfire respects that students study in fragments.

**Exit criteria:** Interleaved mode weights weak topics, quickfire works in under 10 seconds to start, topic/difficulty filters work.

---

### Phase 8: Accessibility & Mobile-First Polish (Day 10)

**Goal:** Every student can use this, regardless of device or ability.

- [ ] **8.1** **Mobile-first testing** — verify every page works on 375px viewport (iPhone SE) and 360px (Android)
- [ ] **8.2** **Touch targets** — all buttons minimum 44×44px, adequate spacing between options
- [ ] **8.3** **High contrast mode** — toggle in settings for low-vision users
- [ ] **8.4** **Font size controls** — small/medium/large in settings
- [ ] **8.5** **Screen reader basics** — proper ARIA labels on quiz options, landmark regions, alt text
- [ ] **8.6** **PWA manifest** — installable on home screen, app icon, splash screen
- [ ] **8.7** **Service worker** — cache question bank for full offline use (students on bad campus WiFi)
- [ ] **8.8** **Fast load** — lazy-load non-critical assets, defer Google Fonts

**Why this matters:** Our audience studies on phones between shifts. Offline support means the bus ride becomes study time. Accessibility isn't charity — it's professional quality.

**Exit criteria:** App works offline after first visit, installable as PWA, accessible with screen reader, mobile UI feels native.

---

### Phase 9: Deploy & Launch (Days 11–12)

**Goal:** Live and usable by real students.

- [ ] **9.1** Deploy to hosting (Digital Ocean or Render free tier)
- [ ] **9.2** SSL certificate, custom domain (fcle.mu2.solutions or similar)
- [ ] **9.3** Smoke test all features on production
- [ ] **9.4** Link from mu2.solutions homepage
- [ ] **9.5** Share with CCF testing center as pilot (Mister K's domain)
- [ ] **9.6** README with setup instructions for self-hosting (open source)

**Exit criteria:** App is live, accessible via URL, works on mobile, CCF has pilot access.

---

## Phase Summary

| Phase | Feature | Days | Priority |
|-------|---------|------|----------|
| 0 | Question Bank | Done | ✅ Complete |
| 1 | Core App Hardening | 1–2 | P0 — nothing works without this |
| 2 | Pre-Test Diagnostic | 3 | P1 — first thing new users see |
| 3 | Stimulus Literacy Training | 4 | P1 — our differentiator |
| 4 | Distractor Explanations | 5 | P1 — highest content value |
| 5 | Mastery Tracking & Smart Recs | 6–7 | P1 — core professional feature |
| 6 | Exam Simulation | 8 | P2 — important but not blocking |
| 7 | Interleaved & Quickfire | 9 | P2 — enhances existing modes |
| 8 | A11y & Mobile-First PWA | 10 | P2 — polish pass |
| 9 | Deploy & Launch | 11–12 | P3 — ship it |

**Total: 12 working days from today**

---

## Technical Notes

- **No new dependencies** — Flask, sqlite3, vanilla JS. Same stack as TEAS.
- **All inference is cloud-based** (Google AI Studio, free tier) for any AI features — nothing runs locally in production.
- **Distractor explanations** are the heaviest content lift (6,525 explanations) — plan as subagent batch generation over Day 5.
- **Existing schemas are solid** — review_queue already has spaced repetition fields, topic_mastery already tracks per-topic accuracy. We're building on a good foundation.
- **fcle.db has rich KB** — 354 misconceptions, 315 key terms, 77 content sections, all domain-tagged. These can power future features (glossary lookup, misconception flashcards).

---

## What We're NOT Building

- ❌ Timed-per-question mode (FCLE is untimed; adds anxiety for no reason)
- ❌ Social features / leaderboards (not the audience, adds complexity)
- ❌ Paywall or premium tier (OER mission — free always)
- ❌ AI tutoring / Socratic mode (Phase 2 of original brief — defer until after launch)
- ❌ Account system beyond anonymous (localStorage first, optional account sync later)
- ❌ Native mobile apps (PWA covers this without app store overhead)
