from enum import Enum, auto
from functools import lru_cache
from typing import Mapping

from fastapi import Depends
from app.core import config

# @Iru_cache 데코레이터가 위에 있으면 Settings 객체는 처음 호출될 때 한번만 생성될 것이다.
# 대충 원리가 어떻게 되냐면 실행한 함수 -> get_settings()가 되야겠지만 아래 print("test!")는 1번만 실행된다.
# 왜냐면 줘야하는 리턴값은 항상 똑같으므로 리턴값을 저장해서 실행한 함수 -> 저장한 리턴값 -> 리턴값 반환 이렇게 된다.
# 다만 파라미터가 있는 경우 파라미터가 달라지면 새로운 리턴 값을 줘야하므로 이때는 get_settings()를 실행하고 리턴값을 다시 저장한다.
@lru_cache()
def get_settings():
    return config.Settings(_env_file='.env', _env_file_encoding='utf-8')
    # return config.settings
    
#@lru_cache()를 중복하면 동작이 안되는 것 같다.
def get_secret_key(settings: config.Settings = Depends(get_settings)) -> Mapping:
    return settings.SECRET_KEY