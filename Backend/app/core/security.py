from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from passlib.context import CryptContext
import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, password_hash: str) -> bool:
    # If hash looks like bcrypt, verify; otherwise compare plain (dev convenience)
    try:
        if password_hash.startswith("$2"):
            return pwd_context.verify(plain_password, password_hash)
    except Exception:
        pass
    return plain_password == password_hash


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: Dict, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.jwt_expire_minutes)
    to_encode = {**subject, "exp": expire}
    token = jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
    return token


def decode_token(token: str) -> Dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
