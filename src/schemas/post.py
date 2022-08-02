from pydantic import BaseModel
from src.schemas import Comment


class PostBase(BaseModel):
    text: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Author(BaseModel):
    username: str
    name: str


class Post(PostBase):
    id: int
    # owner: Author
    owner_id: int
    is_edited: bool
    is_active: bool
    created_at: str
    modified_at: str

    comments: list[Comment] = []

    class Config:
        orm_mode = True
