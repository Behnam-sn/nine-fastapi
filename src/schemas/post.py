from datetime import datetime

from pydantic import BaseModel
from src.schemas.user import Owner


class PostCreate(BaseModel):
    text: str


class PostUpdate(BaseModel):
    text: str


class Post(BaseModel):
    id: int
    text: str
    comments: int
    likes: int
    owner_id: int
    is_modified: bool
    is_active: bool
    is_owner_active: bool
    created_at: datetime
    modified_at: datetime

    owner: Owner

    class Config:
        orm_mode = True
