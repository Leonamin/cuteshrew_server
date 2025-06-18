from typing import List, Mapping, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.search.dependency import valid_posting_search_filters, valid_comment_search_filters
from app.search.schemas import ResponseSearchCommentDetail, ResponseSearchPostingPreview
from app.comment import service as comment_service

router = APIRouter(
    prefix="/search",
    tags=['search']
)

# 아직 순서는 없어서 최신순 고정이다.
# skip_until_id는 skip_until_id까지 건너뛰고 skip_until_id 다음부터 준다.
# skip_until_id가 None이면 처음 부터 가져온다.
# 원래는 skip_number로 해서 3개 4개 건너뛰게 하고 싶었는데 동기화 문제 때문에 id를 명시적으로 지정
@router.get("/posting", response_model=List[ResponseSearchPostingPreview], response_model_exclude_none=True)
async def search_postings_by_user_name(
    postings: List[Mapping] = Depends(valid_posting_search_filters)
):
    response: List[ResponseSearchPostingPreview] = postings
    for i in range(len(response)):
        response[i].comment_count = await comment_service.get_comment_count_by_posting_id(response[i].id)
    return postings


@router.get("/comment", response_model= List[ResponseSearchCommentDetail], response_model_exclude_none=True)
async def search_comments_by_user_name(
    comments: List[Mapping] = Depends(valid_comment_search_filters)
):
    return comments
