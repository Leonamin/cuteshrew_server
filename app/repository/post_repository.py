from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Tuple
from datetime import datetime, timedelta

from app.models.post import Post
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.post_view import PostViewCount, PostView
from app.utils.content_parser import parse_content_to_plain_text


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_user_by_id(self, user_id: int) -> Optional[User]:
        """사용자 ID로 사용자 조회"""
        return self.db.query(User).filter(User.id == user_id).first()

    def create_draft(self, user_id: int) -> Post:
        """임시저장 게시글 생성"""
        new_draft = Post(
            user_id=user_id,
            title="",
            content="",
            is_draft=True,
        )
        self.db.add(new_draft)
        self.db.commit()
        self.db.refresh(new_draft)
        return new_draft

    def find_post_by_id(self, post_id: str) -> Optional[Post]:
        """게시글 ID로 게시글 조회"""
        return self.db.query(Post).filter(Post.id == UUID(post_id)).first()

    def update_post(self, post: Post, update_data: dict) -> Post:
        """게시글 업데이트"""
        for field, value in update_data.items():
            if value is not None:
                setattr(post, field, value)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_post_with_writer_info(
        self, post_id: str
    ) -> Optional[Tuple[Post, str, str]]:
        """게시글과 작성자 정보 함께 조회"""
        db_post = self.find_post_by_id(post_id)
        if not db_post:
            return None

        db_user = self.find_user_by_id(db_post.user_id)
        db_user_profile = (
            self.db.query(UserProfile)
            .filter(UserProfile.user_id == db_post.user_id)
            .first()
        )

        user_name = db_user.name if db_user else ""
        user_thumbnail_url = db_user_profile.thumbnail_url if db_user_profile else ""

        return db_post, user_name, user_thumbnail_url

    def get_recent_posts(self, page: int, limit: int) -> List[dict]:
        """최근 게시글 조회 (Offset-based) - 작성자 정보와 조회수 포함"""
        from sqlalchemy import func

        results = (
            self.db.query(
                Post,
                User.name.label("writer_name"),
                UserProfile.thumbnail_url.label("writer_thumbnail_url"),
                func.coalesce(PostViewCount.view_count, 0).label("view_count"),
            )
            .join(User, Post.user_id == User.id)
            .outerjoin(UserProfile, Post.user_id == UserProfile.user_id)
            .outerjoin(PostViewCount, Post.id == PostViewCount.post_id)
            .filter(Post.is_draft == False, Post.deleted_at.is_(None))
            .order_by(Post.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return [
            {
                "id": str(post.id),
                "title": post.title,
                "short_content": parse_content_to_plain_text(
                    post.content, 
                    post.content_type or "markdown", 
                    200
                ),
                "thumbnail_url": post.thumbnail_url,
                "created_at": post.created_at,
                "view_count": view_count,
                "writer_id": post.user_id,
                "writer_name": writer_name or "",
                "writer_thumbnail_url": writer_thumbnail_url or "",
            }
            for post, writer_name, writer_thumbnail_url, view_count in results
        ]

    def get_top_posts(
        self, page: int, limit: int, start_date: datetime, end_date: datetime
    ) -> List[dict]:
        """인기 게시글 조회 (조회수 기준, Offset-based)"""
        results = (
            self.db.query(
                Post,
                User.name.label("writer_name"),
                UserProfile.thumbnail_url.label("writer_thumbnail_url"),
                func.coalesce(PostViewCount.view_count, 0).label("view_count"),
            )
            .join(User, Post.user_id == User.id)
            .outerjoin(UserProfile, Post.user_id == UserProfile.user_id)
            .outerjoin(PostViewCount, Post.id == PostViewCount.post_id)
            .filter(
                Post.created_at >= start_date,
                Post.created_at <= end_date,
                Post.is_draft == False,  # 임시저장 제외
                Post.deleted_at.is_(None),  # 삭제된 게시글 제외
            )
            .order_by(
                func.coalesce(
                    PostViewCount.view_count, 0
                ).desc(),  # 조회수가 없는 경우 0으로 처리
                Post.created_at.desc(),  # 조회수가 같으면 최신순
            )
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return [
            {
                "id": str(post.id),
                "title": post.title,
                "short_content": parse_content_to_plain_text(
                    post.content, 
                    post.content_type or "markdown", 
                    200
                ),
                "thumbnail_url": post.thumbnail_url,
                "created_at": post.created_at,
                "view_count": view_count,
                "writer_id": post.user_id,
                "writer_name": writer_name or "",
                "writer_thumbnail_url": writer_thumbnail_url or "",
            }
            for post, writer_name, writer_thumbnail_url, view_count in results
        ]

    def get_post_view_count(self, post_id: str) -> int:
        """게시글 조회수 조회"""
        view_count = (
            self.db.query(PostViewCount)
            .filter(PostViewCount.post_id == UUID(post_id))
            .first()
        )
        return view_count.view_count if view_count else 0

    def increment_view_count(
        self,
        post_id: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """게시글 조회수 증가 (중복 조회 방지)

        Args:
            post_id: 게시글 ID
            user_id: 사용자 ID (로그인한 경우)
            ip_address: IP 주소 (익명 사용자용)
            user_agent: User Agent (선택사항)
        """
        # 이미 조회했는지 확인
        query = self.db.query(PostView).filter(PostView.post_id == UUID(post_id))

        if user_id:
            # 로그인한 사용자: user_id로 중복 체크
            query = query.filter(PostView.user_id == user_id)
        elif ip_address:
            # 익명 사용자: IP 주소로 중복 체크 (24시간 내)
            yesterday = datetime.now() - timedelta(days=1)
            query = query.filter(
                PostView.ip_address == ip_address, PostView.created_at >= yesterday
            )
        else:
            # user_id도 ip_address도 없는 경우는 무시
            return False

        existing_view = query.first()

        if existing_view:
            return False  # 이미 조회한 게시글

        # 새로운 조회 기록 추가
        new_view = PostView(
            post_id=UUID(post_id),
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(new_view)

        # 조회수 카운터 업데이트
        view_counter = (
            self.db.query(PostViewCount)
            .filter(PostViewCount.post_id == UUID(post_id))
            .first()
        )

        if not view_counter:
            view_counter = PostViewCount(post_id=UUID(post_id))
            self.db.add(view_counter)

        view_counter.view_count += 1

        # 고유 조회수 업데이트 (중복 제거)
        # 로그인 사용자는 user_id 기준, 익명 사용자는 IP 기준
        if user_id:
            unique_count = (
                self.db.query(PostView)
                .filter(PostView.post_id == UUID(post_id))
                .filter(PostView.user_id.isnot(None))
                .distinct(PostView.user_id)
                .count()
            )
        else:
            # 익명 사용자는 최근 24시간 내 IP 기준
            yesterday = datetime.now() - timedelta(days=1)
            unique_count = (
                self.db.query(PostView)
                .filter(PostView.post_id == UUID(post_id))
                .filter(PostView.created_at >= yesterday)
                .distinct(PostView.ip_address)
                .count()
            )

        view_counter.unique_view_count = unique_count

        self.db.commit()
        return True
