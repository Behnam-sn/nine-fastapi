from sqlalchemy import Boolean, Column, Integer, String, Text
from src.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    created_at = Column(Text)
    modified_at = Column(Text)
    is_active = Column(Boolean, default=True)
