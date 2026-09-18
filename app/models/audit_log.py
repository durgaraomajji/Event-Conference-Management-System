from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer)
    details = Column(Text)
    created_at = Column(DateTime, nullable=False)
