from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.order import Order
from ..models.payment import Payment

class SalesService:
    @staticmethod
    def get_monthly_sales(db: Session):
        # Using PostgreSQL date_trunc for monthly aggregation
        sales = db.query(
            func.date_trunc('month', Order.order_purchase_timestamp).label('month'),
            func.sum(Payment.payment_value).label('revenue')
        ).join(Payment, Order.order_id == Payment.order_id) \
         .group_by('month') \
         .order_by('month') \
         .all()
        
        return [{"month": s.month.strftime('%Y-%m'), "revenue": s.revenue} for s in sales]

    @staticmethod
    def get_sales_by_category(db: Session):
        from ..models.product import Product
        from ..models.order_item import OrderItem
        
        sales = db.query(
            Product.product_category_name,
            func.sum(OrderItem.price).label('revenue')
        ).join(OrderItem, Product.product_id == OrderItem.product_id) \
         .group_by(Product.product_category_name) \
         .order_by(func.sum(OrderItem.price).desc()) \
         .limit(10) \
         .all()
        
        return [{"category": s.product_category_name, "revenue": s.revenue} for s in sales]
