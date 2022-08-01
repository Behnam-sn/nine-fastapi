from pydantic import BaseModel

from .user import Author


class PostBase(BaseModel):
    text: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


# class PostInDB(PostBase):
#     id: int
#     author_id: int
#     created_at: str
#     modified_at: str

#     class Config:
#         orm_mode = True


class Post(PostBase):
    id: int
    author: Author
    is_active: bool
    created_at: str
    modified_at: str

    class Config:
        orm_mode = True
