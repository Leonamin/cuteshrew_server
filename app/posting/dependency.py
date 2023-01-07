
from typing import Mapping, Optional
from fastapi import Depends
from pydantic import SecretStr

from app.dependency import Authority
from app.posting import service
from app.posting.schemas import RequestPostingCreate
from app.posting.exceptions import PostingNotFound, NeedPasswordException, UnauthorizedException
from app.community import dependency as community_dependency
from app.user import dependency as user_dependency


async def valid_posting_id(
    id: int,
    password: Optional[SecretStr] = None,
    community: Mapping = Depends(
        community_dependency.valid_community_name),
) -> Mapping:
    posting = await service.get_posting(
        community.id, id, password.get_secret_value() if password != None else None)

    if not posting:
        raise PostingNotFound()
    return posting


def can_user_write_posting(
    community: Mapping,
    user: Mapping
) -> Mapping:
    if (community.authority.value > user.authority.value):
        raise UnauthorizedException()
    return community
