from pydantic import BaseModel
from src.schemas import Comment


class PostBase(BaseModel):
    text: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostLike(BaseModel):
    id: int
    post_id: int
    owner_id: int
    created_at: str

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    owner_id: int
    is_edited: bool
    is_active: bool
    created_at: str
    modified_at: str

    comments: list[Comment] = []
    likes: list[PostLike] = []

    class Config:
        orm_mode = True
