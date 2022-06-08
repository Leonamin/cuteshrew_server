from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import communityRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/community",
    tags=['community']
)

# 커뮤니티


@router.get('/', response_model=List[schemas.CommunityBase])
def all(db: Session = Depends(database.get_db)):
    return communityRepo.get_all(db)

# TODO 어드민만 생성 가능하게 변경


@router.post('/', status_code=status.HTTP_201_CREATED)
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

# 커뮤니티 게시글
