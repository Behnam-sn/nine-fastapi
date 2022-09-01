from pydantic import BaseModel
from src.schemas.user import Owner


class Follow(BaseModel):
    id: int
    follower_id: int
    following_id: int
    is_follower_active: bool
    is_following_active: bool

    follower: Owner
    following: Owner

    class Config:
        orm_mode = True
