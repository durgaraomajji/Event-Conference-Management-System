from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from app.database import Base
class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10,2), nullable=False)
    discount = Column(Numeric(10,2), default=0)
    tax = Column(Numeric(10,2), default=0)
    total_amount = Column(Numeric(10,2), nullable=False)
    purchase_status = Column(String(50), default="Pending")
    created_at = Column(DateTime)
