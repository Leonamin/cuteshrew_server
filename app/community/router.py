from typing import List, Mapping, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.community.exceptions import UnauthorizedException

from .schemas import ReqeustCommunityCreate, ResponseCommunityInfo
from .dependency import valid_community_name
from .service import create_community
from app.user import dependency as user_dependency

router = APIRouter(
    prefix="/community",
    tags=['community']
)
default_community_count = 5
default_count_per_page = 15

@router.get('', response_model=ResponseCommunityInfo)
def get_community_by_name(community: Mapping = Depends(valid_community_name)):
    return community
    

@router.post('', status_code=status.HTTP_201_CREATED)
async def create(
    new_community: ReqeustCommunityCreate, 
    can_create: bool = Depends(user_dependency.valid_current_user_admin),
):
    if can_create:
        await create_community(
            community_name=new_community.name,
            community_showname=new_community.showname,
            authority=new_community.authority,
            )
        return {"created"}
    else:
        return UnauthorizedException()
# 204 에러는 Content-Length를 가질 수 없다


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int):
    pass

# 개별 커뮤니티 화면에서 요청하게 될 함수
@router.get('/{name}/page/{page_num}', response_model_exclude_none=True)
def get_page(name: str, page_num: int, count_per_page: Optional[int] = default_count_per_page):
    pass