from sqlalchemy import BigInteger, Boolean, Column, Integer, String
from app.db.database import Base


class Posting(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    # Markdown이던 Quill이던 어쨋거나 텍스트이다.
    content = Column(String)

    # 0 : Markdown
    # 1 : Quill
    content_type = Column(Integer)

    # Unix Timestamp
    created_at = Column(BigInteger)

    # Unix Timestamp
    updated_at = Column(BigInteger)
    
    # communities 테이블의 id
    community_id = Column(Integer)

    # users 테이블의 id
    user_id = Column(Integer)
    is_locked = Column(Boolean)
    password = Column(String)