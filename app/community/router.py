from typing import List, Mapping, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.community.constants import DEFAULT_COUNT_PER_PAGE, MAIN_PAGE_COMMUNITY_LOAD_COUNT, MAIN_PAGE_POSTING_LOAD_COUNT

from app.community.exceptions import UnauthorizedException

from .schemas import ReqeustCommunityCreate, ResponseCommunityInfo, ResponseCommunityPageInfo, ResponseMainCommunityInfo
from .dependency import valid_community_name, valid_load_cound, valid_skip_count
from app.community import service
from app.user import dependency as user_dependency
from app.posting import service as posting_service

router = APIRouter(
    prefix="/community",
    tags=['community']
)

@router.get('/all', response_model=List[ResponseCommunityInfo])
async def get_communities(
    load_count: int = Depends(valid_load_cound),
):
    communities: List[ResponseCommunityInfo] = await service.get_communities(load_count)
    
    for i in range(len(communities)):
        communities[i].posting_count = await posting_service.get_posting_count_by_community_id(communities[i].id)
    return communities
        
    

@router.get('/info', response_model=ResponseCommunityInfo)
async def get_community_by_name(community: Mapping = Depends(valid_community_name)):
    community: ResponseCommunityInfo = community
    community.posting_count = await posting_service.get_posting_count_by_community_id(community.id)
    return community

# 메인페이지 화면에서 요청하게될 함수
@router.get('/main', response_model=List[ResponseMainCommunityInfo], response_model_exclude_none=True)
async def get_main_page():
    communities: List[ResponseMainCommunityInfo] = await service.get_communities(MAIN_PAGE_COMMUNITY_LOAD_COUNT)
    for i in range(len(communities)):
        communities[i].latest_postings = await posting_service.get_postings_by_community_id(communities[i].id, MAIN_PAGE_POSTING_LOAD_COUNT)
    
    return communities

# 개별 커뮤니티 화면에서 요청하게 될 함수
@router.get('/{community_name}/page/{page_num}', response_model=ResponseCommunityPageInfo, response_model_exclude_none=True)
async def get_page(
    valid_values: dict = Depends(valid_skip_count)
):
    community: ResponseCommunityPageInfo = valid_values['community']
    count_per_page = valid_values['count_per_page']
    skip_count = valid_values['skip_count']
    community.page_postings = await posting_service.get_postings_by_community_id(
        community.id, count_per_page, skip_count)
    return community

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_community(
    new_community: ReqeustCommunityCreate, 
    can_create: bool = Depends(user_dependency.valid_current_user_admin),
):
    if can_create:
        await service.create_community(
            community_name=new_community.name,
            community_showname=new_community.showname,
            authority=new_community.authority,
            )
        return {"created"}
    else:
        return UnauthorizedException()
# 204 에러는 Content-Length를 가질 수 없다


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def destroy_community(
    community_id: int,
    can_destroy: bool = Depends(user_dependency.valid_current_user_admin),
    ):
    if can_destroy:
        await service.delete_community(community_id=community_id)
        pass
    else:
        raise UnauthorizedException()
