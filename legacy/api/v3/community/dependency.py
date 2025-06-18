
from typing import Mapping, Optional

from fastapi import Depends
from app.community.constants import DEFAULT_COUNT_PER_PAGE

from app.dependency import Authority

from .service import get_community_by_name
from .exceptions import CommunityNotFound, InvalidLoadCountException, InvalidCommunityName, InvalidPageLoadCount, InvalidPageNum, ExceededPageNum


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


def valid_page_num(page_num: int) -> int:
    if (page_num <= 0):
        raise InvalidPageNum()
    return page_num


def valid_page_load_count(count_per_page: Optional[int] = DEFAULT_COUNT_PER_PAGE):
    if (count_per_page <= 0 or count_per_page > 100):
        raise InvalidPageLoadCount()
    return count_per_page


def valid_skip_count(
    community: Mapping = Depends(valid_community_name),
    page_num: int = Depends(valid_page_num),
    count_per_page: int = Depends(valid_page_load_count),
) -> dict:
    skip_count = (page_num - 1) * count_per_page

    # 전체 포스팅 숫자 이상을 건너 뛰면 다음 페이지는 게시글 개수가 0개다
    if community.postings_count <= skip_count:
        raise ExceededPageNum()

    return {'count_per_page' : count_per_page, 'skip_count':skip_count, 'community' : community}
