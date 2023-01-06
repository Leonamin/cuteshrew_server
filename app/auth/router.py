from typing import Mapping
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import database
from app.auth.dependencies import parse_jwt_data, valid_token
from app.auth.schemas import AuthToken
from app.auth.utils import Hash

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post('signin', response_model=AuthToken)
def signin(
    request: OAuth2PasswordRequestForm = Depends(),
    user: Mapping = Depends(),
):
    pass

# 근데 뭔가 이상하지 않나?
# token 유효성 검사 후 다시 token을 반환하는게 말이 안맞는 느낌이다.
@router.post('/verify')
def verify_token(token: AuthToken = Depends(valid_token)):
    return parse_jwt_data(token.access_token)
