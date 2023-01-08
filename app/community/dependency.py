
from typing import Mapping

from fastapi import Depends

from app.dependency import Authority

from .service import get_community_by_name
from .exceptions import CommunityNotFound, InvalidLoadCountException, InvalidCommunityName


async def valid_community_name(community_name: str) -> Mapping:
    if community_name == 'info' or \
            community_name == 'all' or \
            community_name == 'main' or \
            community_name == 'page':
        raise InvalidCommunityName()

    community = await get_community_by_name(community_name=community_name)

    if not community:
        raise CommunityNotFound()
    return community


def valid_load_cound(load_count: int) -> int:
    if (load_count > 100 or load_count <= 0):
        raise InvalidLoadCountException()
    return load_count
