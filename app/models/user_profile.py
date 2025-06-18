import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.database import Base


class UserProfile(Base):
  __tablename__ = "user_profiles"

  id = Column(Integer, primary_key=True, index=True, comment="유저 프로필 ID")
  user_id = Column(Integer, ForeignKey("users.id"), comment="유저 ID")
  thumbnail_url = Column(String, nullable=True, comment="유저 프로필 썸네일 이미지 URL")
  description = Column(String, nullable=True, comment="유저 프로필 설명 Markdown")
  created_at = Column(DateTime, nullable=False, default=datetime.datetime.now, comment="생성일시")
  updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, comment="수정일시")
  deleted_at = Column(DateTime, nullable=True, comment="삭제일시")