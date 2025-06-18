from fastapi import HTTPException, status


def UserNotFoundException():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="User not found")
