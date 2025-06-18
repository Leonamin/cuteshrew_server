
import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, comment="게시글 ID")
    user_id = Column(Integer, ForeignKey("users.id"), comment="유저 ID")
    title = Column(String, nullable=False, comment="게시글 제목")
    content = Column(String, nullable=False, comment="게시글 내용 Markdown")
    thumbnail_url = Column(String, nullable=True, comment="게시글 썸네일 이미지 URL")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="생성일시")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, comment="수정일시")
    deleted_at = Column(DateTime, nullable=True, comment="삭제일시")
