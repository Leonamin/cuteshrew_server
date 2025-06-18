from sqlalchemy import BigInteger, Column, Integer, String
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True)
    email = Column(String, unique=True)

    # 해싱된 비밀번호
    password = Column(String)

    # 권한 어드민 일반 등 Authority
    # 9 : GOD
    # 4 : ADMIN
    # 3 : SUB_ADMIN
    # 2 : WRITER
    # 1 : READER
    authority = Column(Integer)

    # Unix Timestamp
    created_at = Column(BigInteger)