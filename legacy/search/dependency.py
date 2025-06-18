from typing import List, Mapping, Optional

from fastapi import Depends
from app.search.constants import MAX_POSTING_LOAD_COUNT, MAX_COMMENT_LOAD_COUNT, DEFAULT_COMMENT_LOAD_COUNT, DEFAULT_POSTING_LOAD_COUNT
from app.search.exceptions import InvalidLoadCountException, InvalidStartPointException

from app.search import service
from app.user import dependency as user_dependency
from app.posting.exceptions import PostingNotFound
from app.comment.exceptions import CommentNotFound


def valid_posting_load_cound(load_count: Optional[int] = DEFAULT_POSTING_LOAD_COUNT) -> int:
    if load_count == 0:
        load_count = MAX_POSTING_LOAD_COUNT
    if (load_count > MAX_POSTING_LOAD_COUNT or load_count <= 0):
        raise InvalidLoadCountException()
    return load_count


def valid_comment_load_cound(load_count: Optional[int] = DEFAULT_COMMENT_LOAD_COUNT) -> int:
    if load_count == 0:
        load_count = MAX_COMMENT_LOAD_COUNT
    if (load_count > MAX_COMMENT_LOAD_COUNT or load_count <= 0):
        raise InvalidLoadCountException()
    return load_count


def valid_skip_until_id(
    skip_until_id: Optional[int] = None,
) -> int:
    if (skip_until_id != None and skip_until_id < 0):
        raise InvalidStartPointException()
    return skip_until_id


async def valid_posting_search_filters(
    user: Mapping = Depends(user_dependency.valid_user_name),
    skip_until_id: Optional[int] = Depends(valid_skip_until_id),
    load_count: int = Depends(valid_posting_load_cound)
) -> Mapping:
    postings: List[Mapping] = await service.get_postings_by_user_id(user.id, load_count, skip_until_id)
    if not len(postings):
        raise PostingNotFound()
    return postings


async def valid_comment_search_filters(
    user: Mapping = Depends(user_dependency.valid_user_name),
    skip_until_id: Optional[int] = Depends(valid_skip_until_id),
    load_count: int = Depends(valid_comment_load_cound)
) -> Mapping:
    comments: List[Mapping] = await service.get_comments_by_user_id(user.id, load_count, skip_until_id)
    if not len(comments):
        raise CommentNotFound()
    return comments
