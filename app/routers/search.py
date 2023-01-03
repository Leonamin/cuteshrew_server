from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import new_schemas

from .. import database
from ..repository import searchRepo

router = APIRouter(
    prefix="/search",
    tags=['search']
)


@router.get("/posting", response_model=new_schemas.ResponsePostingList, response_model_exclude_none=True)
def search_posts_by_user(user_id: Optional[int] = None, user_name: Optional[str] = None, start_id: Optional[str] = None, load_page_num: Optional[int] = 20, db: Session = Depends(database.get_db)):
    postingPreviewResponse = searchRepo.search_posts_by_user(
        user_id, user_name, start_id, load_page_num, db)
    return postingPreviewResponse


@router.get("/comment", response_model=new_schemas.ResponseCommentList, response_model_exclude_none=True)
def search_comments_by_user(user_id: Optional[int] = None, user_name: Optional[str] = None, start_id: Optional[str] = None, load_page_num: Optional[int] = 20, db: Session = Depends(database.get_db)):
    commentPreviewResponse = searchRepo.search_comments_by_user(
        user_id, user_name, start_id, load_page_num, db)

    return commentPreviewResponse
