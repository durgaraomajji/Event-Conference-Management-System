from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base
class EventSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    speaker_id = Column(Integer, ForeignKey("speakers.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    session_type = Column(String(50), nullable=False)
