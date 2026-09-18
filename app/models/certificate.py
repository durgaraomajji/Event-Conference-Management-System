from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True)
    certificate_number = Column(String(200), unique=True, nullable=False)
    attendee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    certificate_type = Column(String(100), nullable=False)
    status = Column(String(50), default="Issued")
