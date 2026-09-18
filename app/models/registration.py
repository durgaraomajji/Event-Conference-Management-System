from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, UniqueConstraint
from app.database import Base
class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True)
    attendee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registration_date = Column(DateTime, nullable=False)
    registration_status = Column(String(50), default="Pending")
    __table_args__ = (UniqueConstraint("attendee_id", "event_id", name="uq_attendee_event"),)
