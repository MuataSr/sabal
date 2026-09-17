# Sabal — Free FCLE Exam Prep

**Pass the Florida Civic Literacy Exam. Free, forever.**

Sabal is a complete, self-paced study app for the Florida Civic Literacy Exam
(FCLE) — the exam every Florida college student must pass to graduate. It covers
all 36 tested standards with 2,000+ practice questions, and it does what free
flashcards and YouTube videos can't: it explains **why the right answer is right**
and **why each tempting wrong answer is wrong**.

It is **100% free and open**. No credit card, no trial, no "premium" tier, no
upsell. There is nothing to buy and nothing hidden behind a paywall. A student
signs up with just an email and gets a personal dashboard link — that's the whole
gate.

---

## Why this exists

I built Sabal with AI — on purpose.

While a lot of the world is stuck preaching AI doomerism, I decided to point the
same tools at a concrete problem: the students who can't afford paid test-prep
are the ones getting locked out of a graduation requirement. Sabal is AI used to
**open a gate, not close one** — a free, effective study aid so a student can pass
the FCLE without ever worrying about whether they can afford help.

This is the first of several open educational resources coming from
[Mu2 Solutions](https://mu2.solutions). The plan is simple: use AI to build 100%
free educational resources for the exams and subjects that big companies gate
behind a paywall — and give them away. I'm not here to sell you a subscription.
I'm here to make the paid option unnecessary. Call it what it is: a disruption of
the "pay to pass" racket.

— Muata Kamdibe, Sr. · founder, Mu2 Solutions

---

## What's inside

- **Full coverage** — all 36 FCLE benchmarks, 2,000+ questions across the four
  domains: American Democracy, US Constitution, Founding Documents, and Landmark
  Impact.
- **Explanations, not just answers** — every wrong answer carries its own "why
  this felt right but isn't" rationale, because the FCLE is engineered around
  plausible-sounding distractors.
- **Study Coach** — a deterministic, no-model coach that reads your results,
  tells you what to work on next, paces you against your exam date, and points
  you at the exact reading for anything you miss.
- **Diagnostic + readiness** — a timed diagnostic baseline, per-domain and
  per-topic readiness, a 14-day trend, and weak-area drill-downs.
- **Works on a phone** — no download, no password; sign up with an email and
  open your link.

### The Study Coach is not an LLM

The core coach is plain, deterministic code — it retrieves and ranks, it doesn't
hallucinate. That's deliberate: the free product's accuracy never depends on a
model that might drift or invent an answer.

### Bring your own AI tutor

There is also an optional AI tutor in the code — a Socratic tutor grounded in the
app's own knowledge base. It is **not** a paid feature and **not** gated. It is
plumbing: point it at any OpenAI-compatible endpoint (a local
[llama-server](https://github.com/ggml-org/llama.cpp) or a cloud model) via the
`FCLE_TUTOR_ROUTER_URL` / `FCLE_TUTOR_TEACHER_URL` environment variables, and it
works. Leave them unset and the tutor simply reports its models offline. The app
doesn't care whether you bring your own hardware or a cloud key — that choice is
yours, not ours to sell you.

---

## License

Split on purpose:

| What | License |
|---|---|
| Source code (the Flask app, templates, scripts, tooling) | [Apache-2.0](LICENSE) |
| Educational content (questions, explanations, lessons, misconception library, glossary) | [CC BY-NC-SA 4.0](LICENSE-CONTENT) |

The content uses the same license OpenStax now applies across its library.
See [ATTRIBUTION.md](ATTRIBUTION.md) for the full attribution, including the
OpenStax and public-domain source material Sabal builds on.

## Run it locally

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
FLASK_SECRET=$(openssl rand -hex 24) python3 app.py
# open http://127.0.0.1:5000
```

Student progress lives in `data/user_progress.db`; the content lives in
`data/fcle.db`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: open an issue, or fork and open
a pull request. Questions belong in the issue tracker — there is no Discord to
join and no gatekeeper to impress.
