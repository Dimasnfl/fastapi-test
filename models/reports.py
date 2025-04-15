from database.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Reports(Base):
    __tablename__ = "reports"

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body = Column(Text, nullable=False)
    image_path = Column(String, nullable=True)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    
    owner = relationship("Users", back_populates="reports")
    category = relationship("Categories", back_populates="reports")
    
