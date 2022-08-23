from pydantic import BaseModel


class Id(BaseModel):
    id: int

    class Config:
        orm_mode = True
