from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.session import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_post_active = Column(Boolean, default=True)
    is_post_owner_active = Column(Boolean, default=True)
    is_comment_active = Column(Boolean, default=True)
    is_comment_owner_active = Column(Boolean, default=True)
    is_owner_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner = relationship("User", back_populates="like_owner")
