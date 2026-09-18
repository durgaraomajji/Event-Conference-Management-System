from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base
class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True)
    venue_name = Column(String(200), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    facilities = Column(Text)
    status = Column(String(50), default="Active")
class Hall(Base):
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    hall_name = Column(String(150), nullable=False)
    capacity = Column(Integer, nullable=False)
    floor = Column(Integer)
    availability_status = Column(String(50), default="Available")
