from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(CommentBase):
    pass


class CommentLike(BaseModel):
    id: int
    comment_id: int
    owner_id: int
    created_at: str

    class Config:
        orm_mode = True


class Comment(CommentBase):
    id: int
    post_id: int
    owner_id: int
    is_edited: bool
    is_active: bool
    created_at: str
    modified_at: str

    likes: list[CommentLike] = []

    class Config:
        orm_mode = True
