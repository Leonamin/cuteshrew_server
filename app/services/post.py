from sqlalchemy.orm import Session

from app.core.exceptions import (
    PostNotAuthorizedException,
    PostNotFoundException,
    UserNotFoundException,
)
from app.repository.post_repository import PostRepository
from app.schemas.post import PostDetailRes, PostDraftRes, PostUpdateReq, PostUpdateRes


def create_draft(
    db: Session,
    user_id: int,
) -> PostDraftRes:
    repository = PostRepository(db)
    
    # 사용자 존재 확인
    user = repository.find_user_by_id(user_id)
    if not user:
        raise UserNotFoundException()
    
    # 임시저장 게시글 생성
    new_draft = repository.create_draft(user_id)
    return PostDraftRes(id=str(new_draft.id))


def update_post(
    db: Session,
    post_id: str,
    post: PostUpdateReq,
    user_id: int,
) -> PostUpdateRes:
    repository = PostRepository(db)
    
    # 사용자 존재 확인
    user = repository.find_user_by_id(user_id)
    if not user:
        raise UserNotFoundException()
    
    # 게시글 존재 확인
    db_post = repository.find_post_by_id(post_id)
    if not db_post:
        raise PostNotFoundException()
    
    # 권한 확인
    if db_post.user_id != user_id:
        raise PostNotAuthorizedException()
    
    # 업데이트할 데이터 준비
    update_data = {}
    if post.title is not None:
        update_data['title'] = post.title
    if post.content is not None:
        update_data['content'] = post.content
    if post.thumbnail_url is not None:
        update_data['thumbnail_url'] = post.thumbnail_url
    if post.publish is not None:
        update_data['is_draft'] = not post.publish
    
    # 게시글 업데이트
    updated_post = repository.update_post(db_post, update_data)
    return PostUpdateRes(id=str(updated_post.id))


def get_post_detail(
    db: Session,
    post_id: str,
) -> PostDetailRes:
    repository = PostRepository(db)
    
    # 게시글과 작성자 정보 조회
    result = repository.get_post_with_writer_info(post_id)
    if not result:
        raise PostNotFoundException()
    
    db_post, user_name, user_thumbnail_url = result
    
    # 임시저장 글은 조회 불가
    if db_post.is_draft:
        raise PostNotFoundException()
    
    return PostDetailRes(
        id=str(db_post.id),
        title=db_post.title,
        content=db_post.content,
        thumbnail_url=db_post.thumbnail_url,
        created_at=db_post.created_at,
        view_count=0,  # TODO: 실제 조회수 구현
        like_count=0,  # TODO: 실제 좋아요 수 구현
        comment_count=0,  # TODO: 실제 댓글 수 구현
        writer_id=db_post.user_id,
        writer_name=user_name,
        writer_thumbnail_url=user_thumbnail_url,
    )