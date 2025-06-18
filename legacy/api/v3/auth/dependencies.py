from datetime import datetime, timedelta
from typing import Mapping, Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.auth.constants import ALGORITHM, TOKEN_URL
from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import AuthToken
from app.auth.utils import getCurrentUnixTimeStamp
from app.dependency import get_secret_key

# 얘가 로그인 하는 엔드포인트랑 똑같아야한다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

# data = {"sub" : user.email}
def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta],
    secret_key: str
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt, expire

def valid_token(token: AuthToken) -> AuthToken:
    if token.token_type != 'bearer':
        print("토큰 타입이 아님")
        raise InvalidCredentials()
    if token.expire_time < getCurrentUnixTimeStamp():
        print("시간 초과")
        raise InvalidCredentials()
    return token

# 동작 방식
# parse_jwt_data -> oauth2_scheme 
# -> oauth2_scheme에 정의된 엔드포인트로 token 요청 
# -> 정의된 엔드포인트가 토큰 주는 엔드포인트 일 경우 그 엔드포인트 동작대로 수행 후 토큰 반환
# get_current_user
def parse_jwt_data(
    token: str = Depends(oauth2_scheme),
    secret_key: str = Depends(get_secret_key),
) -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    except JWTError:
        raise InvalidCredentials()

    return {"user_nickname": payload["user_nickname"]}

# get_current_user
