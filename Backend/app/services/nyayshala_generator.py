from __future__ import annotations
import os
import json
from datetime import date
from typing import List, Dict
from app.services.llm_client import LLMClient

NYAY_DIR = os.path.join(".data", "nyayshala")
os.makedirs(NYAY_DIR, exist_ok=True)

FIELDS = ["contract", "criminal", "family", "ip", "tax", "property"]

PROMPT = (
    "You are NyaySaathi. Generate a concise 'law nugget' for the FIELD domain in India. "
    "Return 1-2 paragraphs (<= 120 words) with a short title and a couple of references to public sources (names/URLs). "
    "Keep it educational, not legal advice."
)


def _path_for(d: date) -> str:
    return os.path.join(NYAY_DIR, f"{d.isoformat()}.json")


def generate_for_day(d: date) -> List[Dict]:
    client = LLMClient()
    items: List[Dict] = []
    for field in FIELDS:
        msgs = [
            {"role": "system", "content": "You write concise legal learning snippets."},
            {"role": "user", "content": PROMPT.replace("FIELD", field)},
        ]
        text = client.generate(msgs, temperature=0.4)
        title = text.split("\n", 1)[0][:80]
        items.append({
            "field": field,
            "title": title,
            "content": text,
        })
    # persist
    with open(_path_for(d), "w", encoding="utf-8") as f:
        json.dump({"date": d.isoformat(), "items": items}, f, ensure_ascii=False, indent=2)
    return items


def read_for_day(d: date) -> Dict | None:
    p = _path_for(d)
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)
