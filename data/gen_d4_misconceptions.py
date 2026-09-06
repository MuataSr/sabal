#!/usr/bin/env python3
"""Generate 50 college-level FCLE Domain 4 misconceptions via Z.AI API."""

import json
import requests
import time

API_KEY = "REMOVED-ROTATED-KEY"
BASE_URL = "https://api.z.ai/api/coding/paas/v4"
MODEL = "glm-5.1"
OUTPUT_FILE = "/home/muatasr/.nanobot/workspace/fcle-study-app/data/misconceptions_d4.json"

# Existing misconceptions to avoid overlap (key phrases from DB)
EXISTING_PHRASES = [
    "Marbury v. Madison established judicial review",
    "Brown v. Board of Education immediately ended segregation",
    "Civil Rights Act of 1964 was passed because President Johnson",
    "Voting Rights Act of 1965 wasn't really necessary",
    "Miranda rights are just a formality",
    "Mapp v. Ohio just said police need a warrant",
    "Tinker v. Des Moines said students",
    "Engel v. Vitale banned all prayer",
    "McCulloch v. Maryland is just about a bank",
    "Citizens United v. FEC means corporations",
    "Bill of Rights always applied to state governments",
    "Selective incorporation means the Supreme Court picked",
    "If you can't afford a lawyer",
    "Schenck v. United States created",
    "Americans with Disabilities Act just means",
]

TOPICS = [
    "Supreme Court cases (Marbury v Madison, Brown v Board, Roe v Wade, McCulloch v Maryland, etc.)",
    "Civil rights legislation (Civil Rights Act 1964, Voting Rights Act 1965, ADA)",
    "14th Amendment incorporation doctrine",
    "1st Amendment cases (free speech, religion, press — Tinker, Engel, Lemon test, Brandenburg)",
    "Criminal procedure cases (Miranda, Gideon, Mapp, Escobedo, exclusionary rule)",
    "Executive orders and actions (New Deal, Great Society, War Powers, Japanese internment)",
    "New Deal and Great Society programs",
]

SYSTEM_PROMPT = """You are an expert in American constitutional law and civic education. Generate college-level misconceptions for the Florida Civic Literacy Exam (FCLE), Domain 4: Landmark Impact."""

def build_user_prompt(batch_num, topics_subset):
    return f"""Generate exactly 10 college-level misconceptions about FCLE Domain 4: Landmark Impact.

DOMAIN: Landmark Impact — Impact of landmark Supreme Court cases, landmark legislation, and executive actions on American law and society.

FOCUS TOPICS FOR THIS BATCH:
{chr(10).join(f'- {t}' for t in topics_subset)}

REQUIREMENTS:
1. Each misconception must be a plausible wrong belief a COLLEGE student might hold — deeper than middle school civics
2. Cover legal precedent, constitutional interpretation, incorporation doctrine, separation of powers
3. Misconception text: 40-120 characters. Correction text: 80-200 characters.
4. Difficulty: "hard" for all
5. Do NOT duplicate any of these existing misconceptions:
{chr(10).join(f'  - {p}' for p in EXISTING_PHRASES)}

6. Do NOT use these overly simple formats — aim for college-level nuance:
   - No "X just means Y" simplifications
   - No "X immediately ended Y" — discuss gradual implementation
   - No "X is just about Y" dismissals
7. Vary the topics — don't cluster on one case or one theme

OUTPUT FORMAT: Return ONLY a valid JSON array, no markdown fences, no explanation. Each object:
{{"benchmark_code": "FCLE", "misconception": "...", "correction": "...", "difficulty": "hard", "fcle_domain": 4}}

This is batch {batch_num}. Generate exactly 10 items."""


def call_api(batch_num, topics_subset, retries=2):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(batch_num, topics_subset)},
        ],
        "temperature": 0.8,
        "max_tokens": 4000,
    }
    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                f"{BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            # Strip markdown fences if present
            if content.startswith("```"):
                content = content.split("\n", 1)[1] if "\n" in content else content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            data = json.loads(content)
            if not isinstance(data, list):
                print(f"  Warning: expected list, got {type(data)}. Wrapping.")
                data = [data]
            return data
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt == retries:
                raise
            time.sleep(3)


def validate_item(item):
    assert "misconception" in item, "missing misconception"
    assert "correction" in item, "missing correction"
    assert 40 <= len(item["misconception"]) <= 150, f"misconception length {len(item['misconception'])}"
    assert 80 <= len(item["correction"]) <= 250, f"correction length {len(item['correction'])}"
    item.setdefault("benchmark_code", "FCLE")
    item.setdefault("difficulty", "hard")
    item.setdefault("fcle_domain", 4)
    return item


def main():
    all_items = []

    # 5 batches of 10 = 50
    batches = [
        # Batch 1: Supreme Court cases + incorporation
        [TOPICS[0], TOPICS[2]],
        # Batch 2: 1st Amendment cases
        [TOPICS[3]],
        # Batch 3: Criminal procedure
        [TOPICS[4]],
        # Batch 4: Civil rights legislation
        [TOPICS[1]],
        # Batch 5: Executive actions + New Deal/Great Society
        [TOPICS[5], TOPICS[6]],
    ]

    for i, topics in enumerate(batches, 1):
        print(f"Generating batch {i}/5 (topics: {', '.join(topics[:30])}...)...")
        items = call_api(i, topics)
        print(f"  Got {len(items)} items")
        for item in items:
            try:
                validated = validate_item(item)
                all_items.append(validated)
            except AssertionError as e:
                print(f"  Skipping invalid item: {e}")
        time.sleep(2)

    # Deduplicate by misconception text
    seen = set()
    unique = []
    for item in all_items:
        key = item["misconception"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    print(f"\nTotal generated: {len(all_items)}, unique: {len(unique)}")

    # If we have fewer than 50, generate more
    while len(unique) < 50:
        needed = 50 - len(unique)
        batch_topics = [TOPICS[len(unique) % len(TOPICS)]]
        print(f"Generating补充 batch ({needed} needed)...")
        items = call_api(99, batch_topics)
        for item in items:
            if len(unique) >= 50:
                break
            try:
                validated = validate_item(item)
                key = validated["misconception"].lower().strip()
                if key not in seen:
                    seen.add(key)
                    unique.append(validated)
            except AssertionError as e:
                print(f"  Skipping: {e}")
        time.sleep(2)

    # Trim to exactly 50
    final = unique[:50]
    print(f"Final count: {len(final)}")

    # Validate all fields present
    for i, item in enumerate(final):
        for field in ["benchmark_code", "misconception", "correction", "difficulty", "fcle_domain"]:
            assert field in item, f"Item {i} missing field: {field}"

    with open(OUTPUT_FILE, "w") as f:
        json.dump(final, f, indent=2)

    print(f"Saved {len(final)} misconceptions to {OUTPUT_FILE}")

    # Print summary
    print("\n--- Sample items ---")
    for item in final[:3]:
        print(f"  M: {item['misconception'][:80]}...")
        print(f"  C: {item['correction'][:100]}...")
        print()


if __name__ == "__main__":
    main()
