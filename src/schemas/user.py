from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    name: str
    password: str


class User(UserBase):
    id: int
    name: str
    bio: Optional[str] = None
    # picture_url: str
    created_at: str
    modified_at: str

    class Config:
        orm_mode = True
