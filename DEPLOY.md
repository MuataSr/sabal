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


## Signup cap — OFF by default (Sabal is 100% OER)

Sabal is a free, openly licensed educational resource with no revenue model, so
**no student is ever refused a seat.** `PILOT_SIGNUP_CAP` defaults to unset/`0`
(uncapped) and production runs uncapped. The seat machinery survives only as an
emergency brake for the $6 droplet, and the page it shows when it is on speaks
about server capacity — never about pilot cohorts or reserved seats.

All knobs live in `/opt/fcle-study-app/.env` — no code change needed to
adjust, just edit and `systemctl restart fcle-study-app`. Setting a cap is a
deliberate, temporary act during an incident, not a normal operating state.

| Variable | Purpose |
|---|---|
| `PILOT_SIGNUP_CAP` | Max real students. `0` or unset = uncapped, which is the OER default and the prod setting. |
| `PILOT_INTERNAL_EMAILS` | Comma-separated emails that never consume a seat (founder + our test accounts). |
| `PILOT_BYPASS_KEY` | Secret; `?bypass=<key>` on `/signup` lets us register past the cap. |
| `PILOT_ADMIN_KEY` | Secret; `/admin/waitlist?key=<key>` lists the waitlist (`&format=csv` to export). |

Behaviour:
- Seats count **registered, non-anonymous users with an email**, minus
  `PILOT_INTERNAL_EMAILS`. Anonymous/test rows never count.
- The check runs **server-side and race-safe** (single `BEGIN IMMEDIATE` lock), so
  two simultaneous signups cannot both take the last seat.
- When (and only when) a cap is set and reached, `/signup` shows a capacity
  notice with a waitlist form (`POST /waitlist`) instead of the registration
  form. No dead end.
- Waitlist entries are stored in the `waitlist` table; outreach is manual.

Deploy: mirror → M7 (`git commit`/`push`) → droplet `git pull && systemctl restart fcle-study-app`.


## Instrumentation — the wrinkle loop and the funnel

Both views are gated by `PILOT_ADMIN_KEY` in the query string and are unlinked
from the app.

| Route | What it shows |
|---|---|
| `/admin/reports?key=<key>` | Student-reported question problems. `&status=open\|resolved\|all`, `&format=csv` exports. `POST` with `resolve=<id>` marks one resolved. |
| `/admin/funnel?key=<key>` | Discovery-to-product funnel: page counts, accounts, onboarding, first quiz, first answer, returns, 7-day actives, `?src=` attribution, open reports. |
| `/admin/waitlist?key=<key>` | Waitlist entries (only meaningful while a cap is set). |

- **Question reports** come from the collapsible "Something wrong with this
  question?" control on the quiz feedback page (`POST /report-question`, login
  required). Each row stores the reason, the student's note, the domain and
  **the option the student picked** — a "the marked answer looks wrong" report
  cannot be diagnosed afterwards without it. Table: `question_reports`.
- **The funnel is derived, never tracked.** Every number is computed from rows
  the app already writes (`users`, `quiz_sessions`, `answers`); no new
  per-student tracking was added.
- **Page counters are aggregate and identifier-free:** `page_views` holds only
  `(day, page, hits)` for `landing`, `signup` and `registered`. No IP, no
  cookie, no user id, nothing per visitor. This is what makes "nobody came"
  separable from "they came, hit a wall, and left". The in-app privacy promise
  ("we don't sell or share anyone's information") still holds.


## Crawl surfaces — search and link previews (2026-10-14)

- `/robots.txt` and `/sitemap.xml` are served by the app. The public origin is
  **pinned** (`PUBLIC_BASE_URL`, env override `SABAL_PUBLIC_BASE_URL`, default
  `https://fcle.mu2.solutions`) instead of read from the request, because nginx
  terminates TLS and the app itself sees `http`.
- Every student page is `Disallow`ed on purpose and the sitemap lists only `/`,
  `/signup` and `/login`. **Never add a student, results or admin path** to
  either surface.
- The landing head carries canonical + Open Graph + twitter card +
  `WebApplication`/`FAQPage` JSON-LD. **`og:title` and `og:description` must stay
  byte-identical to the approved `<title>` and meta description**: a share tag is
  not a place to smuggle in a new claim or a new number, and a test enforces that
  along with the "FCLE-style" wording rule and the floor-not-exact count rule.
- `og:image` is `static/img/sabal-og-card.png` (1200x630), derived from the
  approved logo card. The source card is 1280x640 with a portrait mark, so the
  mark is centred on the card's own background rather than re-drawn.
- **Indexing itself is not done by any of this.** Submitting the sitemap to
  Google Search Console needs Mister K's own account (or a DNS TXT record on the
  domain), and that is his call.


## OER posture (2026-10-14)

Sabal is 100% open educational resource, permanently: no paid edition, no
paywall, no revenue. Code is Apache-2.0, content is CC BY-NC-SA 4.0. Any public
copy that describes a paid tier, a pilot cohort, a seat count or a "limited
time" frame is wrong and must be corrected on sight.
