from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import postingRepo
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/search",
    tags=['search']
)

@router.get("/posting", response_model=List[schemas.PostingPreviewResponse])
def search_posts_by_user(user_id: Optional[int] = None, user_name: Optional[str] = None, start_post_id: Optional[str] = 0, load_page_num: Optional[int] = 20, db: Session = Depends(database.get_db)):
    return postingRepo.search_posts_by_user(user_id, user_name, start_post_id, load_page_num, db)