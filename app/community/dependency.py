
from typing import Mapping

from fastapi import Depends

from app.dependency import Authority

from .service import get_community_by_name
from .exceptions import CommunityNotFound


async def valid_community_name(community_name: str) -> Mapping:
    community = await get_community_by_name(community_name=community_name)

    if not community:
        raise CommunityNotFound()
    return community
