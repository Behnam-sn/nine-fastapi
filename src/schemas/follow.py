from pydantic import BaseModel


class Follow(BaseModel):
    id: int
    follower_id: int
    following_id: int

    class Config:
        orm_mode = True
