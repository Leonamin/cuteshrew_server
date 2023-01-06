from typing import Mapping
from fastapi import Depends
from sqlalchemy.orm import Session

from app.user.exceptions import UserNotFoundException

from .service import get_user_by_user_name, get_user_by_user_email
from app import database
from app.models.models import User
from app.dependency import Authority

from app.auth import dependencies as auth_dependency


async def valid_user_id(user_id: int) -> Mapping:
    pass


async def can_user_create_community(
        user: Mapping = Depends(auth_dependency.parse_jwt_data)) -> bool:
    user: User = await get_user_by_user_email(user['sub'])

    if (user.authority.value >= Authority.SUB_ADMIN.value):
        return True
    return False


async def valid_user_name(user_name: str) -> Mapping:
    user = await get_user_by_user_name(user_name)
    if not user:
        raise UserNotFoundException()
    return user


async def valid_user_email(user_email: str) -> Mapping:
    user = await get_user_by_user_email(user_email)
    if not user:
        raise UserNotFoundException()
    return user
