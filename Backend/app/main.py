from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers.chatbot import router as chat_router
from app.api.routers.admin import router as admin_router
from app.api.routers.health import router as health_router
from app.api.routers.nyaylens import router as lens_router
from app.api.routers.auth import router as auth_router
from app.api.routers.nyayshala import router as shala_router

app = FastAPI(title="Nyay RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix=settings.api_prefix)
app.include_router(admin_router, prefix=settings.api_prefix)
app.include_router(lens_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(shala_router, prefix=settings.api_prefix)
app.include_router(health_router)


@app.get("/health/live")
def live():
    return {"ok": True}
