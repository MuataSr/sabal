#!/usr/bin/env python3
"""Generate 50 college-level FCLE Domain 3 misconceptions via Z.AI API."""

import json, requests, sys, os
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import misconception_codes  # noqa: E402  real SS.7.CG codes; refuses the "FCLE" placeholder

DOMAIN = 3

def _env_key(name):
    """Read a credential from the environment, falling back to a repo-root .env.
    Credentials are never committed - see .env.example."""
    v = os.environ.get(name, "")
    if not v and os.path.exists(".env"):
        for _line in open(".env"):
            if _line.strip().startswith(name + "="):
                v = _line.split("=", 1)[1].strip().strip("\"'")
                break
    if not v:
        raise SystemExit(
            f"{name} is not set. Copy .env.example to .env and fill it in, "
            f"or export {name}."
        )
    return v

API_KEY = _env_key("ZAI_API_KEY")
BASE_URL = "https://api.z.ai/api/coding/paas/v4/chat/completions"
MODEL = "glm-5.1"
OUTPUT = "/home/muatasr/.nanobot/workspace/fcle-study-app/data/misconceptions_d3.json"

SYSTEM = """You are an expert in American political thought for FCLE Domain 3: Founding Documents.

Generate COLLEGE-LEVEL misconceptions covering deeper political theory:
- Madison's extended republic, pure democracy vs republic, "ambition counteracts ambition"
- Separation of powers vs checks and balances, compound republic
- Commerce Clause, Necessary and Proper, Supremacy Clause debates
- Enumerated vs implied powers, Lockean vs Hobbesian social contract
- Montesquieu's influence, Virginia Plan vs New Jersey Plan
- Great Compromise, Electoral College rationale, three-fifths as power calculation
- Brutus essays, Anti-Federalist judicial/army concerns, Federalist as propaganda
- Northwest Ordinance, intentional Articles weakness, requisition failure
- Ratification strategy, Bill of Rights as compromise, Massachusetts turning point

Rules: misconception 40-120 chars, correction 80-200 chars. Output ONLY JSON array.

Every item MUST carry a real standard code. "FCLE" is NOT a code and is rejected.
Choose the ONE standard the misconception is really about, from this list only:
""" + misconception_codes.prompt_block(DOMAIN)

BATCHES = [
    "Declaration of Independence: Lockean theory depth, consent of governed vs Hobbesian, Jefferson's borrowing, Declaration as philosophy not charter, grievances as legal indictment, self-evident truths epistemology",
    "Articles of Confederation: Intentional weakness as philosophy, Northwest Ordinance achievement, requisition failure, no executive as deliberate, foreign policy weakness, Confederation Congress limits",
    "Constitution structure: Commerce Clause, Necessary and Proper, enumerated vs implied powers, Supremacy Clause, Article V difficulty, We the People framing, preamble's role",
    "Federalist No. 10: Extended republic, faction control through size, pure democracy vs republic, large republic cures factionalism, pluralism, representation filtering passion",
    "Federalist No. 51: Ambition counteracts ambition, separation vs checks distinction, compound republic, government controlling governed then itself, institutional pessimism about power",
    "Anti-Federalists: Brutus on consolidation, judicial tyranny, standing armies, no Bill of Rights, Cato/Centinel essays, republics in small communities only",
    "Convention and Ratification: Virginia vs NJ Plan, Great Compromise, Electoral College, three-fifths power math, Federalist as propaganda, ratification strategy, Bill of Rights promise"
]

def call_api(topic, n):
    resp = requests.post(BASE_URL, headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Generate exactly {n} misconceptions.\nFocus: {topic}\nJSON array: objects with misconception, correction fields only."}],
        "temperature": 0.85, "max_tokens": 6000}, timeout=100)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        lines = content.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        content = "\n".join(lines)
    items = json.loads(content)
    for item in items:
        item["benchmark_code"] = misconception_codes.validate(
            item.get("benchmark_code"), domain=DOMAIN)
        item["difficulty"] = "hard"
        item["fcle_domain"] = 3
    return items

def main():
    all_items = []
    seen = set()
    if os.path.exists(OUTPUT):
        try:
            with open(OUTPUT) as f:
                all_items = json.load(f)
            for it in all_items:
                seen.add(it["misconception"].strip().lower()[:50])
            print(f"Resumed with {len(all_items)} items", flush=True)
        except: pass
    
    for i, topic in enumerate(BATCHES):
        need = 50 - len(all_items)
        if need <= 0: break
        n = min(8, need)
        print(f"Batch {i+1}/7 (need {need}, requesting {n})...", flush=True)
        try:
            items = call_api(topic, n)
            added = 0
            for it in items:
                k = it["misconception"].strip().lower()[:50]
                if k not in seen:
                    seen.add(k)
                    all_items.append(it)
                    added += 1
            print(f"  +{added} new (total {len(all_items)})", flush=True)
        except Exception as e:
            print(f"  ERR: {e}", flush=True)
        with open(OUTPUT, "w") as f:
            json.dump(all_items[:50], f, indent=2)
    
    all_items = all_items[:50]
    with open(OUTPUT, "w") as f:
        json.dump(all_items, f, indent=2)
    print(f"Done: {len(all_items)} items", flush=True)

if __name__ == "__main__":
    main()
