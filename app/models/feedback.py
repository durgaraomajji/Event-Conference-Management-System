from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from app.database import Base
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    speaker_id = Column(Integer, ForeignKey("speakers.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    rating = Column(Integer, nullable=False)
    feedback = Column(Text)
    __table_args__ = (UniqueConstraint("registration_id","session_id",name="uq_feedback_session"),)
