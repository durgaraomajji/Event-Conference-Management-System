from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from app.database import Base
class SessionBooking(Base):
    __tablename__ = "session_bookings"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    registration_id = Column(Integer, ForeignKey("registrations.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    __table_args__ = (UniqueConstraint("session_id","registration_id",name="uq_session_registration"),)
