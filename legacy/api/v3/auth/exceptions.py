from typing import Any, Dict, Optional
from fastapi import HTTPException, status


def InvalidCredentials():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)


def IncorrectPassword():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Incorrect password")
