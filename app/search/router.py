from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/search",
    tags=['search']
)


@router.get("/posting", response_model_exclude_none=True)
def search_posts_by_user(user_id: Optional[int] = None, user_name: Optional[str] = None, start_id: Optional[str] = None, load_page_num: Optional[int] = 20):
    pass


@router.get("/comment", response_model_exclude_none=True)
def search_comments_by_user(user_id: Optional[int] = None, user_name: Optional[str] = None, start_id: Optional[str] = None, load_page_num: Optional[int] = 20):
    pass
