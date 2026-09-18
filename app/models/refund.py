from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from app.database import Base
class Refund(Base):
    __tablename__ = "refunds"
    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)
    cancellation_reason = Column(String(500), nullable=False)
    refund_amount = Column(Numeric(10,2), nullable=False)
    refund_status = Column(String(50), default="Pending")
    refund_date = Column(DateTime)
