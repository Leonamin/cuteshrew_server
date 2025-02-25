from sqlalchemy import BigInteger, Column, Enum, Integer, String
from app.db.database import Base
from app.dependency import Authority
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    # 권한 어드민 일반 등
    authority = Column(Enum(Authority))

    created_at = Column(BigInteger)

    # 작성한 포스팅
    # postings = relationship("Posting", back_populates="creator")
    # comments = relationship("Comment", back_populates="creator")