from typing import List, Mapping
from fastapi import APIRouter
from fastapi import APIRouter, Depends, status

from app.comment import service
from app.comment.schemas import ReqeustCommentCreate, ResponseCommentDetail
from app.comment.dependency import can_user_delete_comment, valid_load_count, valid_comment_id, valid_page_num, valid_comment_posting_id
from app.posting import dependency as posting_dependency
from app.user import dependency as user_dependency
from app.search import schemas as search_schemas

router = APIRouter(
    # prefix="/community/{community_name}/{post_id}/comment",
    prefix="/comment",
    tags=['comment']
)


@router.get("/{comment_id}", response_model=ResponseCommentDetail)
async def get_comment(
    comment: Mapping = Depends(valid_comment_id)
):
    return comment


@router.get("/list/{posting_id}", response_model=List[ResponseCommentDetail])
async def get_comments(
    comments: List[Mapping] = Depends(valid_comment_posting_id)
):
    return comments


@router.get("/page/{posting_id}/comment/{page_num}", response_model=List[search_schemas.ResponseSearchCommentDetail])
async def get_comment_page(
    posting: Mapping = Depends(posting_dependency.valid_posting_id),
    page_num: int = Depends(valid_page_num),
    load_count: int = Depends(valid_load_count)
):
    skip_offset = (page_num - 1) * load_count
    return await service.get_comments_by_posting_id(posting.id, load_count, skip_offset)


@router.post("/create/{posting_id}", status_code=status.HTTP_201_CREATED)
async def create_comment(
    new_comment: ReqeustCommentCreate,
    posting: Mapping = Depends(posting_dependency.valid_posting_id),
    user: Mapping = Depends(user_dependency.get_current_user_info)
):
    comment = await service.create_comment(
        posting.id, user.id, new_comment.comment)
    return comment


@router.post("/reply/create/{group_id}", status_code=status.HTTP_201_CREATED)
def create_reply(community_name: str, post_id: int, group_id: int):
    pass


@router.put("/{comment_id}", status_code=status.HTTP_201_CREATED)
def update_comment(community_name: str, post_id: int, comment_id: int):
    pass


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int = Depends(can_user_delete_comment)
):
    return await service.delete_comment_by_id(comment_id)
