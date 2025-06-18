from datetime import datetime, timedelta, timezone
from jose import jwt

from app.config import settings


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def get_secret_key() -> str:
    return settings.SECRET_KEY


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(
        timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_secret_key(), algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + \
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_secret_key(), algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
