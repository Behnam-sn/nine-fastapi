from pydantic import BaseModel
from src.schemas.user import User


class Follow(BaseModel):
    id: int
    follower_id: int
    following_id: int

    follower: User
    following: User

    class Config:
        orm_mode = True
