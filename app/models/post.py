import datetime
from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, Boolean
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="게시글 ID"
    )
    user_id = Column(Integer, ForeignKey("users.id"), comment="유저 ID")
    title = Column(String, nullable=False, comment="게시글 제목")
    content = Column(String, nullable=False, comment="게시글 내용 Markdown")
    thumbnail_url = Column(String, nullable=True, comment="게시글 썸네일 이미지 URL")
    is_draft = Column(
        Boolean, nullable=False, default=True, comment="게시글 임시 저장 여부"
    )
    created_at = Column(
        DateTime, nullable=False, default=datetime.datetime.now, comment="생성일시"
    )
    updated_at = Column(
        DateTime, nullable=False, default=datetime.datetime.now, comment="수정일시"
    )
    published_at = Column(DateTime, nullable=True, comment="게시일시")
    deleted_at = Column(DateTime, nullable=True, comment="삭제일시")
