from datetime import datetime

from pydantic import BaseModel
from src.schemas import Comment, Follow, Like, Post


class UserBase(BaseModel):
    username: str
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    bio: str


class PasswordUpdate(BaseModel):
    password: str
    new_password: str


class Author(BaseModel):
    id: int
    username: str
    name: str
    is_superuser: bool

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    bio: str | None = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    modified_at: datetime

    posts: list[Post] = []
    comments: list[Comment] = []
    likes: list[Like] = []
    followers: list[Follow] = []
    followings: list[Follow] = []

    class Config:
        orm_mode = True
