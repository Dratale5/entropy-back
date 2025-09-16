from sqlalchemy import Column, Integer, String, Sequence
from base import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, Sequence("users_sequence"), primary_key=True, nullable=False)
    username = Column(String(20), nullable=False)
    passwordHash = Column(String(128), nullable=False)
    token = Column(String(32), nullable=True)