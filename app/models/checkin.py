from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from app.database import Base
class CheckIn(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime)
    check_in_method = Column(String(50), nullable=False)
