from pydantic import BaseModel


class AuthToken(BaseModel):
    access_token: str
    token_type: str
    expire_time: int

    class Config():
        schema_extras = {
            'access_token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJLoK1pbiIsImV4cCI6MTY3MzYxODY2NH0.KwifXTksGbiVdJ4hvj8sYPUV1Fvnzv6cMWwAIoTgJlA",
            'token_type': 'bearer',
            'expire_time': 1673013864
        }
