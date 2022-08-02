from pydantic import BaseModel


class Like(BaseModel):
    id: int
    post_id: int | None = None
    comment_id: int | None = None
    owner_id: int
    created_at: str

    class Config:
        orm_mode = True
