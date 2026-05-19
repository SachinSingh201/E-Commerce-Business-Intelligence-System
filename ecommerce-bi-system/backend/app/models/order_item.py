from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from ..core.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(String(50), ForeignKey("orders.order_id"), primary_key=True)
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String(50), ForeignKey("products.product_id"))
    seller_id = Column(String(50))
    shipping_limit_date = Column(DateTime)
    price = Column(Float)
    freight_value = Column(Float)
