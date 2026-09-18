from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(30))
    password_hash = Column(String(500), nullable=False)
    role = Column(String(50), nullable=False, default="Attendee")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime)
