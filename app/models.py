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

    own_community = relationship("Community", back_populates="postings")
