from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import postingRepo

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


@router.post("/{id}", status_code=status.HTTP_201_CREATED)
def create(name: str, request: schemas.PostingBase, db: Session = Depends(database.get_db)):
    return postingRepo.create_post(name, request, db)
