from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.order import Order
from ..models.payment import Payment
from ..models.customer import Customer

class KPIService:
    @staticmethod
    def get_total_revenue(db: Session):
        return db.query(func.sum(Payment.payment_value)).scalar() or 0.0

    @staticmethod
    def get_total_orders(db: Session):
        return db.query(func.count(Order.order_id)).scalar() or 0

    @staticmethod
    def get_total_customers(db: Session):
        return db.query(func.count(Customer.customer_id)).scalar() or 0

    @staticmethod
    def get_avg_order_value(db: Session):
        revenue = KPIService.get_total_revenue(db)
        orders = KPIService.get_total_orders(db)
        return revenue / orders if orders > 0 else 0.0

    @staticmethod
    def get_kpi_summary(db: Session):
        return {
            "total_revenue": KPIService.get_total_revenue(db),
            "total_orders": KPIService.get_total_orders(db),
            "total_customers": KPIService.get_total_customers(db),
            "avg_order_value": KPIService.get_avg_order_value(db)
        }
