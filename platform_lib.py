"""
platform_lib.py — Per-app paywall helper (vendored byte-identical).

Canonical: exam-prep-lms/platform/platform_lib.py
After ANY change here, copy byte-identical to fcle-study-app/,
teas-study-app/, nclex-study-app/. Verify with `cmp`.

Architecture (locked Sep 5-6, 2026): THREE SEPARATE APPS (TEAS / FCLE /
NCLEX), each with its own codebase, users table, and auth. NO shared DB,
NO unified login, NO cross-app coupling. This module is a PURE paywall
helper: pricing catalog, entitlement checks, free-cap math, and two tiny
DB helpers that operate ONLY on the app's own users table (plan column).

Square billing (Phase 2) will call set_plan() from billing.py/webhooks.
"""

PRICING = {
    "teas_monthly":  {"name": "TEAS Monthly",  "price_cents": 1299, "interval": "month", "app": "teas"},
    "nclex_monthly": {"name": "NCLEX Monthly", "price_cents": 1999, "interval": "month", "app": "nclex"},
    "fcle_monthly":  {"name": "FCLE Monthly",  "price_cents": 999,  "interval": "month", "app": "fcle"},
}
# NO teas_90day, NO annual, NO bundles in v1 (PRICING.md corrected Sep 5, 2026).

FREE_DAILY_QUESTIONS = 10
FREE_DAILY_AI = 5
PAID_DAILY_AI = 100


# ---------------------------------------------------------------------------
# Pure entitlement checks (no DB)
# ---------------------------------------------------------------------------

def is_premium(plan):
    """True when plan names a paid plan in PRICING."""
    return plan in PRICING


def questions_remaining(plan, used):
    """Remaining free questions today. None = unlimited (paid plan)."""
    if is_premium(plan):
        return None
    return max(0, FREE_DAILY_QUESTIONS - used)


def ai_remaining(plan, used):
    """Remaining AI-tutor calls today. Paid plans get PAID_DAILY_AI."""
    if is_premium(plan):
        return max(0, PAID_DAILY_AI - used)
    return max(0, FREE_DAILY_AI - used)


def plan_for_app(app):
    """PRICING key for the given app slug ('teas' | 'fcle' | 'nclex')."""
    for key, info in PRICING.items():
        if info["app"] == app:
            return key
    return None


# ---------------------------------------------------------------------------
# DB helpers — explicit sqlite path, operate ONLY on users(email, plan)
# ---------------------------------------------------------------------------

def set_plan(db_path, email, plan):
    """UPDATE users SET plan=? WHERE lower(email)=lower(?). Returns rowcount.
    Caller guarantees the app's users table has the plan column."""
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


# ---------------------------------------------------------------------------
# CLI: python3 platform_lib.py grant <db_path> <email> <plan>
#      python3 platform_lib.py status <db_path> <email>
# ---------------------------------------------------------------------------

def _cli(argv):
    if len(argv) >= 4 and argv[1] == "grant":
        db_path, email, plan = argv[2], argv[3].lower(), argv[4]
        if plan not in PRICING:
            print(f"unknown plan '{plan}' (valid: {', '.join(PRICING)})")
            return 2
        rc = set_plan(db_path, email, plan)
        print(f"granted {plan} to {email}: {rc} row(s) updated")
        return 0
    if len(argv) == 4 and argv[1] == "status":
        db_path, email = argv[2], argv[3].lower()
        print(f"{email}: plan={get_plan(db_path, email)}")
        return 0
    print(__doc__)
    print("usage: platform_lib.py grant <db_path> <email> <plan>")
    print("       platform_lib.py status <db_path> <email>")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(_cli(sys.argv))
