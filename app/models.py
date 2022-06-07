from enum import unique
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Community(Base):
    __tablename__ = "communities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    showname = Column(String)
    type = Column(Integer)
    created_at = Column(BigInteger)
    published_at = Column(BigInteger)

    postings = relationship("Posting", back_populates="own_community")


class Posting(Base):
    __tablename__ = "postings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    published_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    community_id = Column(Integer, ForeignKey('communities.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    own_community = relationship("Community", back_populates="postings")
    creator = relationship("User", back_populates="postings")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True)
    email = Column(String)
    password = Column(String)

    # 권한 어드민 일반 등
    authority = Column(Integer)

    created_at = Column(BigInteger)

    # 작성한 포스팅
    postings = relationship("Posting", back_populates="creator")
