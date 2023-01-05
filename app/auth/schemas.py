from pydantic import BaseModel


class AuthToken(BaseModel):
    access_token: str
    token_type: str
    expire_time: int