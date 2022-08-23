from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.database.session import Base


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    following_id = Column(Integer, ForeignKey("users.id"))

    follower = relationship(
        "User", back_populates="follower_owner", foreign_keys=[follower_id]
    )
    following = relationship(
        "User", back_populates="following_owner", foreign_keys=[following_id]
    )
