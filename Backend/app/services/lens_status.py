from __future__ import annotations
import os
import json
import time
from typing import Dict, Any

STATUS_DIR = os.path.join('.data', 'lens')
STATUS_PATH = os.path.join(STATUS_DIR, 'status.json')

os.makedirs(STATUS_DIR, exist_ok=True)


def _load() -> Dict[str, Any]:
    if not os.path.exists(STATUS_PATH):
        return {}
    with open(STATUS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(data: Dict[str, Any]):
    with open(STATUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def start_progress(lens_id: str, title: str | None = None):
    """Initialize progress record for a lens ingestion."""
    data = _load()
    now = time.time()
    data[lens_id] = {
        "status": "processing",
        "stage": "start",
        "title": title,
        "total_chunks": 0,
        "ingested": 0,
        "percent": 0,
        "started_at": now,
        "updated_at": now,
    }
    _save(data)


def set_status(lens_id: str, status: str, message: str | None = None):
    data = _load()
    rec = data.get(lens_id, {})
    rec.update({
        "status": status,
        **({"message": message} if message else {}),
        "updated_at": time.time(),
    })
    data[lens_id] = rec
    _save(data)


def set_progress(lens_id: str, **fields):
    """Update progress fields and compute percent/eta when possible."""
    data = _load()
    rec = data.get(lens_id, {"status": "processing", "started_at": time.time()})
    rec.update(fields)
    now = time.time()
    rec["updated_at"] = now

    total = rec.get("total_chunks") or 0
    ing = rec.get("ingested") or 0
    if total > 0:
        # Percent is based on ingested/total
        rec["percent"] = int(max(0, min(100, round((ing / total) * 100))))
        # Simple ETA based on linear rate
        started = rec.get("started_at", now)
        elapsed = max(0.001, now - started)
        if ing > 0:
            rate = ing / elapsed  # chunks per second
            remaining = max(0, total - ing)
            eta = int(round(remaining / rate)) if rate > 0 else None
        else:
            eta = None
        rec["eta_seconds"] = eta
    data[lens_id] = rec
    _save(data)


def complete(lens_id: str):
    data = _load()
    rec = data.get(lens_id, {})
    rec.update({
        "status": "ready",
        "stage": "done",
        "percent": 100,
        "updated_at": time.time(),
    })
    data[lens_id] = rec
    _save(data)


def get_status(lens_id: str) -> Dict[str, Any]:
    data = _load()
    return data.get(lens_id, {"status": "unknown"})
