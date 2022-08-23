from datetime import datetime

from pydantic import BaseModel
from src.schemas.user import User


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    likes: int
    post_id: int
    owner_id: int
    is_active: bool
    is_modified: bool
    created_at: datetime
    modified_at: datetime

    owner: User

    class Config:
        orm_mode = True
