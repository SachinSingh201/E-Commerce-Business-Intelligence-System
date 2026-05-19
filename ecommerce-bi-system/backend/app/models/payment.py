from sqlalchemy import Column, String, Integer, Float, ForeignKey
from ..core.database import Base

class Payment(Base):
    __tablename__ = "payments"

    order_id = Column(String(50), ForeignKey("orders.order_id"), primary_key=True)
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String(50))
    payment_installments = Column(Integer)
    payment_value = Column(Float)
