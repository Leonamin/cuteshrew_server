from typing import Optional
from pydantic import BaseModel

from app.dependency import Authority


class ReqeustCommunityCreate(BaseModel):
    name: str
    showname: str
    authority: Authority

    class Config:
        schema_extra = {
            "example": {
                "name": "general",
                "showname": "자유게시판",
                "authority": 9,
            }
        }

class ResponseCommunityInfo(BaseModel):
    id: Optional[int] = None
    name: str
    showname: str
    authority: Optional[Authority] = None
    created_at: Optional[int] = None
    published_at: Optional[int] = None
    posting_count: Optional[int] = None
    
    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "id" : 1,
                "name": "general",
                "showname": "자유게시판",
                "authority": 9,
                "created_at": 1672791019,
                "published_at" : 1672794023,
                "posting_count": 123,                
            }
        }
        
        
class ResponseCommunityWithPostings(ResponseCommunityInfo):
    postings: None
    
    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "id" : 1,
                "name": "general",
                "showname": "자유게시판",
                "authority": 9,
                "created_at": 1672791019,
                "published_at" : 1672794023,
                "posting_count": 123,     
                "postings" : [],           
            }
        }