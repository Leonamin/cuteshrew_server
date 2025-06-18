# Global Exception

from fastapi import HTTPException, status


def DatabaseError(detail: str):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail)


def HashValueError():
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Hash method failed because of value error")


def HashTypeError():
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Hash method failed because of type error")


def UnknownError(detail: str):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail)


def UnauthorizedException():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Your don't have permission")
