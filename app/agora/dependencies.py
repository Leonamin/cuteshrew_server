from typing import Mapping


def valid_time_limit(
    time_limit: int = 10,
) -> Mapping:
    if time_limit > 60 or time_limit < 0:
        time_limit = 10
    return time_limit


def valid_role(
    role: int
) -> Mapping:
    if (role != 1 or role != 2):
        role = 2
    return role
