from fastapi import APIRouter

from app.auth.router import router as AuthRouter
from app.user.router import router as UserRouter
from app.comment.router import router as CommentRouter
from app.community.router import router as CommunityRouter
from app.posting.router import router as PostingRouter
from app.search.router import router as SearchRouter
from app.page.router import router as PageRouter


router = APIRouter(
    prefix="/apiv2",
)

router.include_router(AuthRouter)
router.include_router(UserRouter)
router.include_router(CommentRouter)
router.include_router(CommunityRouter)
router.include_router(PostingRouter)
router.include_router(SearchRouter)
router.include_router(PageRouter)
