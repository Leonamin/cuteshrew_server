from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from app.core.exceptions import (
    PostNotAuthorizedException,
    PostNotFoundException,
    UserNotFoundException,
)
from app.repository.post_repository import PostRepository
from app.schemas.post import (
    PostDetailRes,
    PostDraftRes,
    PostSummaryRes,
    PostUpdateReq,
    PostUpdateRes,
)
from app.utils.content_parser import (
    move_temp_images_to_storage,
    cleanup_temp_images,
    extract_embedded_images_from_content,
)
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("post_service")


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

    logger.info(f"Updating post {post_id} by user {user_id}")

    # 사용자 존재 확인
    user = repository.find_user_by_id(user_id)
    if not user:
        logger.error(f"User not found: {user_id}")
        raise UserNotFoundException()

    # 게시글 존재 확인
    db_post = repository.find_post_by_id(post_id)
    if not db_post:
        logger.error(f"Post not found: {post_id}")
        raise PostNotFoundException()

    # 권한 확인
    if db_post.user_id != user_id:
        logger.error(
            f"Unauthorized access to post {post_id} by user {user_id}")
        raise PostNotAuthorizedException()

    # 업데이트할 데이터 준비
    update_data = {}
    if post.title is not None:
        update_data["title"] = post.title
    if post.content is not None:
        update_data["content"] = post.content
    if post.content_type is not None:
        update_data["content_type"] = post.content_type
    if post.thumbnail_url is not None:
        update_data["thumbnail_url"] = post.thumbnail_url
    if post.publish is not None:
        update_data["is_draft"] = not post.publish

    logger.debug(f"Update data prepared: {list(update_data.keys())}")

    # 이미지 처리 (게시글 발행이 아니더라도 이미지 처리)
    logger.info(f"Processing images for published post {post_id}")

    # 임시 이미지를 실제 저장소로 이동
    updated_content, moved_files = move_temp_images_to_storage(
        content=post.content,
        content_type=post.content_type or db_post.content_type,
        post_id=post_id,
        temp_path=settings.STORAGE_TEMP_PATH,
        storage_path=settings.STORAGE_POSTS_PATH
    )

    logger.info(f"Moved {len(moved_files)} images to storage")

    # content 업데이트
    update_data["content"] = updated_content

    # 임베딩된 이미지 목록 업데이트
    embedded_images = extract_embedded_images_from_content(
        content=updated_content,
        content_type=post.content_type or db_post.content_type
    )
    update_data["embedded_images"] = json.dumps(embedded_images)

    logger.info(f"Found {len(embedded_images)} embedded images")

    # 사용하지 않는 임시 이미지 정리
    deleted_files = cleanup_temp_images(
        content=updated_content,
        content_type=post.content_type or db_post.content_type,
        temp_path=settings.STORAGE_TEMP_PATH
    )

    logger.info(f"Cleaned up {len(deleted_files)} unused temp images")

    # 게시글 업데이트
    updated_post = repository.update_post(db_post, update_data)
    logger.info(f"Successfully updated post {post_id}")

    return PostUpdateRes(id=str(updated_post.id))


def get_post_detail(
    db: Session,
    post_id: str,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
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

    # 게시글 조회수 증가 (로그인/익명 사용자 모두 지원)
    repository.increment_view_count(
        post_id=post_id, user_id=user_id, ip_address=ip_address, user_agent=user_agent
    )

    # 게시글 조회수 조회
    view_count = repository.get_post_view_count(post_id)

    return PostDetailRes(
        id=str(db_post.id),
        title=db_post.title,
        content=db_post.content,
        thumbnail_url=db_post.thumbnail_url,
        created_at=db_post.created_at,
        view_count=view_count,
        like_count=0,  # TODO: 실제 좋아요 수 구현
        comment_count=0,  # TODO: 실제 댓글 수 구현
        writer_id=db_post.user_id,
        writer_name=user_name,
        writer_thumbnail_url=user_thumbnail_url,
    )


def get_recent_posts(
    db: Session,
    page: int = 1,
    limit: int = 10,
) -> List[PostSummaryRes]:
    """페이징 기반 최근 게시글 조회"""
    repository = PostRepository(db)
    posts_data = repository.get_recent_posts(page, limit)

    return [
        PostSummaryRes(
            id=post_data["id"],
            title=post_data["title"],
            short_content=post_data["short_content"],
            thumbnail_url=post_data["thumbnail_url"],
            created_at=post_data["created_at"],
            view_count=post_data["view_count"],
            like_count=0,
            comment_count=0,
            writer_id=post_data["writer_id"],
            writer_name=post_data["writer_name"],
            writer_thumbnail_url=post_data["writer_thumbnail_url"],
        )
        for post_data in posts_data
    ]


def get_top_posts(
    db: Session,
    page: int = 1,
    limit: int = 10,
    days: int = 7,
) -> List[PostSummaryRes]:
    """조회수 기준 인기 게시글 조회"""
    repository = PostRepository(db)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    posts_data = repository.get_top_posts(page, limit, start_date, end_date)

    return [
        PostSummaryRes(
            id=post_data["id"],
            title=post_data["title"],
            short_content=post_data["short_content"],
            thumbnail_url=post_data["thumbnail_url"],
            created_at=post_data["created_at"],
            view_count=post_data["view_count"],
            like_count=0,
            comment_count=0,
            writer_id=post_data["writer_id"],
            writer_name=post_data["writer_name"],
            writer_thumbnail_url=post_data["writer_thumbnail_url"],
        )
        for post_data in posts_data
    ]
