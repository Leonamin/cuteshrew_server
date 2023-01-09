from typing import List, Mapping
from fastapi import APIRouter
from fastapi import APIRouter, Depends, status

from app.comment import service
from app.comment.schemas import ReqeustCommentCreate, ResponseCommentDetail
from app.comment.dependency import can_user_delete_comment, valid_comment_id, valid_comment_posting_id
from app.posting import dependency as posting_dependency
from app.user import dependency as user_dependency

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
