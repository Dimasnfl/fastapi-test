from database.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    
    reports = relationship("Reports", back_populates="category")