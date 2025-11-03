# NyaySaathi Backend (FastAPI)

Minimal FastAPI backend with SSE chat, pluggable LLM (OpenAI GPT-4o-mini / Google Gemini 2.0 Flash), and stubs for RAG.

## Quickstart (Windows PowerShell)

```powershell
cd e:\Hackathons\AIU1\NyaySaathi\Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Set your API key(s) in .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Optional (faster embeddings on GPU) – install CUDA PyTorch before sentence-transformers:
```powershell
# Close venv if open, then re-activate; install CUDA 12.1 build of torch
pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio
```

Optional infra:
```powershell
docker compose up -d
```

## Env
See `.env.example` for provider selection and CORS settings.

## Endpoints
- GET `/health/live` – liveness
- GET `/health/ready` – readiness (LLM + Qdrant)
- GET `/api/chat/stream?query=...` – SSE streaming tokens
- POST `/api/chat/ask` – non-stream response
- POST `/api/admin/documents` – upload + ingest into corpus

## Next
- Qdrant retrieval + ingestion
- Admin uploads, NyayLens, NyayShala, Auth
