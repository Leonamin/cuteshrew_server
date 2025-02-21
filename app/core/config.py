
from typing import List, Union

from pydantic import AnyHttpUrl, Field, validator
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    VERSION: str
    ENVIRONMENT: str
    SHOW_DOCS_ENVIRONMENT: str = ("local", "staging")  #  docs가 보일 환경은 명시적으로 정할것
    SECRET_KEY: str = Field(default= None)

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'

# python ~~~ 실행 위치에 따라 .env 실행하는게 달라진다.
# python 명령어를 실행 혹은 uvicorn을 실행할 때 실행하는 디렉토리 내에 .env 파일을 읽는 것이다.
settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
# settings = Settings(_env_file=['prod.env', 'aaa.env'], _env_file_encoding='utf-8')

# print(settings)
