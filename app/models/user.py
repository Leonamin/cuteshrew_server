import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.database import Base


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.now)
  updated_at = Column(DateTime, nullable=False, default=datetime.now)
  deleted_at = Column(DateTime, nullable=True)