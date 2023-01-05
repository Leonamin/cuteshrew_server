from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.auth.constants import ALGORITHM, SECRET_KEY
from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import AuthToken
from app.auth.utils import getCurrentUnixTimeStamp

def valid_token(token: AuthToken) -> AuthToken:
    if token.token_type != 'bearer':
        print("토큰 타입이 아님")
        raise InvalidCredentials()
    if token.expire_time < getCurrentUnixTimeStamp():
        print("시간 초과")
        raise InvalidCredentials()
    return token

def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()
        # raise "InvalidCredentials"

    return {"user_email": payload["sub"]}