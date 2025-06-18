import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from app.database import Base


class PostView(Base):
    __tablename__ = "post_views"

    id = Column(Integer, primary_key=True, index=True, comment="게시글 조회 ID")
    post_id = Column(Integer, ForeignKey("posts.id"), comment="게시글 ID")
    user_id = Column(Integer, ForeignKey("users.id"), comment="유저 ID")
    created_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now, comment="생성일시")
