from __future__ import annotations
import os
import json
from typing import Dict, List

META_DIR = os.path.join('.data', 'meta')
META_PATH = os.path.join(META_DIR, 'docs.json')

os.makedirs(META_DIR, exist_ok=True)


def _load() -> Dict:
    if not os.path.exists(META_PATH):
        return {"documents": []}
    with open(META_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(data: Dict):
    with open(META_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_document(doc: Dict):
    data = _load()
    # replace if same doc_id
    data['documents'] = [d for d in data['documents'] if d.get('doc_id') != doc.get('doc_id')]
    data['documents'].append(doc)
    _save(data)


def list_documents() -> List[Dict]:
    return _load().get('documents', [])


def delete_document(doc_id: str) -> bool:
    data = _load()
    before = len(data.get('documents', []))
    data['documents'] = [d for d in data['documents'] if d.get('doc_id') != doc_id]
    _save(data)
    return len(data['documents']) < before
