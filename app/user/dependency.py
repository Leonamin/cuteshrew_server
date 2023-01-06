from typing import Mapping
from fastapi import Depends
from sqlalchemy.orm import Session

from app.user.exceptions import UserNotFoundException

from .service import get_user_by_user_name, get_user_by_user_email
from app import database


async def valid_user_id(user_id: int) -> Mapping:
    pass


async def valid_user_name(user_name: str) -> Mapping:
    user = await get_user_by_user_name(user_name)
    if not user:
        # raise UserNotFoundException
        return None
    return user


async def valid_user_email(user_email: str) -> Mapping:
    user = await get_user_by_user_email(user_email)
    if not user:
        # raise UserNotFoundException
        return None
    return user
