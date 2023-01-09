from typing import List
from fastapi import APIRouter, Depends
from app.community.constants import MAIN_PAGE_COMMUNITY_LOAD_COUNT, MAIN_PAGE_POSTING_LOAD_COUNT

from app.page.schemas import ResponseMainPage, ResponseCommunityPage
from app.community.dependency import valid_skip_count
from app.community import service
from app.posting import service as posting_service

router = APIRouter(
    prefix="/community",
    tags=['page']
)

# 메인페이지 화면에서 요청하게될 함수
@router.get('', response_model=List[ResponseMainPage], response_model_exclude_none=True)
async def get_main_page():
    communities: List[ResponseMainPage] = await service.get_communities(MAIN_PAGE_COMMUNITY_LOAD_COUNT)
    for i in range(len(communities)):
        communities[i].latest_postings = await posting_service.get_postings_by_community_id(communities[i].id, MAIN_PAGE_POSTING_LOAD_COUNT)
    
    return communities

# 개별 커뮤니티 화면에서 요청하게 될 함수
@router.get('/{community_name}/page/{page_num}', response_model=ResponseCommunityPage, response_model_exclude_none=True)
async def get_page(
    valid_values: dict = Depends(valid_skip_count)
):
    community: ResponseCommunityPage = valid_values['community']
    count_per_page = valid_values['count_per_page']
    skip_count = valid_values['skip_count']
    community.page_postings = await posting_service.get_postings_by_community_id(
        community.id, count_per_page, skip_count)
    return community