from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SalesSummary(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    avg_order_value: float

class MonthlySales(BaseModel):
    month: str
    revenue: float

class CategorySales(BaseModel):
    category: str
    revenue: float
