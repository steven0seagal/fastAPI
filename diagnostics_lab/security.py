from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import cast

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from diagnostics_lab.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return cast(str, pwd_context.hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


class TokenData(BaseModel):
    sub: str


def create_access_token(*, subject: str, expires_minutes: int | None = None) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_minutes
        if expires_minutes is not None
        else settings.access_token_expire_minutes
    )
    to_encode = {"sub": subject, "exp": expire}
    return cast(str, jwt.encode(to_encode, settings.secret_key, algorithm="HS256"))


def decode_access_token(token: str) -> TokenData:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        sub = payload.get("sub")
        if not sub:
            raise ValueError("missing sub")
        return TokenData(sub=str(sub))
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
