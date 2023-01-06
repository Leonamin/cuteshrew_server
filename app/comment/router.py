from fastapi import APIRouter
from fastapi import APIRouter, Depends, status


router = APIRouter(
    # prefix="/community/{community_name}/{post_id}/comment",
    prefix="/comment",
    tags=['comment']
)


@router.get("/{page_num}", response_model_exclude_none=True)
def get_page(community_name: str, post_id: int, page_num: int, count_per_page: int):
    pass


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
