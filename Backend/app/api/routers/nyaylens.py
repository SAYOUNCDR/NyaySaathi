from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi import Body
import uuid
from typing import Dict
from app.services.doc_ingestion import save_upload, ingest_file
from app.services.embedding import embed_query, get_embedder
from app.services.vector_store import QdrantStore
from app.services.llm_client import LLMClient
from sse_starlette.sse import EventSourceResponse
from app.services.lens_status import set_status, get_status, start_progress, set_progress, complete

router = APIRouter(prefix="/nyaylens", tags=["nyaylens"])


@router.post("/upload")
async def lens_upload(file: UploadFile = File(...), title: str | None = Form(None), tasks: BackgroundTasks = None):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")
    lens_id = str(uuid.uuid4())
    collection = f"lens_{lens_id}"
    content = await file.read()
    saved = save_upload(content, file.filename)
    start_progress(lens_id, title=title or file.filename)

    def _bg():
        try:
            def _cb(update: Dict):
                # update has keys like stage, total_chunks, ingested, percent
                set_progress(lens_id, **update)

            ingest_file(saved, title=title, collection=collection, progress_cb=_cb)
            complete(lens_id)
        except Exception as e:
            set_status(lens_id, "error", str(e))

    if tasks is not None:
        tasks.add_task(_bg)
    else:
        _bg()

    # return lens id immediately
    return {"ok": True, "lens_id": lens_id}


@router.post("/{lens_id}/ask")
async def lens_ask(lens_id: str, query: str = Body(..., embed=True), top_k: int = 6):
    dim = get_embedder().get_sentence_embedding_dimension()
    store = QdrantStore(collection=f"lens_{lens_id}")
    store.ensure_collection(dim)
    qvec = embed_query(query)
    results = store.search(qvec, top_k=top_k)
    # Simple return for now; streaming answer can reuse chat path later
    return {"matches": results}


@router.get("/{lens_id}/stream")
def lens_stream(lens_id: str, query: str):
    dim = get_embedder().get_sentence_embedding_dimension()
    store = QdrantStore(collection=f"lens_{lens_id}")
    store.ensure_collection(dim)
    qvec = embed_query(query)
    contexts = store.search(qvec, top_k=6)

    header = (
        "You are NyaySaathi. Use ONLY the provided document context for this user-uploaded file. "
        "Cite as [doc_id:chunk_id]. If unsure, say you don't know."
    )
    ctx_text = "\n\n".join(f"[{c.get('doc_id','?')}:{c.get('chunk_id','?')}] {c['text']}" for c in contexts) or "(no context)"
    messages = [
        {"role": "system", "content": header},
        {"role": "user", "content": f"Context:\n{ctx_text}\n\nQuestion: {query}"},
    ]

    def generator():
        llm = LLMClient()
        for token in llm.stream_generate(messages):
            yield {"event": "token", "data": token}
        yield {"event": "end", "data": "[DONE]"}

    return EventSourceResponse(generator())


@router.get("/{lens_id}/status")
def lens_status(lens_id: str):
    return get_status(lens_id)


@router.post("/{lens_id}/critique")
async def lens_critique(lens_id: str, instructions: str | None = Body(None, embed=True)):
    # Placeholder: returns that critique will be implemented in next iteration
    return {"ok": True, "lens_id": lens_id, "status": "critique-not-implemented-yet"}


@router.delete("/{lens_id}")
async def lens_delete(lens_id: str):
    # Optional: drop collection
    try:
        QdrantStore(collection=f"lens_{lens_id}").client.delete_collection(collection_name=f"lens_{lens_id}")
    except Exception:
        pass
    return {"ok": True, "deleted": lens_id}
