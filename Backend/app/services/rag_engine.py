from typing import List, Dict, Iterable
from app.services.llm_client import LLMClient
from app.services.embedding import embed_query, get_embedder
from app.services.vector_store import QdrantStore

# Placeholder retrieval to be replaced by Qdrant

def retrieve_context(query: str, top_k: int = 6) -> List[Dict]:
    # Embed query and search Qdrant corpus collection
    # Ensure collection exists based on current embedder dim
    dim = get_embedder().get_sentence_embedding_dimension()
    store = QdrantStore()
    store.ensure_collection(dim)
    qvec = embed_query(query)
    results = store.search(qvec, top_k=top_k)
    return results


def build_prompt(user_query: str, contexts: List[Dict]) -> list[dict]:
    header = (
        "You are NyaySaathi, a helpful legal assistant.\n"
        "Answer using ONLY the provided context. Cite sources as [doc_id:chunk_id]. "
        "If unsure, say you don't know."
    )
    ctx_text = "\n\n".join(
        f"[{c.get('doc_id','?')}:{c.get('chunk_id','?')}] {c['text']}" for c in contexts
    ) or "(no context)"
    system = {"role": "system", "content": header}
    user = {"role": "user", "content": f"Context:\n{ctx_text}\n\nQuestion: {user_query}"}
    return [system, user]


def answer(query: str, stream: bool = True) -> Iterable[str] | str:
    contexts = retrieve_context(query)
    msgs = build_prompt(query, contexts)
    llm = LLMClient()
    if stream:
        return llm.stream_generate(msgs)
    return llm.generate(msgs)
