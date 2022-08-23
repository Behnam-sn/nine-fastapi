from pydantic import BaseModel
from src.schemas.user import Owner


class Follow(BaseModel):
    id: int
    follower_id: int
    following_id: int

    follower: Owner
    following: Owner

    class Config:
        orm_mode = True
