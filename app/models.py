from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Enum, select, func
from sqlalchemy.orm import relationship, column_property

from app.dependency import Authority
from .database import Base


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
    email = Column(String, unique=True)
    password = Column(String)

    # 권한 어드민 일반 등
    authority = Column(Enum(Authority))

    created_at = Column(BigInteger)

    # 작성한 포스팅
    postings = relationship("Posting", back_populates="creator")


class Community(Base):
    __tablename__ = "communities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    showname = Column(String)
    # 권한 어드민 일반 등
    authority = Column(Enum(Authority))
    created_at = Column(BigInteger)
    published_at = Column(BigInteger)

    postings = relationship("Posting", back_populates="own_community")
    postings_count = column_property(
        select([func.count(Posting.id)]).scalar_subquery())
