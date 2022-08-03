from pydantic import BaseModel
from src.schemas import Comment, Follow, Like, Post


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    name: str
    password: str


class UserUpdate(BaseModel):
    username: str
    name: str
    bio: str


class PasswordUpdate(BaseModel):
    password: str
    new_password: str


class User(UserBase):
    id: int
    name: str
    bio: str | None = None
    is_active: bool
    is_superuser: bool
    created_at: str
    modified_at: str

    posts: list[Post] = []
    comments: list[Comment] = []
    likes: list[Like] = []
    followers: list[Follow] = []
    followings: list[Follow] = []

    class Config:
        orm_mode = True
