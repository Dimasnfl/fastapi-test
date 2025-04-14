from database.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

class Reports(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False)
    image_path = Column(String, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.user_id"))
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    
    owner = relationship("Users", back_populates="reports")
    category = relationship("Categories", back_populates="reports")
    
