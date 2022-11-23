from typing import List, Optional, Union
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import  searchRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/search",
    tags=['search']
)

@router.get("/posting", response_model=Union[schemas.PostingPreviewResponseWithHeader, List[schemas.PostingPreviewResponse]])
def search_posts_by_user(user_id: Optional[int] = None, user_name: Optional[str] = None, start_id: Optional[str] = None, load_page_num: Optional[int] = 20, db: Session = Depends(database.get_db)):
    postingPreviewResponse = searchRepo.search_posts_by_user(user_id, user_name, start_id, load_page_num, db)
    return postingPreviewResponse

@router.get("/comment", response_model=Union[schemas.CommentResponseWithHeader, List[schemas.CommentResponse]])
def search_comments_by_user(user_id: Optional[int] = None, user_name: Optional[str] = None, start_id: Optional[str] = None, load_page_num: Optional[int] = 20, db: Session = Depends(database.get_db)):
    commentPreviewResponse = searchRepo.search_comments_by_user(user_id, user_name, start_id, load_page_num, db)
    return commentPreviewResponse
