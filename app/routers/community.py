from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import communityRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/community",
    tags=['community']
)
default_community_count = 5
default_count_per_page = 15

# 커뮤니티


@router.get('', response_model=List[schemas.ShowCommunity])
def all(community_count: Optional[int] = default_community_count, db: Session = Depends(database.get_db)):
    return communityRepo.get_all(community_count, db)

# TODO 어드민만 생성 가능하게 변경


@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.CommunityBase, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    print(current_user)
    return communityRepo.create(request, db, current_user)

# 204 에러는 Content-Length를 가질 수 없다


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return communityRepo.destroy(id, db, current_user)

# 나중에 자동으로 page로 이동 /general/1[page_num]/


@router.get('/{name}', status_code=status.HTTP_200_OK, response_model=schemas.ShowCommunity)
def show(name: str, db: Session = Depends(database.get_db)):
    return communityRepo.show(name, db)


@router.get('/{name}/page/{page_num}', response_model=schemas.ShowCommunity)
def get_page(name: str, page_num: int, count_per_page: Optional[int] = default_count_per_page, db: Session = Depends(database.get_db)):
    return communityRepo.get_page(name, page_num, count_per_page, db)

# 커뮤니티 게시글
