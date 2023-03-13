from datetime import timedelta, datetime
from typing import Optional
from jose import JWTError, jwt


def create_session_token(
    data: dict,
    expires_delta: Optional[timedelta],
    secret_key: str

):
    to_encode = data.copy()
    if expires_delta or expires_delta < timedelta(hours=48):
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=1800)
    to_encode.update({"iat": datetime.utcnow(), "exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm='HS256')
    return encoded_jwt
