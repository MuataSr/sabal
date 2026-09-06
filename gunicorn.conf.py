# gunicorn config — Sabal FCLE Exam Prep
# Multi-worker safe: quiz state lives in SQLite (active_quizzes table), not RAM.
bind = "127.0.0.1:5002"
workers = 2
threads = 4
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
