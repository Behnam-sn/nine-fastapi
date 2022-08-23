from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.session import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    likes = Column(Integer, default=0)
    post_id = Column(Integer, ForeignKey("posts.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_modified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner = relationship("User", back_populates="comment_owner")
    # likes = relationship("Like", back_populates="comment")
