# FCLE Study Buddy — Deployment Runbook (Sep 2026)

Source of truth: `MuataSr/fcle-study-app` (GitHub, private). Deploy by git clone — no rsync of working trees.

## Target

- Dedicated study-apps droplet (see `~/.hermes/workspace/FCLE-DEPLOYMENT-PLAN-v2.md`)
- Nginx → gunicorn :5002 → Flask app.py
- `fcle.mu2.solutions` (HTTPS via Certbot)

## First deploy (root on droplet)

```bash
# 1. Clone
git clone git@github.com:MuataSr/fcle-study-app.git /opt/fcle-study-app   # needs repo Deploy Key
cd /opt/fcle-study-app

# 2. Venv + deps
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# 3. Env (never commit)
cat > .env << 'EOF'
FLASK_SECRET=<64-hex>
FLASK_ENV=production
# Beta: leave FCLE_FREE_LAUNCH=1 (default) — flip to 0 only at paid launch
EOF
chmod 600 .env

# 4. First boot (creates fresh user_progress.db + schema)
venv/bin/python -c "import db; db.init_db(); db.init_diagnostic_table()"

# 5. systemd unit
cat > /etc/systemd/system/fcle-study-app.service << 'EOF'
[Unit]
Description=FCLE Study Buddy (gunicorn)
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/fcle-study-app
EnvironmentFile=/opt/fcle-study-app/.env
ExecStart=/opt/fcle-study-app/venv/bin/gunicorn -c gunicorn.conf.py wsgi:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload && systemctl enable --now fcle-study-app

# 6. Nginx vhost (see plan; proxy to 127.0.0.1:5002), then certbot
```

## Code update (post-launch)

```bash
cd /opt/fcle-study-app && git pull && systemctl restart fcle-study-app
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://fcle.mu2.solutions/
```

## Notes

- `data/user_progress.db` is gitignored + created fresh at first boot — never copy a dev DB to prod.
- Quiz state is SQLite-backed (`active_quizzes`) → gunicorn workers=2 is safe.
- Backup cron: nightly sqlite3 `.backup` of user_progress.db + integrity check (mirror ORDER pattern), keep 14 days.
- Deploy Key (read-only) on GitHub: Settings → Deploy keys → paste droplet `~/.ssh/id_ed25519.pub`.


## Pilot signup cap (RC #1)

The first release candidate is intentionally capped so the $6 droplet can never be
overrun. All knobs live in `/opt/fcle-study-app/.env` — no code change needed to
adjust, just edit and `systemctl restart fcle-study-app`.

| Variable | Purpose |
|---|---|
| `PILOT_SIGNUP_CAP` | Max real students. `0` or unset = uncapped. Pilot value: `125`. |
| `PILOT_INTERNAL_EMAILS` | Comma-separated emails that never consume a seat (founder + our test accounts). |
| `PILOT_BYPASS_KEY` | Secret; `?bypass=<key>` on `/signup` lets us register past the cap. |
| `PILOT_ADMIN_KEY` | Secret; `/admin/waitlist?key=<key>` lists the waitlist (`&format=csv` to export). |

Behaviour:
- Seats count **registered, non-anonymous users with an email**, minus
  `PILOT_INTERNAL_EMAILS`. Anonymous/test rows never count.
- The check runs **server-side and race-safe** (single `BEGIN IMMEDIATE` lock), so
  two simultaneous signups cannot both take the last seat.
- When full, `/signup` shows the pilot-full state with a waitlist form
  (`POST /waitlist`) instead of the registration form. No dead end.
- Waitlist entries are stored in the `waitlist` table; outreach is manual.

Deploy: mirror → M7 (`git commit`/`push`) → droplet `git pull && systemctl restart fcle-study-app`.
