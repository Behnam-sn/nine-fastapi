from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(Text)
    modified_at = Column(Text)
    posts = relationship("Post", back_populates="author")
