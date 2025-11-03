from fastapi import APIRouter, Body, Query
from sse_starlette.sse import EventSourceResponse
from app.services.rag_engine import answer

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/stream")
def stream_chat(query: str = Query(..., min_length=1)):
    def event_gen():
        for token in answer(query, stream=True):
            yield {"event": "token", "data": token}
        yield {"event": "end", "data": "[DONE]"}

    return EventSourceResponse(event_gen())


@router.post("/ask")
def ask_chat(query: str = Body(..., embed=True)):
    text = answer(query, stream=False)
    return {"answer": text}
