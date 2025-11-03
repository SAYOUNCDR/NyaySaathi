from __future__ import annotations
from fastapi import APIRouter
from app.services.llm_client import LLMClient
from app.services.vector_store import QdrantStore
from app.services.embedding import get_embedder

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ready")
def ready():
    # Check LLM init
    ok_llm = True
    try:
        _ = LLMClient()
    except Exception:
        ok_llm = False

    # Check Qdrant
    ok_qdrant = True
    try:
        dim = get_embedder().get_sentence_embedding_dimension()
        QdrantStore().ensure_collection(dim)
    except Exception:
        ok_qdrant = False

    return {"llm": ok_llm, "qdrant": ok_qdrant, "ready": ok_llm and ok_qdrant}
