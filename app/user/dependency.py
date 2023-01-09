from typing import Mapping
from fastapi import Depends
from app.dependency import Authority

from app.user.exceptions import UserNotFoundException

from .service import get_user_by_user_name, get_user_by_user_email
from app.auth import dependencies as auth_dependency


async def valid_user_id(user_id: int) -> Mapping:
    pass


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


async def get_current_user_info(
    parsed_info: dict = Depends(auth_dependency.parse_jwt_data)
) -> Mapping:
    user: Mapping = await valid_user_name(parsed_info['user_nickname'])

    return user


def valid_current_user_admin(
    user: Mapping = Depends(get_current_user_info)
) -> bool:
    if (user.authority.value >= Authority.SUB_ADMIN.value):
        return True
    return False
