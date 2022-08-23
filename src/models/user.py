from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, index=True, nullable=True)
    bio = Column(String, index=True, nullable=True)
    posts = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    followings = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    post_owner = relationship("Post", back_populates="owner")
    comment_owner = relationship("Comment", back_populates="owner")
    like_owner = relationship("Like", back_populates="owner")
    follower_owner = relationship(
        "Follow", back_populates="follower", foreign_keys="Follow.follower_id"
    )
    following_owner = relationship(
        "Follow", back_populates="following", foreign_keys="Follow.following_id"
    )
