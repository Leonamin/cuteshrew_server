from enum import Enum


class Authority(str, Enum):
    GOD = 'GOD',
    ADMIN = 'ADMIN',
    SUB_ADMIN = 'SUB_ADMIN',
    WRITER = 'WRITER',
    READER = 'READER'
