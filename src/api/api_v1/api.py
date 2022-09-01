from fastapi import APIRouter
from src.api.api_v1.endpoints import (active_comments, active_follows,
                                      active_posts, active_users, auth,
                                      comments, follows, likes, posts, users)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    active_users.router, prefix="/active-users", tags=["active users"]
)
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(
    active_posts.router, prefix="/active-posts", tags=["active posts"]
)
api_router.include_router(
    comments.router, prefix="/comments", tags=["comments"]
)
api_router.include_router(
    active_comments.router, prefix="/active-comments", tags=["active comments"]
)
api_router.include_router(likes.router, prefix="/likes", tags=["likes"])
api_router.include_router(follows.router, prefix="/follows", tags=["follows"])
api_router.include_router(
    active_follows.router, prefix="/active-follows", tags=["active follows"]
)
