"""
app.py — FCLE Study Buddy Flask application.

Civic literacy practice for the Florida Civic Literacy Exam.
Four domains: American Democracy, US Constitution, Founding Documents, Landmark Impact.
All data from kb.py (question bank) and db.py (user progress).
"""

import os
import uuid
import random
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
import kb
import tutor_engine
import db
import platform_lib  # per-app paywall helper (vendored, canonical in exam-prep-lms/platform)

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# App & Config
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", os.urandom(24).hex())

# Active quiz state now in SQLite (see db.py)
db.init_active_quizzes_table()

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Auth Helpers
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


def _get_current_user_id():
    user_id = session.get("user_id")
    if not user_id:
        user = db.create_anonymous_user()
        session["user_id"] = user["id"]
        session.permanent = True
        return user["id"]
    return user_id


def _get_current_user():
    user_id = session.get("user_id")
    if user_id:
        return db.get_user(user_id)
    return None


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        _get_current_user_id()
        return f(*args, **kwargs)
    return decorated


@app.context_processor
def inject_paywall():
    """Expose plan / premium state / free limits to all templates."""
    user_id = session.get("user_id")
    plan = db.get_plan(user_id) if user_id else "free"
    return {
        "current_user": _get_current_user(),
        "plan": plan,
        "is_premium": platform_lib.is_premium(plan),
        "free_daily": platform_lib.FREE_DAILY_QUESTIONS,
    }


_FREE_LIMIT_MSG = ("You've hit today's free limit of 10 questions. "
                   "Upgrade for unlimited practice, or come back tomorrow!")


def _questions_left_today():
    """Remaining free questions today for the current session.
    Returns None when unlimited (paid plan); else int >= 0."""
    user_id = session.get("user_id")
    if not user_id:
        return platform_lib.FREE_DAILY_QUESTIONS
    plan = db.get_plan(user_id)
    used = db.count_answers_today(user_id)
    return platform_lib.questions_remaining(plan, used)


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Domain Registry
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


_DOMAIN_GETTERS = {
    "american-democracy": {
        "id": 1,
        "topics": kb.get_american_democracy_topics,
        "quiz": kb.get_american_democracy_questions,
        "name": "American Democracy",
        "icon": "🏛️",
        "color": "#1B4332",
    },
    "us-constitution": {
        "id": 2,
        "topics": kb.get_us_constitution_topics,
        "quiz": kb.get_us_constitution_questions,
        "name": "US Constitution",
        "icon": "📜",
        "color": "#7F4F24",
    },
    "founding-documents": {
        "id": 3,
        "topics": kb.get_founding_documents_topics,
        "quiz": kb.get_founding_documents_questions,
        "name": "Founding Documents",
        "icon": "🦅",
        "color": "#1B3A5C",
    },
    "landmark-impact": {
        "id": 4,
        "topics": kb.get_landmark_impact_topics,
        "quiz": kb.get_landmark_impact_questions,
        "name": "Landmark Impact",
        "icon": "⚖️",
        "color": "#6B2737",
    },
}


def _get_domain_info(slug):
    return _DOMAIN_GETTERS.get(slug)


def _pretty_domain(slug):
    info = _DOMAIN_GETTERS.get(slug)
    return info["name"] if info else (slug or "Quiz").title()


def _all_domains(user_id):
    domains = []
    for slug, info in _DOMAIN_GETTERS.items():
        readiness = db.get_readiness(user_id, slug) or 0
        domains.append({
            "domain_name": info["name"],
            "slug": slug,
            "readiness_pct": readiness,
            "icon": info["icon"],
            "color": info["color"],
        })
    return domains


def _greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


def _exam_countdown(exam_date_str):
    if not exam_date_str:
        return None
    try:
        exam = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        diff = (exam - today).days
        return max(0, diff)
    except (ValueError, TypeError):
        return None


def _build_recommendations(user_id):
    recs = []
    for slug, info in _DOMAIN_GETTERS.items():
        readiness = db.get_readiness(user_id, slug) or 0
        if readiness < 60:
            topics = info["topics"]()
            if topics:
                t = random.choice(topics)
                recs.append({
                    "domain": info["name"],
                    "topic": t["name"],
                    "slug": slug,
                    "level": "Building" if readiness < 40 else ("Fair" if readiness < 70 else "Strong"),
                })
    return recs[:5]


def _build_recent_sessions(user_id):
    sessions = db.get_recent_sessions(user_id, 5)
    result = []
    for s in sessions:
        pct = s.get("pct", 0) or 0
        if pct >= 80:
            status = "Strong"
        elif pct >= 60:
            status = "Fair"
        else:
            status = "Building"
        result.append({
            "domain": s.get("domain", "Unknown"),
            "question_count": s.get("num_questions", 0),
            "score": int(pct),
            "date": s.get("finished_at", "")[:10] if s.get("finished_at") else "—",
            "status": status,
        })
    return result


def _format_time(seconds):
    if seconds is None:
        return "0:00"
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m}:{s:02d}"


def _premium_trend(user_id):
    """14-day daily-average readiness for the premium trend chart.
    Returns [{day: 'MM/DD', pct: int|None}] oldest->newest."""
    sessions = db.get_recent_sessions(user_id, 200)
    by_day = {}
    for s in sessions:
        finished = s.get("finished_at") or ""
        if not finished:
            continue
        day = finished[:10]
        pct = s.get("pct")
        if pct is None:
            continue
        by_day.setdefault(day, []).append(float(pct))
    out = []
    today = datetime.utcnow().date()
    for i in range(13, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        vals = by_day.get(d)
        out.append({
            "day": d[5:],
            "pct": int(round(sum(vals) / len(vals))) if vals else None,
        })
    return out


def _premium_weak_areas(user_id):
    """Weak topics below 70% w/ >=3 attempts across domains."""
    weak = []
    for slug, info in _DOMAIN_GETTERS.items():
        d_stats = db.get_subject_stats(user_id, slug)
        for t in d_stats.get("topics", []):
            if (t.get("total") or 0) >= 3 and (t.get("pct") or 0) < 70:
                weak.append({
                    "name": t.get("topic", "Topic"),
                    "area": info["name"],
                    "pct": int(round(t.get("pct", 0) or 0)),
                    "url": f"/quiz/{slug}",
                })
    weak.sort(key=lambda w: w["pct"])
    return weak[:8]


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Routes
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


@app.route("/")
@login_required
def dashboard():
    user_id = session.get("user_id", 1)
    user = _get_current_user()
    stats = db.get_overall_stats(user_id)
    overall_pct = stats.get("overall_readiness", 0) or 0

    domains = _all_domains(user_id)

    for d in domains:
        d_stats = db.get_subject_stats(user_id, d["slug"])
        weak = 0
        for t in d_stats.get("topics", []):
            if (t.get("pct") or 0) < 60:
                weak += 1
        d["weak_count"] = weak

    recommendations = _build_recommendations(user_id)
    recent_sessions = _build_recent_sessions(user_id)

    display_name = user["display_name"] if user else "Student"
    exam_days = _exam_countdown(user.get("exam_date") if user else None)

    return render_template("dashboard.html",
        greeting=_greeting(),
        display_name=display_name,
        overall_pct=int(overall_pct),
        overall_readiness=int(overall_pct),
        domains=domains,
        recommendations=recommendations,
        recent_sessions=recent_sessions,
        exam_days=exam_days,
        is_anonymous=user.get("is_anonymous", 1) if user else 1,
    )


@app.route("/quiz/<domain_slug>")
@login_required
def quiz_start(domain_slug):
    user_id = session.get("user_id", 1)
    if domain_slug == "mixed":
        return quiz_start_mixed()

    info = _get_domain_info(domain_slug)
    if not info:
        return redirect("/")

    count = request.args.get("count", 5, type=int)
    count = min(count, 20)

    rem = _questions_left_today()
    if rem == 0:
        flash(_FREE_LIMIT_MSG, "info")
        return redirect("/pricing")
    if rem is not None:
        count = min(count, rem)
        if count < 1:
            flash(_FREE_LIMIT_MSG, "info")
            return redirect("/pricing")

    questions = info["quiz"](count=count)
    if not questions:
        return redirect("/")

    quiz_id = uuid.uuid4().hex[:12]
    db.save_quiz(quiz_id, {
        "user_id": user_id,
        "domain": domain_slug,
        "questions": questions,
        "current_index": 0,
        "answers": [],
        "started_at": datetime.now().isoformat(),
        "session_id": None,
    })

    return redirect(f"/quiz/{domain_slug}/{quiz_id}/0")


def quiz_start_mixed():
    user_id = session.get("user_id", 1)
    count = request.args.get("count", 10, type=int)
    count = min(count, 20)

    rem = _questions_left_today()
    if rem == 0:
        flash(_FREE_LIMIT_MSG, "info")
        return redirect("/pricing")
    if rem is not None:
        count = min(count, rem)
        if count < 1:
            flash(_FREE_LIMIT_MSG, "info")
            return redirect("/pricing")

    questions = kb.get_mixed_quiz_questions(count=count)

    if not questions:
        return redirect("/")

    quiz_id = uuid.uuid4().hex[:12]
    db.save_quiz(quiz_id, {
        "user_id": user_id,
        "domain": "mixed",
        "questions": questions,
        "current_index": 0,
        "answers": [],
        "started_at": datetime.now().isoformat(),
        "session_id": None,
    })

    return redirect(f"/quiz/mixed/{quiz_id}/0")


@app.route("/quiz/<domain_slug>/<quiz_id>/<int:q_index>")
@login_required
def quiz_question(domain_slug, quiz_id, q_index):
    quiz = db.load_quiz(quiz_id)
    if not quiz:
        return redirect("/")

    questions = quiz["questions"]
    if q_index < 0 or q_index >= len(questions):
        return redirect("/")

    question = questions[q_index]

    domain_name = "Mixed Review"
    if domain_slug != "mixed":
        info = _get_domain_info(domain_slug)
        domain_name = info["name"] if info else domain_slug

    return render_template("quiz.html",
        question=question,
        current_q=q_index + 1,
        total_q=len(questions),
        domain_name=domain_name,
        domain_slug=domain_slug,
        quiz_id=quiz_id,
    )


@app.route("/quiz/<domain_slug>/<quiz_id>/<int:q_index>/answer", methods=["POST"])
@login_required
def quiz_answer(domain_slug, quiz_id, q_index):
    quiz = db.load_quiz(quiz_id)
    if not quiz:
        return redirect("/")

    # Safety net for pre-existing in-flight sessions: never let a free user
    # bank answers past today's quota.
    if _questions_left_today() == 0:
        flash(_FREE_LIMIT_MSG, "info")
        return redirect("/pricing")

    user_id = quiz.get("user_id", session.get("user_id", 1))
    questions = quiz["questions"]
    if q_index < 0 or q_index >= len(questions):
        return redirect("/")

    question = questions[q_index]
    selected = request.form.get("selected", "")
    time_elapsed = request.form.get("time_elapsed", 0, type=float)
    confidence = request.form.get("confidence", None, type=int)

    correct_answer = question.get("correct_answer", "")
    is_correct = str(selected).strip() == str(correct_answer).strip()

    answer = {
        "question_id": question.get("id", q_index),
        "question_text": question.get("question_text", ""),
        "selected": selected,
        "correct": correct_answer,
        "is_correct": is_correct,
        "time_elapsed": time_elapsed,
        "confidence": confidence,
        "topic": question.get("topic", ""),
    }
    quiz["answers"].append(answer)

    if quiz["session_id"] is None:
        quiz["session_id"] = db.create_session(
            user_id=user_id,
            domain=quiz["domain"],
            num_questions=len(questions),
        )

    db.record_answer(
        user_id=user_id,
        session_id=quiz["session_id"],
        question_id=question.get("id", q_index),
        question_text=question.get("question_text", ""),
        selected=selected,
        correct=correct_answer,
        is_correct=is_correct,
        time_elapsed=int(time_elapsed),
        confidence=confidence,
    )

    topic = question.get("topic", "")
    if topic:
        db.update_topic_mastery(user_id, quiz["domain"], topic, is_correct)

    if confidence is not None:
        db.update_review_queue(
            user_id=user_id,
            question_id=question.get("id", q_index),
            domain=quiz["domain"],
            topic=topic,
            is_correct=is_correct,
            confidence=confidence,
        )

    # Persist quiz state to SQLite
    db.save_quiz(quiz_id, quiz)

    next_index = q_index + 1
    explanation = question.get("explanation", "")
    wrong_explanations = question.get("wrong_explanations", [])
    wrong_answers = question.get("wrong_answers", [])
    # Build a map: wrong_answer -> wrong_explanation
    wrong_explanation_map = {}
    if wrong_explanations and wrong_answers:
        for i, wa in enumerate(wrong_answers):
            if i < len(wrong_explanations):
                wrong_explanation_map[wa] = wrong_explanations[i]
    # Also try building from options: anything that's not correct_answer
    if not wrong_explanation_map and wrong_explanations:
        options = question.get("options", [])
        idx = 0
        for opt in options:
            if opt != correct_answer and idx < len(wrong_explanations):
                wrong_explanation_map[opt] = wrong_explanations[idx]
                idx += 1

    feedback_mode = "quiz"
    if confidence == 1:
        feedback_mode = "teach"
    elif confidence == 2:
        feedback_mode = "hint"

    domain_name = "Mixed Review"
    if domain_slug != "mixed":
        info = _get_domain_info(domain_slug)
        domain_name = info["name"] if info else domain_slug

    render_kwargs = dict(
        question=question,
        current_q=q_index + 1,
        total_q=len(questions),
        domain_name=domain_name,
        domain_slug=domain_slug,
        quiz_id=quiz_id,
        feedback=True,
        is_correct=is_correct,
        selected=selected,
        correct_answer=correct_answer,
        explanation=explanation,
        wrong_explanation_map=wrong_explanation_map,
        feedback_mode=feedback_mode,
    )

    if next_index < len(questions):
        render_kwargs["next_url"] = f"/quiz/{domain_slug}/{quiz_id}/{next_index}"
    else:
        correct_count = sum(1 for a in quiz["answers"] if a["is_correct"])
        total = len(quiz["answers"])
        pct = int((correct_count / total * 100) if total else 0)
        db.finish_session(quiz["session_id"], correct_count, total, pct)
        render_kwargs["next_url"] = f"/results/{domain_slug}/{quiz_id}"

    return render_template("quiz.html", **render_kwargs)


@app.route("/results/<domain_slug>/<quiz_id>")
@login_required
def quiz_results(domain_slug, quiz_id):
    quiz = db.load_quiz(quiz_id)
    if not quiz:
        return redirect("/")

    answers = quiz["answers"]
    questions = quiz["questions"]

    correct_count = sum(1 for a in answers if a["is_correct"])
    total = len(answers)
    pct = int((correct_count / total * 100) if total else 0)
    elapsed = sum(a.get("time_elapsed", 0) for a in answers)

    best_streak = 0
    current_streak = 0
    for a in answers:
        if a["is_correct"]:
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            current_streak = 0

    topic_map = {}
    for a in answers:
        topic = a.get("topic", "General")
        if topic not in topic_map:
            topic_map[topic] = {"correct": 0, "total": 0}
        topic_map[topic]["total"] += 1
        if a["is_correct"]:
            topic_map[topic]["correct"] += 1

    topic_breakdown = [
        {"topic": t, "correct": v["correct"], "total": v["total"]}
        for t, v in topic_map.items()
    ]

    mistakes = [
        {
            "question": a["question_text"],
            "user_answer": a["selected"],
            "correct_answer": a["correct"],
            "explanation": next(
                (q.get("explanation", "") for q in questions if q.get("question_text") == a["question_text"]),
                "",
            ),
        }
        for a in answers if not a["is_correct"]
    ]

    domain_name = "Mixed Review"
    if domain_slug != "mixed":
        info = _get_domain_info(domain_slug)
        domain_name = info["name"] if info else domain_slug

    db.delete_quiz(quiz_id)

    return render_template("results.html",
        score=correct_count,
        total=total,
        pct=pct,
        elapsed_time=_format_time(elapsed),
        accuracy=pct,
        best_streak=best_streak,
        topic_breakdown=topic_breakdown,
        mistakes=mistakes,
        domain_slug=domain_slug,
        domain_name=domain_name,
    )


@app.route("/stats")
@login_required
def stats():
    user_id = session.get("user_id", 1)
    overall_stats = db.get_overall_stats(user_id)
    overall_readiness = int(overall_stats.get("overall_readiness", 0) or 0)

    domains = []
    for slug in _DOMAIN_GETTERS:
        info = _DOMAIN_GETTERS[slug]
        d_stats = db.get_subject_stats(user_id, slug)
        topics = info["topics"]()

        db_topics = {t["topic"]: t for t in d_stats.get("topics", [])}
        strong = 0
        for t in topics:
            db_t = db_topics.get(t["name"]) or db_topics.get(t.get("slug", ""))
            if db_t and (db_t.get("pct") or 0) >= 80:
                strong += 1

        domains.append({
            "name": info["name"],
            "slug": slug,
            "icon": info["icon"],
            "readiness_pct": int(d_stats.get("readiness_pct", 0) or 0),
            "strong_topics": strong,
            "total_topics": len(topics),
        })

    recent = db.get_recent_sessions(user_id, 10)
    recent_quizzes = []
    for s in recent:
        recent_quizzes.append({
            "date": s.get("finished_at", "")[:10] if s.get("finished_at") else "—",
            "domain_name": s.get("domain", "Unknown").title(),
            "domain_slug": s.get("domain", ""),
            "score": int(s.get("pct", 0) or 0),
            "total_questions": s.get("num_questions", 0),
        })

    weekly = db.get_weekly_activity(user_id)

    current_streak = 0
    today = datetime.utcnow().date()
    check_date = today
    activity_days = {w.get("day", "") for w in weekly}
    while True:
        if check_date.isoformat() in activity_days:
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    return render_template("stats.html",
        overall_readiness=overall_readiness,
        domains=domains,
        recent_quizzes=recent_quizzes,
        weekly_activity=weekly,
        current_streak=current_streak,
        premium_trend=_premium_trend(user_id),
        premium_weak=_premium_weak_areas(user_id),
        active_nav="stats",
    )


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html",
        user=_get_current_user(),
        version="0.1.0 MVP",
        active_nav="settings",
    )


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Diagnostic (Pre-Test)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


def _build_diagnostic_questions():
    """Build 20 diagnostic questions: 5 per domain, mixed difficulty."""
    questions = []
    for slug, info in _DOMAIN_GETTERS.items():
        qs = info["quiz"](count=5)
        for q in qs:
            q["_domain_slug"] = slug
            q["_domain_name"] = info["name"]
            questions.append(q)
    random.shuffle(questions)
    return questions


@app.route("/diagnostic", methods=["GET", "POST"])
@login_required
def diagnostic():
    user_id = session.get("user_id", 1)
    already = db.has_diagnostic(user_id)

    if request.method == "POST":
        # Start diagnostic quiz
        questions = _build_diagnostic_questions()
        quiz_id = uuid.uuid4().hex[:12]
        db.save_quiz(quiz_id, {
            "questions": questions,
            "answers": [],
            "started_at": datetime.utcnow().isoformat(),
            "is_diagnostic": True,
        })
        return redirect(f"/diagnostic/{quiz_id}/0")

    return render_template("diagnostic.html",
        user=_get_current_user(),
        already_taken=already,
        active_nav="diagnostic",
    )


@app.route("/diagnostic/<quiz_id>/<int:q_index>", methods=["GET"])
@login_required
def diagnostic_question(quiz_id, q_index):
    quiz = db.load_quiz(quiz_id)
    if not quiz or not quiz.get("is_diagnostic"):
        flash("Diagnostic session not found.", "error")
        return redirect("/diagnostic")

    questions = quiz["questions"]
    if q_index >= len(questions):
        return redirect(f"/diagnostic/results/{quiz_id}")

    q = questions[q_index]
    q["index"] = q_index
    q["total"] = len(questions)
    q["options"] = q.get("options", [])

    return render_template("diagnostic_quiz.html",
        question=q,
        quiz_id=quiz_id,
        q_index=q_index,
        total=len(questions),
        active_nav="diagnostic",
    )


@app.route("/diagnostic/<quiz_id>/<int:q_index>/answer", methods=["POST"])
@login_required
def diagnostic_answer(quiz_id, q_index):
    quiz = db.load_quiz(quiz_id)
    if not quiz or not quiz.get("is_diagnostic"):
        return redirect("/diagnostic")

    questions = quiz["questions"]
    if q_index >= len(questions):
        return redirect(f"/diagnostic/results/{quiz_id}")

    q = questions[q_index]
    selected = request.form.get("selected", "")
    is_correct = str(selected).strip() == str(q.get("correct_answer", "")).strip()
    quiz["answers"].append({
        "question_id": q["id"],
        "question_text": q["question_text"],
        "selected": selected,
        "correct": q.get("correct_answer", ""),
        "is_correct": is_correct,
        "domain": q["_domain_slug"],
        "domain_name": q["_domain_name"],
        "topic": q.get("topic", ""),
    })

    next_index = q_index + 1
    if next_index >= len(questions):
        return redirect(f"/diagnostic/results/{quiz_id}")
    return redirect(f"/diagnostic/{quiz_id}/{next_index}")


@app.route("/diagnostic/results/<quiz_id>")
@login_required
def diagnostic_results(quiz_id):
    quiz = db.load_quiz(quiz_id)
    if not quiz or not quiz.get("is_diagnostic"):
        flash("Diagnostic session not found.", "error")
        return redirect("/diagnostic")

    answers = quiz["answers"]
    taken_at = quiz["started_at"]
    user_id = session.get("user_id", 1)

    # Build per-domain and per-topic results
    domain_results = {}
    topic_results = {}

    for a in answers:
        dom = a["domain"]
        dom_name = a["domain_name"]
        topic = a["topic"]

        if dom not in domain_results:
            domain_results[dom] = {"name": dom_name, "slug": dom, "total": 0, "correct": 0}
        domain_results[dom]["total"] += 1
        if a["is_correct"]:
            domain_results[dom]["correct"] += 1

        key = f"{dom}|{topic}"
        if key not in topic_results:
            topic_results[key] = {
                "domain": dom, "domain_name": dom_name, "topic": topic,
                "total": 0, "correct": 0,
            }
        topic_results[key]["total"] += 1
        if a["is_correct"]:
            topic_results[key]["correct"] += 1

    # Calculate percentages and sort
    for d in domain_results.values():
        d["pct"] = round(d["correct"] / d["total"] * 100, 1) if d["total"] > 0 else 0

    for t in topic_results.values():
        t["pct"] = round(t["correct"] / t["total"] * 100, 1) if t["total"] > 0 else 0

    # Sort domains: weakest first (study order)
    sorted_domains = sorted(domain_results.values(), key=lambda x: x["pct"])

    # Sort topics: weakest first
    sorted_topics = sorted(topic_results.values(), key=lambda x: x["pct"])

    # Identify strengths and weaknesses
    strengths = [d for d in domain_results.values() if d["pct"] >= 80]
    weaknesses = [d for d in domain_results.values() if d["pct"] < 60]
    middle = [d for d in domain_results.values() if 60 <= d["pct"] < 80]

    # Save baselines to DB
    for key, t in topic_results.items():
        db.save_diagnostic_baseline(
            user_id, t["domain"], t["topic"],
            t["total"], t["correct"], t["pct"], taken_at,
        )

    # Overall score
    total_q = len(answers)
    total_correct = sum(1 for a in answers if a["is_correct"])
    overall_pct = round(total_correct / total_q * 100, 1) if total_q > 0 else 0

    # Clean up active quiz
    db.delete_quiz(quiz_id)

    return render_template("diagnostic_results.html",
        overall_pct=overall_pct,
        total_correct=total_correct,
        total_questions=total_q,
        domain_results=sorted_domains,
        topic_results=sorted_topics,
        strengths=strengths,
        weaknesses=weaknesses,
        middle=middle,
        study_order=sorted_domains,
        active_nav="diagnostic",
    )


@app.route("/settings/reset", methods=["POST"])
@login_required
def settings_reset():
    user_id = session.get("user_id", 1)
    db.reset_all_progress(user_id)
    flash("All progress has been reset.", "success")
    return redirect("/settings")


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Auth Routes
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        display_name = request.form.get("display_name", "").strip() or "Student"

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("signup.html")
        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return render_template("signup.html")

        try:
            user = db.create_user(email=email, password=password, display_name=display_name)
            session["user_id"] = user["id"]
            session.permanent = True
            flash("Account created! Welcome to FCLE Study Buddy.", "success")
            return redirect("/")
        except ValueError as e:
            flash(str(e), "error")
            return render_template("signup.html")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html")

        user = db.verify_login(email, password)
        if not user:
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session.permanent = True
        flash(f"Welcome back, {user['display_name']}!", "success")
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out. See you next time!", "success")
    return redirect("/")


@app.route("/pricing")
def pricing():
    """Pricing / upgrade page. Square checkout is Phase 2 — button is inert."""
    user_id = session.get("user_id")
    plan = db.get_plan(user_id) if user_id else "free"
    return render_template(
        "premium.html",
        plan=plan,
        is_premium=platform_lib.is_premium(plan),
        free_daily=platform_lib.FREE_DAILY_QUESTIONS,
        plan_price=platform_lib.PRICING[platform_lib.plan_for_app("fcle")],
    )


@app.route("/account")
@login_required
def account():
    """Student account portal — shared portal.html (see exam-prep-lms/platform)."""
    user_id = session.get("user_id", 1)
    user = _get_current_user() or {}
    plan = db.get_plan(user_id)
    is_premium = platform_lib.is_premium(plan)
    plan_key = platform_lib.plan_for_app("fcle")
    pinfo = platform_lib.PRICING[plan_key]
    used = db.count_answers_today(user_id)
    rem = platform_lib.questions_remaining(plan, used)
    stats = db.get_overall_stats(user_id)
    total = db.get_total_answered(user_id)

    areas = [{"name": _pretty_domain(d.get("name") or d.get("slug") or ""),
              "pct": int(d["readiness_pct"])}
             for d in stats.get("domains", [])]
    recent = [{"name": _pretty_domain(s.get("domain") or "Quiz"),
               "score": s.get("score", 0), "date": s.get("date", "—"),
               "status": s.get("status", "Building")}
              for s in _build_recent_sessions(user_id)]
    created = user.get("created_at", "") or ""

    return render_template("portal.html",
        app_name="FCLE Study Buddy",
        app_slug="fcle",
        plan=plan,
        is_premium=is_premium,
        plan_label=pinfo["name"],
        plan_price_str="${:,.2f}".format(pinfo["price_cents"] / 100),
        free_daily=platform_lib.FREE_DAILY_QUESTIONS,
        questions_used_today=used,
        questions_remaining=rem,
        total_answered=total,
        overall_pct=int(stats.get("overall_readiness", 0) or 0),
        exam_days=_exam_countdown(user.get("exam_date") if user else None),
        member_since=created[:10] if created else None,
        areas=areas,
        chips=[{"label": "Total answered", "value": total}],
        recent_sessions=recent,
        siblings=[
            {"name": "TEAS Study", "note": "Nursing school entrance exam prep."},
            {"name": "NCLEX Study", "note": "Passed the TEAS? Next stop: licensure prep."},
        ],
        active_nav="account",
    )


@app.route("/onboarding", methods=["GET", "POST"])
@login_required
def onboarding():
    user_id = session.get("user_id", 1)
    user = _get_current_user()

    if user and user.get("onboarding_done"):
        return redirect("/")

    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip() or "Student"
        exam_date = request.form.get("exam_date", "").strip() or None
        target_score = request.form.get("target_score", 80, type=int)
        target_score = max(0, min(100, target_score))

        db.update_user(user_id,
            display_name=display_name,
            exam_date=exam_date,
            target_score=target_score,
            onboarding_done=1,
        )
        flash("Profile saved! Let's start studying.", "success")
        return redirect("/")

    return render_template("onboarding.html", user=user)


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Stimulus Literacy Training
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


@app.route("/stimulus")
@login_required
def stimulus_hub():
    """Hub page: pick domain or do mixed stimulus practice."""
    domains = kb.get_domains()
    domain_data = []
    for d in domains:
        stim_count = kb.get_stimulus_questions(domain_id=d["id"], count=999)
        domain_data.append({
            "id": d["id"],
            "name": d["name"],
            "slug": d["name"].lower().replace(" ", "-"),
            "stimulus_count": len(stim_count),
        })
    total_stim = sum(dd["stimulus_count"] for dd in domain_data)

    return render_template("stimulus_hub.html",
        domains=domain_data,
        total_stimulus=total_stim,
        active_nav="stimulus",
    )


@app.route("/stimulus/practice", methods=["GET", "POST"])
@app.route("/stimulus/practice/<int:domain_id>", methods=["GET", "POST"])
@login_required
def stimulus_practice(domain_id=None):
    """Practice reading stimulus passages with guided annotation steps."""
    if request.method == "POST":
        # Start a new practice session
        count = min(int(request.form.get("count", 5)), 20)
        questions = kb.get_stimulus_questions(domain_id=domain_id, count=count)
        if not questions:
            flash("No stimulus questions available for this selection.", "error")
            return redirect(f"/stimulus")

        quiz_id = uuid.uuid4().hex[:12]
        db.save_quiz(quiz_id, {
            "questions": questions,
            "answers": [],
            "started_at": datetime.utcnow().isoformat(),
            "is_stimulus": True,
            "domain_id": domain_id,
        })
        return redirect(f"/stimulus/practice/{quiz_id}/0")

    domain_name = None
    if domain_id:
        domains = kb.get_domains()
        domain_name = next((d["name"] for d in domains if d["id"] == domain_id), "Unknown")

    return render_template("stimulus_practice_setup.html",
        domain_id=domain_id,
        domain_name=domain_name,
        active_nav="stimulus",
    )


@app.route("/stimulus/practice/<quiz_id>/<int:q_index>", methods=["GET", "POST"])
@login_required
def stimulus_practice_question(quiz_id, q_index):
    """Show a stimulus question with guided annotation workflow."""
    quiz = db.load_quiz(quiz_id)
    if not quiz or not quiz.get("is_stimulus"):
        flash("Practice session not found.", "error")
        return redirect("/stimulus")

    questions = quiz["questions"]
    if q_index >= len(questions):
        return redirect(f"/stimulus/practice/results/{quiz_id}")

    q = questions[q_index]

    # Parse options
    wrong_answers = q.get("wrong_answers", "[]")
    if isinstance(wrong_answers, str):
        wrong_answers = eval(wrong_answers) if wrong_answers.startswith("[") else wrong_answers.split("|")
    correct = q.get("correct_answer", "")
    all_options = wrong_answers + [correct]
    random.shuffle(all_options)

    # Step management
    step = request.form.get("step", request.args.get("step", "read"))
    annotation = request.form.get("annotation", "")
    guess = request.form.get("guess", "")

    if request.method == "POST":
        new_step = request.form.get("next_step", "")
        if new_step:
            step = new_step
            if new_step == "answer":
                annotation = request.form.get("annotation", "")
            elif new_step == "results":
                # Save answer
                selected = request.form.get("selected", "")
                is_correct = selected == correct
                quiz["answers"].append({
                    "question_id": q["id"],
                    "question_text": q["question"],
                    "stimulus": q["stimulus"],
                    "selected": selected,
                    "correct": correct,
                    "is_correct": is_correct,
                    "annotation": annotation,
                    "guess": guess,
                    "topic": q.get("topic", ""),
                    "domain_id": q.get("fcle_domain", ""),
                })
                # Persist stimulus state to SQLite
                db.save_quiz(quiz_id, quiz)
                next_idx = q_index + 1
                if next_idx >= len(questions):
                    return redirect(f"/stimulus/practice/results/{quiz_id}")
                return redirect(f"/stimulus/practice/{quiz_id}/{next_idx}")

    return render_template("stimulus_practice_question.html",
        question=q,
        quiz_id=quiz_id,
        q_index=q_index,
        total=len(questions),
        options=all_options,
        step=step,
        annotation=annotation,
        guess=guess,
        correct_answer=correct,
        active_nav="stimulus",
    )


@app.route("/stimulus/practice/results/<quiz_id>")
@login_required
def stimulus_practice_results(quiz_id):
    """Results for stimulus practice session."""
    quiz = db.load_quiz(quiz_id)
    if not quiz or not quiz.get("is_stimulus"):
        flash("Practice session not found.", "error")
        return redirect("/stimulus")

    answers = quiz["answers"]
    total = len(answers)
    correct = sum(1 for a in answers if a["is_correct"])
    pct = round(correct / total * 100, 1) if total > 0 else 0

    # Track stimulus literacy metrics
    guessed_correct = sum(1 for a in answers if a["guess"].strip() != "" and a["is_correct"])
    annotated = sum(1 for a in answers if a["annotation"].strip() != "")

    # Domain name lookup
    domains = kb.get_domains()
    domain_map = {d["id"]: d["name"] for d in domains}

    db.delete_quiz(quiz_id)

    return render_template("stimulus_results.html",
        answers=answers,
        total=total,
        correct=correct,
        pct=pct,
        guessed_correct=guessed_correct,
        annotated=annotated,
        domain_map=domain_map,
        active_nav="stimulus",
    )

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Socratic Tutor — dual-model local AI tutor
# ---------------------------------------------------------------------------

_tutor = tutor_engine.TutorEngine()

@app.route('/tutor')
def tutor_page():
    user_id = session.get("user_id", 1)
    has_diagnostic = db.has_diagnostic(user_id)
    
    # Build domain progress
    domain_slugs = {
        1: ("american-democracy", "\U0001f3db\ufe0f"),
        2: ("us-constitution", "\U0001f4dc"),
        3: ("founding-documents", "\U0001f985"),
        4: ("landmark-impact", "\u2696\ufe0f"),
    }
    domain_progress = []
    for did, (slug, icon) in domain_slugs.items():
        pct = db.get_readiness(user_id, slug) or 0
        domain_progress.append({
            "id": did,
            "slug": slug,
            "name": _DOMAIN_GETTERS[slug]["name"] if slug in _DOMAIN_GETTERS else f"Domain {did}",
            "icon": icon,
            "pct": pct,
        })
    
    # Overall stats
    stats = db.get_overall_stats(user_id) or {}
    overall_readiness = stats.get("overall_readiness", 0)
    
    # Count total answered + sessions
    total_answered = 0
    sessions_count = 0
    try:
        import sqlite3 as _sq
        _c = _sq.connect("data/user_progress.db")
        _c.row_factory = _sq.Row
        _r = _c.execute("SELECT COUNT(*) as c FROM answers WHERE user_id=?", (user_id,)).fetchone()
        total_answered = _r["c"] if _r else 0
        _r2 = _c.execute("SELECT COUNT(*) as c FROM quiz_sessions WHERE user_id=?", (user_id,)).fetchone()
        sessions_count = _r2["c"] if _r2 else 0
        _c.close()
    except Exception:
        pass
    
    # Load chat history
    chat_messages = []
    try:
        import sqlite3 as _sq2
        _c2 = _sq2.connect("data/user_progress.db")
        _c2.row_factory = _sq2.Row
        _rows = _c2.execute(
            "SELECT role, content, domain, created_at FROM tutor_messages WHERE user_id=? ORDER BY id DESC LIMIT 50",
            (user_id,)
        ).fetchall()
        _c2.close()
        chat_messages = [{"role": r["role"], "content": r["content"], "domain": r["domain"], "time": r["created_at"]} for r in reversed(_rows)]
    except Exception:
        pass
    
    return render_template('tutor.html',
        active_nav='tutor',
        has_diagnostic=has_diagnostic,
        domain_progress=domain_progress,
        total_answered=total_answered,
        overall_pct=overall_readiness,
        sessions_count=sessions_count,
        chat_messages=chat_messages,
    )

@app.route('/tutor/chat', methods=['POST'])
def tutor_chat():
    data = request.get_json(force=True)
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Empty message'}), 400
    domain = data.get('domain')
    history = data.get('history', [])
    user_id = session.get("user_id", 1)
    
    # Save student message
    import sqlite3 as _sq
    try:
        _c = _sq.connect("data/user_progress.db")
        _c.execute("INSERT INTO tutor_messages (user_id, role, content, domain) VALUES (?, 'student', ?, ?)",
                   (user_id, message, domain))
        _c.commit()
        _c.close()
    except Exception:
        pass
    
    result = _tutor.chat(message, domain=domain, history=history)
    
    # Save tutor response
    try:
        _c = _sq.connect("data/user_progress.db")
        _c.execute("INSERT INTO tutor_messages (user_id, role, content, domain) VALUES (?, 'tutor', ?, ?)",
                   (user_id, result.get('response', ''), domain))
        _c.commit()
        _c.close()
    except Exception:
        pass
    
    return jsonify(result)

@app.route('/tutor/status')
def tutor_status():
    return jsonify(_tutor.check_servers())


@app.route('/tutor/history')
def tutor_history():
    """Load persistent chat history for the current user."""
    user_id = session.get("user_id", 1)
    limit = request.args.get("limit", 50, type=int)
    import sqlite3 as _sq
    try:
        _c = _sq.connect("data/user_progress.db")
        _c.row_factory = _sq.Row
        rows = _c.execute(
            "SELECT role, content, domain, created_at FROM tutor_messages WHERE user_id=? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
        _c.close()
        messages = [{"role": r["role"], "content": r["content"], "domain": r["domain"], "time": r["created_at"]} for r in reversed(rows)]
        return jsonify({"messages": messages})
    except Exception as e:
        return jsonify({"messages": [], "error": str(e)})

# Entry point
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    db.init_db()
    db.init_diagnostic_table()
    app.run(host="0.0.0.0", port=5002, debug=False)

