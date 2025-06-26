import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UUID
from app.database import Base


class PostView(Base):
    __tablename__ = "post_views"

    id = Column(Integer, primary_key=True, index=True, comment="게시글 조회 ID")
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), comment="게시글 ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="유저 ID (로그인한 경우)")
    ip_address = Column(String(45), nullable=True, comment="IP 주소 (익명 사용자용)")
    user_agent = Column(String(500), nullable=True, comment="User Agent")
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now, comment="생성일시")

    __table_args__ = (
        # 같은 IP에서 같은 게시글을 중복 조회하는 것을 방지
        # (로그인 사용자는 user_id로, 익명 사용자는 ip_address로)
    )


class PostViewCount(Base):
    """게시글 조회수 카운터 테이블"""
    __tablename__ = "post_view_counts"

    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True, comment="게시글 ID")
    view_count = Column(Integer, default=0, comment="총 조회수")
    unique_view_count = Column(Integer, default=0, comment="고유 조회수 (중복 제거)")
    updated_at = Column(DateTime, nullable=False, 
                       default=datetime.datetime.now, 
                       onupdate=datetime.datetime.now, 
                       comment="업데이트 일시")
