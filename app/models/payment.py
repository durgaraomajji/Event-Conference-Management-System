from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from app.database import Base
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)
    transaction_id = Column(String(200), unique=True, nullable=False)
    payment_method = Column(String(50), nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    payment_status = Column(String(50), default="Pending")
    payment_date = Column(DateTime)
