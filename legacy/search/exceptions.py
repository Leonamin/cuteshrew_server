from fastapi import HTTPException, status


def InvalidLoadCountException():
    return HTTPException(status_code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
                         detail="Load count must be less than 100 or over than 0")


def InvalidStartPointException():
    return HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                         detail="Search start point must be higher than 0")
