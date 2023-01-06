from typing import Mapping
from fastapi import APIRouter, Depends, status

from .dependency import valid_user_name, valid_user_email
from .schemas import RequestUserCreate, ResponseUserDetail
from .exceptions import UserNotFoundException


router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post('/general', status_code=status.HTTP_201_CREATED)
def create_user(user: RequestUserCreate = Depends()):
    print(user.password.get_secret_value())
    return {"asdasd"}


@router.post('/admin')
def create_user_for_admin():
    pass


@router.get('/search', response_model=ResponseUserDetail)
async def get_user_by_name(user: Mapping = Depends(valid_user_name)):
    return user
