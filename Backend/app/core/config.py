from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    # API
    api_prefix: str = "/api"
    cors_origins: List[str] = ["http://localhost:5173"]

    # LLM provider
    llm_provider: str = Field("openai", description="openai|google")
    llm_model: str = Field("gpt-4o-mini")
    openai_api_key: str | None = None
    google_api_key: str | None = None

    # Stores
    qdrant_url: str = "http://localhost:6333"
    redis_url: str = "redis://localhost:6379/0"
    storage_dir: str = ".data/uploads"
    qdrant_corpus_collection: str = "corpus"

    # Auth
    jwt_secret: str = "change-me-dev-secret"
    jwt_expire_minutes: int = 120
    admin_email: str = "admin@example.com"
    admin_password: str = "admin123"

    class Config:
        env_file = ".env"

settings = Settings()
