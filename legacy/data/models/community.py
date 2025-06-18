from sqlalchemy import BigInteger, Column, Integer, String

from app.db.database import Base


class Community(Base):
    __tablename__ = "communities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    showname = Column(String)
    # 권한 어드민 일반 등
    read_authority = Column(Integer)
    write_authority = Column(Integer)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    last_posted_at = Column(BigInteger)