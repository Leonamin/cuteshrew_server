from typing import Optional
from pydantic import BaseModel

"""
유저의 자세한 정보
nickname: 닉네임
email: 이메일
posting_count: 작성한 게시글 수
comment_count: 작성한 댓글 수
introduction: 유저 자기소개
"""
class ResponseUserDetail(BaseModel):
    nickname: str
    email: str
    posting_count: Optional[int]
    comment_count: Optional[int]
    introduction: Optional[str] 
    
    class Config():
        orm_mode = True