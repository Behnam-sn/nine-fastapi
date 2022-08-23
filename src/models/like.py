from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.session import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner = relationship("User", back_populates="like_owner")
    # post = relationship("Post", back_populates="likes")
    # comment = relationship("Comment", back_populates="likes")
