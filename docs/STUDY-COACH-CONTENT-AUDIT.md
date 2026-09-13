# FCLE bank — content-audit findings

**Opened:** September 13, 2026
**Found by:** the Study Coach Phase 0 topic→benchmark mapping pass
**Status:** OPEN — nothing here has been fixed

These are defects the mapping pass surfaced incidentally. They are recorded because the
Study Coach **surfaces topic names and per-topic verdicts to students**, so anything wrong
with a topic label or a topic's question membership becomes a student-facing error.

## A. Topic labels that contradict their own questions

| Topic (as shown to students) | What the questions actually cover | Problem |
|---|---|---|
| **Political socialization** (D1, 67 Q) | How parties differ from interest groups, "personal politics" campaign style, majority-party status, party-in-the-electorate | Party/interest-group content, not political socialization (belief formation). A student told "you're weak in Political socialization" is misinformed. |
| **Citizen participation** (D1, 67 Q) | Collective goods and government's role, "framing" in news media, toll goods and interest groups, party-in-the-electorate | Media-framing and interest-group content. Not participation per se. |

**Why it matters:** the coach's readiness report and weak-topic cards render these labels
verbatim. A mislabeled topic is a wrong diagnosis delivered with confidence — the exact
failure mode the Study Coach exists to avoid.

**Note:** this also means the *mapping* for these two topics was decided on question content
rather than the label (both → `SS.7.CG.2.8`). If the labels are corrected later, the mapping
should be re-checked, not assumed.

## B. Misfiled questions

| Question | Currently filed under | Belongs under |
|---|---|---|
| "In the context of U.S. foreign policy and the Cold War era, which term best describes the specific strategy adopted by the United States to prevent the expansion of communism…" | D4 · **Voting Rights Act 1965** | D4 international policy (`SS.7.CG.4.3`) |
| "According to the 'Two Presidencies' thesis by Aaron Wildavsky, how does the Civil Rights Act of 1964 illustrate a shift from the 'domestic' presidency to the 'international' presidency…" | D4 · **Civil Rights Act 1964** | D4 international policy (`SS.7.CG.4.1`) |

Both are foreign-policy items sitting inside civil-rights topics. They will corrupt any
per-topic mastery score for those topics and therefore the coach's weak-topic recommendations.

## C. Root cause of GAP-D2 (the 350 placeholder misconception codes)

Not a data-entry slip — **hardcoded in the generators**:

- `generate_d1_misconceptions.py:81` — prompt instructs `benchmark_code (always "FCLE")`
- `generate_d1_misconceptions.py:247` — `item["benchmark_code"] = "FCLE"`
- `data/gen_d3.py:49` — `item["benchmark_code"] = "FCLE"`
- `data/gen_d4_misconceptions.py:119` — `item.setdefault("benchmark_code", "FCLE")`

So re-keying the existing 350 rows is **not sufficient** — the generators must be fixed in the
same pass or the next batch reintroduces the placeholder. (D2's misconceptions do carry real
codes, which is why only D2 has a usable code signal.)

## D. Blueprint coverage question

The topic **"Article structure and content"** (D2, 6 Q) asks what each Article of the
Constitution establishes — including Articles IV, V and VI. No single `SS.7.CG` benchmark
covers "the Articles"; the state covers them piecemeal (`SS.7.CG.3.3` branches,
`SS.7.CG.3.4` Article IV, `SS.7.CG.3.5` Article V).

**Open question:** are those questions aligned to anything the FCLE actually assesses? If not,
they are practice that does not map to the exam, and they should not be counted toward a
student's readiness score.

## E. Known-stale metadata (carried, not new)

`fcle_domains.fcle_question_count` still reports 20 per domain. Real counts come from
`SELECT COUNT(*) FROM questions WHERE fcle_domain=?` (675 / 496 / 503 / 501 = 2,175). Never
read that column.

---

## Suggested disposition

| Item | Suggested action | Effort |
|---|---|---|
| A | Rename the two topics, then re-check their mapping | Small — 2 rows + a re-check |
| B | Refiling 2 questions between topics | Small |
| C | Fix 4 generator call sites, then re-key the 350 rows | Medium |
| D | Sample the 6 questions, decide whether they stay | Small — a judgement call |
| E | Backfill the column or drop it | Small |

All five are **content decisions for Mister K**, not engineering calls. None block Phase 1
(the coach engine), which reads the data as-is.
