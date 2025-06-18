import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from app.database import Base


class PostLike(Base):
  __tablename__ = "post_likes"

  id = Column(Integer, primary_key=True, index=True, comment="게시글 좋아요 ID")
  post_id = Column(Integer, ForeignKey("posts.id"), comment="게시글 ID")
  user_id = Column(Integer, ForeignKey("users.id"), comment="유저 ID")
  created_at = Column(DateTime, nullable=False, default=datetime.now, comment="생성일시")