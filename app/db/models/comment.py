from sqlalchemy import BigInteger, Column, Integer, String

from app.db.database import Base


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    # 댓글 작성자
    user_id = Column(Integer)
    # 댓글 내용
    comment = Column(String)
    # 생성 일자
    created_at = Column(BigInteger)
    # 댓글이 등록된 포스팅
    post_id = Column(Integer)
    # 댓글과 대댓글 계층
    comment_class = Column(Integer)
    # 한 댓글 그룹의 순서
    order = Column(Integer)
    # 댓글 그룹 id
    group_id = Column(Integer)