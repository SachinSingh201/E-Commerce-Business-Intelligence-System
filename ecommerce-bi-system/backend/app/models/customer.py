from sqlalchemy import Column, String, Integer
from ..core.database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String(50), primary_key=True)
    customer_unique_id = Column(String(50))
    customer_zip_code_prefix = Column(Integer)
    customer_city = Column(String(100))
    customer_state = Column(String(10))
