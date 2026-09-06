# FCLE Study App — Project Brief

**Created:** 2026-05-03
**Product:** Mu2 Solutions — free OER study app for the Florida Civic Literacy Exam
**Target:** Any FL college student who needs to pass FCLE for graduation

---

## What is FCLE?

- **Florida Civic Literacy Exam** — computer-based, 80 MCQ questions, no time limit
- **Passing score:** 48/80 (60%)
- **Required** for FL college graduation per s. 1007.25(5)
- **Alternative:** CLEP American Government score ≥ 50

### Four Domains (20 questions each)

| # | Domain | What's Tested |
|---|--------|--------------|
| 1 | **American Democracy** | Founding principles (natural rights, social contract, limited gov), citizen roles, political participation |
| 2 | **US Constitution** | Structure (articles, amendments, branches), federalism, ratification, Bill of Rights |
| 3 | **Founding Documents** | Declaration of Independence, Federalist Papers, Articles of Confederation, Constitution — how they shaped self-government |
| 4 | **Landmark Impact** | Supreme Court cases + landmark legislation + executive actions that shaped law and society |

---

## Why This App?

- **Every FL college student** (~400K/year) must pass FCLE or CLEP to graduate
- **Current prep is weak:** Quizlet flashcards, YouTube practice tests — all passive recall, zero tutoring
- **No Socratic tutoring exists** for civic literacy — same gap TEAS had
- **David Tran philosophy:** free, open source, actually better than paid alternatives
- **Mu2 brand fit:** serving students who can't afford $200 test-prep courses

---

## Existing Assets (What We're Reusing)

The civics project at `openstax-tutor/civics/` gives us a massive head start:

| Asset | Count | Status |
|-------|-------|--------|
| KB content (OpenStax American Government 2e) | 77 sections, 2.2M chars | ✅ Ready |
| Key terms | 315 | ✅ Ready |
| Misconceptions | 354 (across 4 categories) | ✅ Ready — needs FCLE re-mapping |
| Benchmark alignments | 36 (SS.7.CG.* — 7th grade EOC) | ⚠️ Wrong target — remap to FCLE domains |
| Eval cases | 241 (EOC-aligned) | ⚠️ Wrong target — regenerate for FCLE |
| Harness (`civics_harness.py`) | 8 functions, verified | ✅ Reusable — add FCLE domain functions |
| Flask server + voice UI | Port 5432, PTT green theme | ✅ Reusable |
| TTS pipeline | Qwen3-TTS (alloy voice) | ✅ Reusable |

### KB Coverage vs. FCLE Domains

All 34 key FCLE topics verified present in KB:
- **Supreme Court cases (12):** Marbury, Brown, Roe, Plessy, Gideon, Miranda, Tinker, Schenck, McCulloch, Gibbons, Dred Scott, Citizens United — all ✅
- **Legislation (4):** Civil Rights Act, Voting Rights Act, New Deal, Great Society — all ✅
- **Founding docs (4):** Declaration, Federalist Papers, Articles of Confederation, Bill of Rights — all ✅
- **Constitutional principles (6):** Due Process, Equal Protection, Commerce Clause, Establishment Clause, Free Exercise, Necessary & Proper — all ✅

**Gap: OpenStax American History textbook** — supplementary for historical context (Constitutional Convention era, civil rights era). Not strictly required but enriches explanations.

---

## Architecture

Same proven stack as TEAS study app:

- **Delivery:** Hosted web app / PWA
- **Model:** Gemma 4 E4B (router) + Gemma 4 26B A4B (teacher) via Google AI Studio
- **Inference:** Google AI Studio (free tier: 1500 req/day, $0/mo for Phase 1)
- **Hosting:** Digital Ocean Droplet (same as TEAS — share infra)
- **DB:** SQLite — single `fcle.db` with question bank + KB
- **Frontend:** Vanilla JS (same patterns as TEAS app)

### Key Difference from TEAS

FCLE is **pure text comprehension** — no math, no science diagrams. This means:
- Simpler question generation (no LaTeX, no calculations)
- Faster eval runs (no multi-step reasoning)
- Potentially higher baseline accuracy with smaller model

---

## Phases

### Phase 0: KB Alignment & Question Bank (5 days)

**Goal:** Remap existing KB from 7th grade EOC → FCLE 4-domain structure + generate 320 practice questions

- [ ] **0.1** FCLE domain mapping table — map each of the 77 KB sections to FCLE domain 1-4
- [ ] **0.2** Add `fcle_domain` column to content table (values: 1-4)
- [ ] **0.3** Create FCLE domain table in DB with descriptions and topic lists
- [ ] **0.4** Re-misconceptions: tag existing 354 misconceptions with FCLE domain (not EOC benchmark)
- [ ] **0.5** Identify misconceptions to ADD (postsecondary-level: Federalist No. 10/51, 14th Amendment incorporation doctrine, executive order authority, etc.)
- [ ] **0.6** Parse OpenStax American History chapters 5-8 (Constitutional era) + 24-28 (civil rights era) as supplementary KB content
- [ ] **0.7** Generate 320 practice questions (80 per domain × 30/45/25 easy/medium/hard)
- [ ] **0.8** Write 250+ char explanations for all 320 questions
- [ ] **0.9** Data quality pass: no nulls, no duplicates, no generic distractors, all MCQ A/B/C/D
- [ ] **0.10** Update harness with FCLE domain functions (search by domain, get domain stats, misconception check by domain)

### Phase 1: Eval & Tutor Tuning (3 days)

**Goal:** Validate the harness + model produces 85%+ quality on FCLE-style questions

- [ ] **1.1** Create FCLE eval rubric (reuse TEAS pattern: 4 dims × 25pts)
  - grounded_ref (answer correctness)
  - consistency (explanation matches answer)
  - mistake_catching (identifies student errors)
  - socratic_hint (guides without revealing)
- [ ] **1.2** Build 100 FCLE eval cases (25 per domain)
- [ ] **1.3** Run eval on Gemma 4 26B teacher via AI Studio
- [ ] **1.4** Tune harness based on weak dimensions
- [ ] **1.5** Scale to 250 eval cases if baseline looks good

### Phase 2: Web App Build (4 days)

**Goal:** Student-facing web app with study mode, quiz mode, progress tracking

- [ ] **2.1** Copy TEAS app skeleton, strip subject-specific code
- [ ] **2.2** Build FCLE dashboard (4 domain progress bars, overall score)
- [ ] **2.3** Study mode: question + explanation + related KB content
- [ ] **2.4** Quiz mode: timed practice, domain selection, score tracking
- [ ] **2.5** Weakness targeting: identify low-scoring domains and prioritize
- [ ] **2.6** Quickfire mode (reuse TEAS pattern)
- [ ] **2.7** Progress persistence (localStorage or account)

### Phase 3: Deploy & Polish (2 days)

- [ ] **3.1** Deploy to Digital Ocean
- [ ] **3.2** Test on mobile (most students will use phones)
- [ ] **3.3** PWA manifest + offline caching
- [ ] **3.4** Link from mu2.solutions
- [ ] **3.5** Share with CCF testing center as pilot

**Total estimated time: ~14 working days**

---

## Hard Targets

- **320 practice questions** (80 per domain) — minimum viable
- **85% eval score** across all 4 rubric dimensions
- **All MCQ with A/B/C/D options, 250+ char explanations**
- **Difficulty distribution: 30/45/25 easy/medium/hard per domain**
- **Zero paid dependencies** — same open source stack as TEAS

---

## Telegram
- Project updates → chat ID `-1003972068284`
