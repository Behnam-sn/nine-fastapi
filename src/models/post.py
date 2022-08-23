from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.session import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    comments = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_edited = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner = relationship("User", back_populates="post_owner")
    # comments = relationship("Comment", back_populates="post")
    # likes = relationship("Like", back_populates="post")
