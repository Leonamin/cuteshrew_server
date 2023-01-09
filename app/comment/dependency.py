from typing import Mapping, List, Optional

from fastapi import Depends

from app.comment import service
from app.comment.constants import DEFAULT_COMMENT_LOAD_COUNT, MAX_COMMENT_LOAD_COUNT
from app.comment.exceptions import CommentNotFound, InvalidLoadCountException

from app.posting import service as posting_service
from app.posting import dependency as posting_dependency


async def valid_comment_id(
    comment_id: int,
) -> Mapping:
    comment = await service.get_comment_by_comment_id(comment_id)

    if not comment:
        raise CommentNotFound()
    return comment


# 최대 개수 제한
def valid_load_count(load_count: Optional[int] = DEFAULT_COMMENT_LOAD_COUNT) -> int:
    if load_count == None:
        load_count = MAX_COMMENT_LOAD_COUNT
    if (load_count > MAX_COMMENT_LOAD_COUNT or load_count <= 0):
        raise InvalidLoadCountException()
    return load_count

async def valid_comment_posting_id(
    posting_id: int,
    load_count: int = Depends(valid_load_count)
) -> List[Mapping]:
    posting: Mapping = await posting_dependency.valid_posting_id(posting_id)
    comments: List = await service.get_comments_by_posting_id(posting.id, load_count)
    if not len(comments):
        raise CommentNotFound()
    return comments
