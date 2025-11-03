from __future__ import annotations
import os
import uuid
import hashlib
from typing import List, Dict
import fitz  # PyMuPDF
from docx2python import docx2python
from app.core.config import settings
from app.utils.text_splitter import split_text
from app.services.embedding import get_embedder
from app.services.vector_store import QdrantStore


UPLOAD_DIR = settings.storage_dir

os.makedirs(UPLOAD_DIR, exist_ok=True)


def _checksum(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_pdf(path: str) -> str:
    doc = fitz.open(path)
    texts: List[str] = []
    for page in doc:
        texts.append(page.get_text())
    return "\n".join(texts)


def _read_docx(path: str) -> str:
    with docx2python(path) as doc:
        parts: List[str] = []
        for sec in doc.body:
            for para in sec:
                parts.append(" ".join(para))
        return "\n".join(parts)


def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text(path: str, mimetype: str | None = None) -> str:
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".pdf":
            return _read_pdf(path)
        if ext in (".docx",):
            return _read_docx(path)
        if ext in (".txt", ".md"):
            return _read_txt(path)
    except Exception as e:
        raise RuntimeError(f"Failed to parse {path}: {e}")
    raise RuntimeError(f"Unsupported file type: {ext}")


def ingest_file(
    saved_path: str,
    title: str | None = None,
    doc_id: str | None = None,
    collection: str | None = None,
    progress_cb: callable | None = None,
    batch_size: int = 64,
) -> Dict:
    """Parse -> split -> embed -> upsert into Qdrant in batches with optional progress callback.

    progress_cb, if provided, will be called with a dict including fields like:
    { 'stage': 'extract' | 'split' | 'index' | 'done', 'total_chunks': int, 'ingested': int, 'percent': int }
    """
    # Extract
    if progress_cb:
        progress_cb({"stage": "extract"})
    text = extract_text(saved_path)

    # Split
    chunks = split_text(text)
    total_chunks = len(chunks)
    if progress_cb:
        progress_cb({"stage": "split", "total_chunks": total_chunks, "ingested": 0, "percent": 0})

    # Prepare embedding and collection
    embedder = get_embedder()
    vector_size = embedder.get_sentence_embedding_dimension()
    store = QdrantStore(collection=collection)
    store.ensure_collection(vector_size)

    if not doc_id:
        doc_id = str(uuid.uuid4())
    checksum = _checksum(saved_path)

    # Embed + upsert in batches, reporting progress
    ingested = 0
    title_value = title or os.path.basename(saved_path)
    for start in range(0, total_chunks, batch_size):
        end = min(start + batch_size, total_chunks)
        batch_chunks = chunks[start:end]
        # Embed this batch
        vectors = embedder.encode(
            batch_chunks,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        ).tolist()

        # Build ids/payloads for this batch
        ids: List[str] = []
        payloads: List[Dict] = []
        for i_rel, (chunk, vec) in enumerate(zip(batch_chunks, vectors)):
            idx = start + i_rel
            # Qdrant point id must be an unsigned integer or a UUID. Use UUID per chunk.
            point_id = str(uuid.uuid4())
            ids.append(point_id)
            payloads.append(
                {
                    "doc_id": doc_id,
                    "chunk_id": idx,
                    "text": chunk,
                    "title": title_value,
                    "source_path": saved_path,
                    "checksum": checksum,
                }
            )

        # Upsert this batch
        store.upsert_points(ids, vectors, payloads)

        ingested = end
        if progress_cb:
            percent = int(max(0, min(100, round((ingested / max(1, total_chunks)) * 100))))
            progress_cb({
                "stage": "index",
                "total_chunks": total_chunks,
                "ingested": ingested,
                "percent": percent,
            })

    if progress_cb:
        progress_cb({"stage": "done", "total_chunks": total_chunks, "ingested": total_chunks, "percent": 100})

    return {
        "doc_id": doc_id,
        "title": title_value,
        "chunks": total_chunks,
        "checksum": checksum,
        "path": saved_path,
    }


def save_upload(file_bytes: bytes, filename: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    # disambiguate
    base, ext = os.path.splitext(filename)
    safe_base = base.replace(" ", "_")
    target = os.path.join(UPLOAD_DIR, f"{safe_base}{ext}")
    i = 1
    while os.path.exists(target):
        target = os.path.join(UPLOAD_DIR, f"{safe_base}_{i}{ext}")
        i += 1
    with open(target, "wb") as f:
        f.write(file_bytes)
    return target
