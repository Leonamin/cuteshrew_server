from typing import List
from pydantic import BaseModel

class CommunityBase(BaseModel):
    name: str
    showname: str
    type: int
    class Config():
        orm_mode = True

class PostingBase(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True

class ShowCommunity(CommunityBase):
    showname: str
    type: int
    postings: List[PostingBase]
    class Config():
        orm_mode = True
    