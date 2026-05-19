from sqlalchemy import Column, String, Integer, Float
from ..core.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(50), primary_key=True)
    product_category_name = Column(String(100))
    product_name_length = Column(Integer)
    product_description_length = Column(Integer)
    product_photos_qty = Column(Integer)
    product_weight_g = Column(Float)
    product_length_cm = Column(Float)
    product_height_cm = Column(Float)
    product_width_cm = Column(Float)
