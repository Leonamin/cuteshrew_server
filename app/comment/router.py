from typing import List, Mapping
from fastapi import APIRouter
from fastapi import APIRouter, Depends, status

from app.comment.schemas import ResponseCommentDetail
from app.comment.dependency import valid_comment_id, valid_comment_posting_id

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


@router.post("", status_code=status.HTTP_201_CREATED)
def create_comment(community_name: str, post_id: int):
    pass


@router.post("/{group_id}", status_code=status.HTTP_201_CREATED)
def create_reply(community_name: str, post_id: int, group_id: int):
    pass


@router.put("/{comment_id}", status_code=status.HTTP_201_CREATED)
def update_comment(community_name: str, post_id: int, comment_id: int):
    pass


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(community_name: str, post_id: int, comment_id: int):
    pass
