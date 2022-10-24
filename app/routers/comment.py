from fastapi import APIRouter
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import commentRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/community/{community_name}/{post_id}/comment",
    tags=['comment']
)


@router.get("/{page_num}")
def get_page(community_name: str, post_id: int, page_num: int, count_per_page: int, db: Session = Depends(database.get_db)):
    return commentRepo.get_page(post_id, page_num, count_per_page, db)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_comment(community_name: str, post_id: int, request: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return commentRepo.create_comment(post_id, request, db, current_user)


@router.post("/{group_id}", status_code=status.HTTP_201_CREATED)
def create_reply(community_name: str, post_id: int, group_id: int, request: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return commentRepo.create_reply(post_id, group_id, request, db, current_user)
