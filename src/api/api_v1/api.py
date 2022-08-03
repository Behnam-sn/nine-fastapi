from fastapi import APIRouter
from src.api.api_v1.endpoints import (auth, comments, follows, likes, posts,
                                      users)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(
    comments.router, prefix="/comments", tags=["comments"]
)
api_router.include_router(likes.router, prefix="/likes", tags=["likes"])
api_router.include_router(follows.router, prefix="/follows", tags=["follows"])
