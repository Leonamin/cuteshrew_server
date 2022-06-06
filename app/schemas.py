from typing import List
from pydantic import BaseModel

class CommunityBase(BaseModel):
    name: str
    type: int