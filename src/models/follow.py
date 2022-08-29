from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.session import Base


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    following_id = Column(Integer, ForeignKey("users.id"))
    is_follower_active = Column(Boolean, default=True)
    is_following_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    follower = relationship(
        "User", back_populates="follower_owner", foreign_keys=[follower_id]
    )
    following = relationship(
        "User", back_populates="following_owner", foreign_keys=[following_id]
    )
