from datetime import datetime

from pydantic import BaseModel
from src.schemas.user import Owner


class CommentCreate(BaseModel):
    text: str
    post_id: int


class CommentUpdate(BaseModel):
    text: str


class Comment(BaseModel):
    id: int
    text: str
    likes: int
    post_id: int
    owner_id: int
    is_active: bool
    is_modified: bool
    created_at: datetime
    modified_at: datetime

    owner: Owner

    class Config:
        orm_mode = True
