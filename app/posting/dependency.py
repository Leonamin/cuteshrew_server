
from typing import Mapping, Optional
from fastapi import Depends, HTTPException
from pydantic import SecretStr

from app.dependency import Authority
from app.exceptions import HashTypeError, HashValueError, UnknownError
from app.posting import service
from app.posting.schemas import RequestPostingCreate
from app.posting.exceptions import PostingNotFound, NeedPasswordException, InvalidPasswordException, UnauthorizedException
from app.community import dependency as community_dependency
from app.user import dependency as user_dependency
from app.user import dependency as user_dependency

from app.auth.utils import Hash


# id를 통해 포스팅이 존재하는지 확인
async def valid_posting_id(
    id: int,
) -> Mapping:
    posting = await service.get_posting_by_id(id)

    if not posting:
        raise PostingNotFound()
    return posting

# 가져온 포스팅의 비밀번호가 올바른지 확인
async def verify_posting(
    password: Optional[SecretStr] = None,
    posting: Mapping = Depends(valid_posting_id)
) -> Mapping:
    if not posting.is_locked:
        return posting
    try:
        if not password:
            raise NeedPasswordException()
        if not Hash.verify(posting.password, password.get_secret_value()):
            raise InvalidPasswordException()
        return posting
        
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HashValueError()
    except TypeError as e:
        raise HashTypeError()
    except Exception as e:
        raise UnknownError(detail=e.__class__.__name__)


def can_user_write_posting(
    community: Mapping,
    user: Mapping
) -> Mapping:
    if (community.authority.value > user.authority.value):
        raise UnauthorizedException()
    return community
