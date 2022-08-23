from datetime import datetime

from pydantic import BaseModel
from src.schemas.user import User


class PostBase(BaseModel):
    text: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    comments: int
    likes: int
    owner_id: int
    is_active: bool
    is_modified: bool
    created_at: datetime
    modified_at: datetime

    owner: User

    class Config:
        orm_mode = True
