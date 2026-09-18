from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from app.database import Base
class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    ticket_type = Column(String(50), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    quantity = Column(Integer, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    sale_start = Column(DateTime, nullable=False)
    sale_end = Column(DateTime, nullable=False)
