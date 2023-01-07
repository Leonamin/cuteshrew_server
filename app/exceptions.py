# Global Exception

from fastapi import HTTPException, status


def DatabaseError(detail: str):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail)
