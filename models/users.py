from database.db import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)