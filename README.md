# NyaySaathi — AI Legal Assistant

![NyaySaathi](public/LogoSaathi.svg)

Full documentation for developers and recruiters — a complete overview of the project, architecture, and how to run, test and extend the application.

---

## Table of contents

- Overview
- Quick demo (screenshots)
- Features
- Architecture & design
- Getting started
  - Backend (Python / FastAPI)
  - Frontend (React / Vite)
  - Docker (quick compose)
- Configuration / Environment
- API & Auth
- Data & storage notes (Qdrant / Redis)
- Development workflow
- Testing
- Deploy & production notes
- Project structure
- Contributing
- License
- Contact

---

## Overview

NyaySaathi is an AI-powered legal assistant focused on making verified Indian legal information easy to explore. The project combines a React frontend (Vite + Tailwind) and a Python FastAPI backend that integrates vector search (Qdrant), Redis for ephemeral state, and modular services for ingestion, embedding, and retrieval.

The app is intended to demonstrate an end-to-end Retrieval-Augmented Generation (RAG) flow with:

- Document ingestion and indexing
- Vector store for semantic search (Qdrant)

## NyaySaathi — Open Source Legal Assistant

![NyaySaathi](public/LogoSaathi.svg)

This repository is published as an open-source project to help developers and legal-technology enthusiasts build and extend a Retrieval-Augmented Generation (RAG) system tailored for Indian legal content. It includes a React frontend and a FastAPI backend with pluggable vector storage and LLM adapters.

This README targets contributors and maintainers: how to run the project, how to contribute, governance, and the technical details needed to extend the system.

---

## Table of contents

- Overview
- Quick demo (screenshots)
- Features
- Architecture & design
- Getting started
  - Backend (Python / FastAPI)
  - Frontend (React / Vite)
  - Docker (quick compose)
- Configuration / Environment
- API & Auth
- Data & storage notes (Qdrant / Redis)
- Development workflow
- Testing & CI
- Roadmap
- Governance & Code of Conduct
- Project structure
- How to contribute (OSS)
- License
- Contact

---

## Overview

NyaySaathi is an AI-powered legal assistant aimed at making verified Indian legal information searchable and conversational. The project demonstrates a complete ingestion -> embedding -> vector search -> LLM answer flow and is provided as an open-source reference for building RAG-based legal tools.

Key goals of the OSS project:

- Provide a clear, modular reference architecture for legal RAG systems
- Make it simple to swap the embedding model or vector store
- Encourage contributions — from docs and tests to new data connectors and UI improvements

---

## Quick demo (screenshots)

Add screenshots in `public/` and reference them here. Placeholder markup is provided for easy replacement.

- Landing / Hero UI

![Hero screenshot](Images/hero.png)

- Chat interface (desktop)

![Chat desktop](Images/chat-desktop.png)

- Chat interface (mobile)

![Chat mobile](Images/chat-mobile.png)

Replace the images above with real screenshots by placing files at `Images/hero.png`, `Images/chat-desktop.png` and `Images/chat-mobile.png` in the repository root (or update paths to where you keep screenshots). Commit the images together with the README so previews render correctly on GitHub.

---

## Features

- AI-powered conversational assistant for legal questions
- Document ingestion pipeline (upload -> parse -> embed -> index)
- Vector search powered by Qdrant (collection `corpus` by default)
- Pluggable LLM adapter (configurable via environment)
- Admin endpoints for document management
- Responsive React UI with accessibility considerations

---

## Architecture & design

- Frontend: React + Vite + Tailwind CSS — component-driven UI
- Backend: FastAPI with modular services in `app/services`
  - `vector_store.py` — qdrant client wrapper
  - `embedding.py` — embedder adapter
  - `doc_ingestion.py` — parsing and chunking utilities
  - `rag_engine.py` — retrieval + generation orchestration
- Data stores:
  - Qdrant: vector index
  - Redis: ephemeral state and caching
  - Local FS: uploads and metadata for the demo

The backend is designed for clarity and extension rather than production hardening — see `Deploy & production notes` for recommended changes.

---

## Getting started

See the `Backend/` and `Frontend/` directories for full source. Quick start using Docker Compose (recommended):

```bat
cd "C:\Users\Sayoun Parui\Desktop\NyaySaathi\Backend"
docker compose up --build -d
```

Start frontend in a second terminal:

```bat
cd "C:\Users\Sayoun Parui\Desktop\NyaySaathi\Frontend"
npm install
npm run dev
```

Start backend locally (if you prefer to run without containerising the Python code):

```bat
cd "C:\Users\Sayoun Parui\Desktop\NyaySaathi\Backend"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open the frontend (Vite) address (usually http://localhost:5173) and backend docs at http://localhost:8000/docs.

---

## Configuration / Environment

Settings are loaded via pydantic from `.env`. Copy `.env.example` to `.env` and adjust.

Important variables:

- `JWT_SECRET` — production secret
- `ADMIN_EMAIL` / `ADMIN_PASSWORD` — dev admin credentials
- `QDRANT_URL` — `http://localhost:6333` by default
- `REDIS_URL` — `redis://localhost:6379/0`

---

## API & Auth

The backend exposes REST endpoints under `/api`.

- POST `/api/auth/login` — obtain JWT using admin credentials from `.env`
- Admin endpoints under `/api/admin` require a Bearer token with `role: admin`

Refer to the interactive docs at `/docs` for up-to-date request/response shapes.

---

## Data & storage notes

- Qdrant: store location configured via Docker Compose (see `Backend/docker-compose.yml`). Use Docker named volumes in production — avoid Windows bind mounts for RocksDB.
- Redis: persistent snapshot lives at `.data/redis/dump.rdb`
- Uploads and metadata persist to `.data/uploads` and `.data/meta`

If you accidentally encounter DB corruption during development, remove `.data/qdrant` and restart the stack (this will remove indexed vectors).

---

## Development workflow

- Start Qdrant & Redis with `docker compose`
- Run backend with `uvicorn --reload`
- Run frontend with `npm run dev`
- Use the Swagger UI to test APIs and obtain tokens

---

## Testing & CI

This repository currently does not include CI pipelines or unit tests. Recommended additions for a production-ready OSS project:

- Add `pytest` test suite under `Backend/tests/` and run in CI
- Set up GitHub Actions to run linting, tests, and build checks on PRs
- Add code coverage and static type checks (mypy)

---

## Roadmap

Planned improvements and community-friendly tasks:

- Add persistent user management and role-based ACLs
- Implement unit/integration tests for ingestion and RAG pipeline
- Add deployment scripts (Docker Compose + Kubernetes manifests)
- Provide example datasets and scripts to seed the index

Contributions welcome — see `How to contribute`.

---

## Governance & Code of Conduct

This project follows an open, meritocratic governance model. Maintainers review issues and PRs and merge changes that align with the roadmap.

Please follow the Contributor Covenant Code of Conduct (add `CODE_OF_CONDUCT.md` to the repo). Be respectful, inclusive, and constructive in discussions.

---

## Project structure (short)

```
NyaySaathi/
├─ Backend/                # FastAPI backend
│  ├─ app/                 # FastAPI app, routers, and services
│  ├─ .data/               # persisted data (qdrant, redis, uploads)
│  └─ docker-compose.yml   # qdrant + redis for quick dev
├─ Frontend/               # React (Vite) SPA
│  ├─ src/                 # components and app code
│  └─ public/              # static assets & screenshots
└─ README.md               # this document
```

---

## How to contribute (OSS)

We welcome contributions of all sizes. A practical onboarding path for new contributors:

1. Read `CONTRIBUTING.md` (create this file if missing) and `CODE_OF_CONDUCT.md`.
2. Look for issues labeled `good first issue` or `help wanted`.
3. Fork the repository and open a PR with a clear description and tests (if applicable).

Small, helpful contributions:

- Improve or add documentation and screenshots
- Add tests for backend services
- Fix UI accessibility or responsiveness issues
- Integrate an alternative embedding provider or vector store adapter

Maintainers will review PRs and provide feedback. If you want to take on a larger feature, open an issue to discuss the design first.

---

## License

This project is distributed under the MIT License. See `LICENSE` for details.

---

## Contact

If you have questions or want a walkthrough, open an issue or start a discussion on the repository.

---

Thank you for considering contributing to NyaySaathi — this README is now focused on making the project friendly for open-source contributions and ongoing maintenance.
