from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..schemas import new_schemas

from .. import database
from ..repository import communityRepo
from .oauth2 import get_current_user

router = APIRouter(
    prefix="/community",
    tags=['community']
)
default_community_count = 5
default_count_per_page = 15

# 커뮤니티
# 일반적으로 메인 페이지에 쓰이고 0개면 모든 커뮤니티를 불러온다

@router.get('', response_model=List[new_schemas.ResponseShowCommunity], response_model_exclude_none=True)
def all(community_count: Optional[int] = 0, db: Session = Depends(database.get_db)):
    return communityRepo.get_all(community_count, db)

# TODO 어드민만 생성 가능하게 변경


@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: new_schemas.CommunityCreate, db: Session = Depends(database.get_db), current_user: new_schemas.UserBase = Depends(get_current_user)):
    print(current_user)
    return communityRepo.create(request, db, current_user)

# 204 에러는 Content-Length를 가질 수 없다


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db), current_user: new_schemas.UserBase = Depends(get_current_user)):
    return communityRepo.destroy(id, db, current_user)


# 개별 커뮤니티 화면에서 요청하게 될 함수
@router.get('/{name}/page/{page_num}', response_model=new_schemas.ResponseShowCommunity, response_model_exclude_none=True)
def get_page(name: str, page_num: int, count_per_page: Optional[int] = default_count_per_page, db: Session = Depends(database.get_db)):
    return communityRepo.get_page(name, page_num, count_per_page, db)
