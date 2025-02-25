from datetime import timedelta
import time
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.db import database
from app.auth.constants import ACCESS_TOKEN_EXPIRE_WEEKS
from app.auth.dependencies import create_access_token, parse_jwt_data, valid_token
from app.auth.schemas import AuthToken
from app.auth.utils import Hash
from app.dependency import get_secret_key
from app.user import service as user_service
from app.user.exceptions import UserNotFoundException
from .exceptions import IncorrectPassword

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

# FIXME 나중에 repository로 분화 하든 해서 엔드포인트에서 처리를 안하게 만들어야할거 같다.
@router.post('/signin', response_model=AuthToken)
async def signin(
    request: OAuth2PasswordRequestForm = Depends(),
    secret_key: str = Depends(get_secret_key)
):
    user = await user_service.get_user_by_user_name(request.username)
    if not user:
        raise UserNotFoundException()
    if not Hash.verify(user.password, request.password):
        raise IncorrectPassword()
        
    expires_delta = timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEKS)
    access_token, expire_time = create_access_token(
        data={"user_nickname": user.nickname}, 
        expires_delta=expires_delta, 
        secret_key=secret_key)
    expire_time = round(time.mktime(expire_time.timetuple()))
    
    return {"access_token": access_token, "token_type": "bearer", "expire_time": expire_time}


# 근데 뭔가 이상하지 않나?
# token 유효성 검사 후 다시 token을 반환하는게 말이 안맞는 느낌이다.
@router.post('/verify')
async def verify_token(token: AuthToken = Depends(valid_token)):
    return parse_jwt_data(token.access_token)
