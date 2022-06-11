from enum import Enum, auto


class Authority(Enum):
    # READER = 'READER'
    # WRITER = 'WRITER'
    # SUB_ADMIN = 'SUB_ADMIN'
    # ADMIN = 'ADMIN'
    # GOD = 'GOD'
    GOD = 9
    ADMIN = 4
    SUB_ADMIN = 3
    WRITER = 2

    READER = 1
