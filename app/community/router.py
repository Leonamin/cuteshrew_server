from typing import List, Mapping, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.community.exceptions import UnauthorizedException

from .schemas import ReqeustCommunityCreate, ResponseCommunityInfo
from .dependency import valid_community_name, valid_load_cound
from app.community import service
from app.user import dependency as user_dependency

router = APIRouter(
    prefix="/community",
    tags=['community']
)
default_community_count = 5
default_count_per_page = 15

@router.get('/all', response_model=List[ResponseCommunityInfo])
async def get_communities(
    load_count: int = Depends(valid_load_cound),
):
    return await service.get_communities(load_count)
    

@router.get('/info', response_model=ResponseCommunityInfo)
def get_community_by_name(community: Mapping = Depends(valid_community_name)):
    return community


# 개별 커뮤니티 화면에서 요청하게 될 함수
@router.get('/{name}/page/{page_num}', response_model_exclude_none=True)
def get_page(name: str, page_num: int, count_per_page: Optional[int] = default_count_per_page):
    pass

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
