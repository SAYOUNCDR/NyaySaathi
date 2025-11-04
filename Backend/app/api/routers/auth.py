from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.core.security import verify_password, create_access_token, get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(body: LoginRequest):
    # Single admin user from env for now
    email = body.email.strip().lower()
    if email != settings.admin_email.strip().lower():
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(body.password, settings.admin_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": email, "role": "admin"})
    return {"access_token": token, "token_type": "bearer", "user": {"email": email, "role": "admin"}}
