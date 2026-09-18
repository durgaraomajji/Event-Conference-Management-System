from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database import Base
class Speaker(Base):
    __tablename__ = "speakers"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(30))
    bio = Column(Text)
    expertise = Column(String(300))
    company = Column(String(200))
    experience = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)
