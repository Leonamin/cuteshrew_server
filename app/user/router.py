from typing import Mapping
from fastapi import APIRouter, Depends, status

from app.user.dependency import valid_user_name, valid_user_email
from app.user.schemas import RequestUserCreate, ResponseUserDetail
from app.user.exceptions import UserNotFoundException
from app.posting import service as posting_service
from app.comment import service as comment_service
from app.user import service


router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.post('/general', status_code=status.HTTP_201_CREATED)
async def create_user(user: RequestUserCreate):
    print(user.password.get_secret_value())
    await service.create_user(
        user.nickname, user.email, user.password.get_secret_value(),)
    return "user created"


@router.post('/admin')
def create_user_for_admin():
    pass


@router.get('/search', response_model=ResponseUserDetail)
async def get_user_by_name(user: Mapping = Depends(valid_user_name)):
    response: ResponseUserDetail = user
    response.posting_count = await posting_service.get_posting_count_by_user_id(response.id)
    response.comment_count = await comment_service.get_comment_count_by_user_id(response.id)

    return user
