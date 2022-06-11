from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import postingRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/community/{name}",
    tags=['posting']
)


@router.get("/")
def get_all(name: str, db: Session = Depends(database.get_db)):
    return postingRepo.get_all(name, db)


@router.get("/{id}")
def get_post(name: str, post_id: int, db: Session = Depends(database.get_db)):
    return postingRepo.get_post(name, post_id, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(name: str, request: schemas.PostingBase, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return postingRepo.create_post(name, request, db, current_user)

# update 할 때 .dict()로 형변환...


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(name: str, post_id: int, request: schemas.PostingBase, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return postingRepo.update_post(name, post_id, request, db, current_user)