from pydantic import BaseModel


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
    # picture_url: str
    created_at: str
    modified_at: str

    class Config:
        orm_mode = True
