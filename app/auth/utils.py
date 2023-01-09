from datetime import datetime
from enum import Enum
from passlib.context import CryptContext
import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)

class TimeFormat(Enum):
    SEC = 'seconds'
    MILLIS = 'millis'
    MICROS = 'micros'

def getCurrentUnixTimeStamp(time_format: TimeFormat = None):
    now = datetime.utcnow()
    # if time_format is TimeFormat.SEC:
    return round(time.mktime(now.timetuple()))
    # elif time_format is TimeFormat.MILLIS: