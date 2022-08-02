from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from src.database.session import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_edited = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(Text)
    modified_at = Column(Text)

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
