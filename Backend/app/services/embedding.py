from __future__ import annotations
from sentence_transformers import SentenceTransformer
import torch
from functools import lru_cache
from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedder() -> SentenceTransformer:
    device = settings.embed_device if hasattr(settings, "embed_device") else ("cuda" if torch.cuda.is_available() else "cpu")
    model_name = getattr(settings, "embed_model", "BAAI/bge-m3")
    model = SentenceTransformer(model_name, device=device, trust_remote_code=True)
    return model


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedder()
    embs = model.encode(texts, batch_size=64, convert_to_numpy=True, show_progress_bar=False, normalize_embeddings=True)
    return embs.tolist()


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
