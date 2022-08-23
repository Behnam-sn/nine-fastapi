from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    name: str
    password: str


class UserUpdate(BaseModel):
    username: str
    name: str
    bio: str


class PasswordUpdate(BaseModel):
    password: str
    new_password: str


# class Author(BaseModel):
#     id: int
#     username: str
#     name: str
#     is_superuser: bool

#     class Config:
#         orm_mode = True


class Owner(BaseModel):
    id: int
    username: str
    name: str
    is_superuser: bool

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
    name: str
    bio: str | None = None
    posts: int
    comments: int
    likes: int
    followers: int
    followings: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True
