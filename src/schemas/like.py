from datetime import datetime

from pydantic import BaseModel
from src.schemas.user import Owner


class Like(BaseModel):
    id: int
    post_id: int | None = None
    comment_id: int | None = None
    owner_id: int
    created_at: datetime

    owner: Owner

    class Config:
        orm_mode = True
