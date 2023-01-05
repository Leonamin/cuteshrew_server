from fastapi import APIRouter
from . import community, posting, authentication, user, comment, search
from app.auth import router as auth_module

router = APIRouter(
    prefix="/api",
)

router.include_router(community.router)
router.include_router(posting.router)
router.include_router(user.router)
router.include_router(authentication.router)
router.include_router(comment.router)
router.include_router(search.router)
router.include_router(auth_module.router)