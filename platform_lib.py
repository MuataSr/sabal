"""
platform_lib.py — Per-app paywall helper (vendored byte-identical).

Canonical: exam-prep-lms/platform/platform_lib.py
After ANY change here, copy byte-identical to fcle-study-app/,
teas-study-app/, nclex-study-app/. Verify with `cmp`.

Architecture (locked Sep 5-6, 2026): THREE SEPARATE APPS (TEAS / FCLE /
NCLEX), each with its own codebase, users table, and auth. NO shared DB,
NO unified login, NO cross-app coupling. This module is a PURE paywall
helper: pricing catalog, entitlement checks, free-cap math, and tiny DB
helpers that operate ONLY on the app's own users table (plan / premium_until).

Pricing (locked Sep 6, 2026): FCLE is ONE-TIME (90-day sprint $29 / annual
$50) per FCLE_ONE_TIME_PRICING_SPEC.md; TEAS/NCLEX stay monthly. One-time
plans carry an expiry in users.premium_until (UTC ISO); monthly plans are
active while the plan column is set.

Entitlement helpers are polymorphic: pass a plan-key STRING (TEAS/NCLEX
legacy call sites) OR a user row DICT with 'plan'/'premium_until' (FCLE
expiry-aware call sites). Do NOT add app-specific env reads here — the
free-launch override lives in each app's app.py.
"""

from datetime import datetime, timedelta, timezone

PRICING = {
    "teas_monthly":   {"name": "TEAS Monthly",  "price_cents": 1299, "interval": "month", "app": "teas"},
    "nclex_monthly":  {"name": "NCLEX Monthly", "price_cents": 1999, "interval": "month", "app": "nclex"},
    "fcle_sprint_90": {"name": "FCLE Sprint Pass", "price_cents": 2900, "interval": "once", "duration_days": 90, "app": "fcle"},
    "fcle_annual_12": {"name": "FCLE Annual",   "price_cents": 5000, "interval": "once", "duration_days": 365, "app": "fcle"},
}
# FCLE sells NO monthly plan (removed fcle_monthly $9.99 Sep 6, 2026).
# TEAS/NCLEX: monthly only; NO 90-day/annual/bundles in v1 (PRICING.md).

FREE_DAILY_QUESTIONS = 10
FREE_DAILY_AI = 5
PAID_DAILY_AI = 100


# ---------------------------------------------------------------------------
# Time helpers (UTC naive ISO — matches db.py storage convention)
# ---------------------------------------------------------------------------

def _now_utc():
    """Naive UTC datetime (consistent with SQLite TEXT columns elsewhere)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _iso(dt):
    return dt.isoformat()


# ---------------------------------------------------------------------------
# Pure entitlement checks (no DB)
# ---------------------------------------------------------------------------

def _plan_info(plan_or_user):
    """Return (plan_key, PRICING info dict-or-None) from a string or row dict."""
    if isinstance(plan_or_user, dict):
        plan = plan_or_user.get("plan") or "free"
    else:
        plan = plan_or_user or "free"
    return plan, PRICING.get(plan)


def is_premium(plan_or_user):
    """True when the user holds an unexpired paid entitlement.

    Accepts a plan-key STRING (legacy TEAS/NCLEX call sites) OR a user row
    DICT with 'plan' and 'premium_until' (FCLE expiry-aware call sites).
      - monthly plans: active while the plan column is set (no expiry in v1)
      - one-time plans: active only while now < premium_until
    Free-launch override is applied by each app's app.py BEFORE calling here.
    """
    plan, info = _plan_info(plan_or_user)
    if not info:
        return False
    if info.get("interval") == "month":
        return True
    # one-time: require an unexpired premium_until on the row
    until = (plan_or_user or {}).get("premium_until") if isinstance(plan_or_user, dict) else None
    if not until:
        return False
    try:
        return datetime.fromisoformat(until) > _now_utc()
    except (TypeError, ValueError):
        return False


def premium_until_utc(plan_or_user):
    """UTC ISO premium_until for a one-time row, else None (monthly/free)."""
    if not isinstance(plan_or_user, dict):
        return None
    plan, info = _plan_info(plan_or_user)
    if not info or info.get("interval") != "once":
        return None
    return plan_or_user.get("premium_until")


def days_remaining(plan_or_user, now=None):
    """Whole days remaining on a one-time plan (>=0), else None for monthly/free."""
    if not isinstance(plan_or_user, dict):
        return None
    until = premium_until_utc(plan_or_user)
    if not until:
        return None
    now = now or _now_utc()
    try:
        delta = datetime.fromisoformat(until) - now
    except (TypeError, ValueError):
        return None
    return max(0, delta.days)


def questions_remaining(plan_or_user, used):
    """Remaining free questions today. None = unlimited (paid entitlement)."""
    if is_premium(plan_or_user):
        return None
    return max(0, FREE_DAILY_QUESTIONS - used)


def ai_remaining(plan_or_user, used):
    """Remaining AI-tutor calls today. Paid plans get PAID_DAILY_AI."""
    if is_premium(plan_or_user):
        return max(0, PAID_DAILY_AI - used)
    return max(0, FREE_DAILY_AI - used)


def plan_for_app(app):
    """PRICING key for the given app slug ('teas' | 'fcle' | 'nclex').

    FCLE has two plans; returns the first (sprint). Prefer plans_for_app()
    when the caller can show multiple cards.
    """
    for key, info in PRICING.items():
        if info["app"] == app:
            return key
    return None


def plans_for_app(app):
    """All PRICING keys for an app slug, in catalog order."""
    return [key for key, info in PRICING.items() if info["app"] == app]


# ---------------------------------------------------------------------------
# DB helpers — explicit sqlite path; operate ONLY on users(plan[, premium_until])
# ---------------------------------------------------------------------------

def _ensure_premium_until_column(db_path):
    """Idempotently add users.premium_until (TEXT) if missing. Returns True if added."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
        if "premium_until" in cols:
            return False
        conn.execute("ALTER TABLE users ADD COLUMN premium_until TEXT")
        conn.commit()
        return True
    finally:
        conn.close()


def set_plan(db_path, email, plan):
    """UPDATE users SET plan=? WHERE lower(email)=lower(?). Returns rowcount.
    Caller guarantees the app's users table has the plan column.
    Kept for direct/billing use; grant_plan() is the entitlement-aware path."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(
            "UPDATE users SET plan=? WHERE lower(email)=lower(?)",
            (plan, email),
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def grant_plan(db_path, email, plan_key):
    """Grant a plan with correct expiry semantics. Returns rowcount.

      - interval == 'month': set plan and CLEAR premium_until (monthly plans
        are active while the plan column is set; NULL = no expiry in v1).
      - interval == 'once': set plan AND premium_until = now + duration_days
        (FCLE sprint/annual). Creates the column if the DB predates it.
    """
    info = PRICING.get(plan_key)
    if not info:
        return 0
    if info.get("interval") == "once":
        _ensure_premium_until_column(db_path)
        until = _iso(_now_utc() + timedelta(days=info["duration_days"]))
        import sqlite3
        conn = sqlite3.connect(db_path)
        try:
            cur = conn.execute(
                "UPDATE users SET plan=?, premium_until=? WHERE lower(email)=lower(?)",
                (plan_key, until, email),
            )
            conn.commit()
            return cur.rowcount
        finally:
            conn.close()
    # monthly: plan set, premium_until cleared (NULL semantics)
    _ensure_premium_until_column(db_path)
    import sqlite3
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(
            "UPDATE users SET plan=?, premium_until=NULL WHERE lower(email)=lower(?)",
            (plan_key, email),
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def get_plan(db_path, email):
    """Plan string for email, or 'free'. Operates on users(email, plan)."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT plan FROM users WHERE lower(email)=lower(?)",
            (email,),
        ).fetchone()
        return row[0] if row and row[0] else "free"
    finally:
        conn.close()


def get_premium_until(db_path, email):
    """premium_until (UTC ISO) for email, or None. NULL for monthly/free."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT premium_until FROM users WHERE lower(email)=lower(?)",
            (email,),
        ).fetchone()
        return row[0] if row and row[0] else None
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# CLI: python3 platform_lib.py grant <db_path> <email> <plan>
#      python3 platform_lib.py status <db_path> <email>
#      python3 platform_lib.py revoke <db_path> <email>
# ---------------------------------------------------------------------------

def _cli(argv):
    if len(argv) >= 5 and argv[1] == "grant":
        db_path, email, plan = argv[2], argv[3].lower(), argv[4]
        if plan not in PRICING:
            print(f"unknown plan '{plan}' (valid: {', '.join(PRICING)})")
            return 2
        rc = grant_plan(db_path, email, plan)
        extra = ""
        if PRICING[plan].get("interval") == "once":
            until = get_premium_until(db_path, email)
            extra = f", premium_until={until}"
        print(f"granted {plan} to {email}: {rc} row(s) updated{extra}")
        return 0
    if len(argv) == 4 and argv[1] == "status":
        db_path, email = argv[2], argv[3].lower()
        until = get_premium_until(db_path, email)
        print(f"{email}: plan={get_plan(db_path, email)}, premium_until={until or 'NULL'}")
        return 0
    if len(argv) == 4 and argv[1] == "revoke":
        db_path, email = argv[2], argv[3].lower()
        import sqlite3
        conn = sqlite3.connect(db_path)
        try:
            _ensure_premium_until_column(db_path)
            cur = conn.execute(
                "UPDATE users SET plan='free', premium_until=NULL WHERE lower(email)=lower(?)",
                (email,),
            )
            conn.commit()
            print(f"revoked {email}: {cur.rowcount} row(s) updated")
            return 0
        finally:
            conn.close()
    print(__doc__)
    print("usage: platform_lib.py grant <db_path> <email> <plan>")
    print("       platform_lib.py status <db_path> <email>")
    print("       platform_lib.py revoke <db_path> <email>")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(_cli(sys.argv))
