from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import communityRepo

router = APIRouter(
    prefix="/community",
    tags=['community']
)

@router.get('/', response_model=List[schemas.CommunityBase])
def all(db: Session = Depends(database.get_db)):
    return communityRepo.get_all(db)

# TODO 어드민만 생성 가능하게 변경
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.CommunityBase, db: Session = Depends(database.get_db)):
    return communityRepo.create(request, db)

# 204 에러는 Content-Length를 가질 수 없다
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db)):
    return communityRepo.destroy(id, db)