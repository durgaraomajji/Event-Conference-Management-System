from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Index
from app.database import Base
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    event_name = Column(String(200), nullable=False)
    description = Column(Text)
    event_type = Column(String(50), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    registration_start = Column(DateTime, nullable=False)
    registration_end = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String(50), default="Draft")
    city = Column(String(100))
    venue_id = Column(Integer, ForeignKey("venues.id"))
    is_deleted = Column(Boolean, default=False, nullable=False)
    __table_args__ = (Index("ix_events_status_type_city", "status", "event_type", "city"),)
