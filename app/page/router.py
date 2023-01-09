from typing import List, Mapping
from fastapi import APIRouter, Depends
from app.community.constants import MAIN_PAGE_COMMUNITY_LOAD_COUNT, MAIN_PAGE_POSTING_LOAD_COUNT

from app.page.schemas import ResponseMainPage, ResponseCommunityPage
from app.community.dependency import valid_skip_count
from app.community import service
from app.posting import service as posting_service
from app.comment import service as comment_service

router = APIRouter(
    prefix="/community",
    tags=['page']
)

# 메인페이지 화면에서 요청하게될 함수
@router.get('', response_model=List[ResponseMainPage], response_model_exclude_none=True)
async def get_main_page():
    communities: List[ResponseMainPage] = await service.get_communities(MAIN_PAGE_COMMUNITY_LOAD_COUNT)
    for i in range(len(communities)):
        communities[i].posting_list = await posting_service.get_postings_by_community_id(communities[i].id, MAIN_PAGE_POSTING_LOAD_COUNT)
        print(communities[i].name)
        print(len(communities[i].posting_list))
        for j in range(len(communities[i].posting_list)):
            communities[i].posting_list[j].comment_count = await comment_service.get_comment_count_by_posting_id(communities[i].posting_list[j].id)
    
    return communities

# 개별 커뮤니티 화면에서 요청하게 될 함수
@router.get('/{community_name}/page/{page_num}', response_model=ResponseCommunityPage, response_model_exclude_none=True)
async def get_community_page(
    valid_values: dict = Depends(valid_skip_count)
):
    community: ResponseCommunityPage = valid_values['community']
    count_per_page = valid_values['count_per_page']
    skip_count = valid_values['skip_count']
    community.posting_list = await posting_service.get_postings_by_community_id(
        community.id, count_per_page, skip_count)

    for i in range(len(community.posting_list)):
        community.posting_list[i].comment_count = await comment_service.get_comment_count_by_posting_id(community.posting_list[i].id)
    
    return community