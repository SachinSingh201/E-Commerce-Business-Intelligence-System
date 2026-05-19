import pandas as pd
from prophet import Prophet
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.order import Order
from ..models.payment import Payment

class ForecastService:
    @staticmethod
    def forecast_sales(db: Session, periods: int = 30):
        # Fetch daily sales data
        sales_data = db.query(
            func.date(Order.order_purchase_timestamp).label('ds'),
            func.sum(Payment.payment_value).label('y')
        ).join(Payment, Order.order_id == Payment.order_id) \
         .group_by(func.date(Order.order_purchase_timestamp)) \
         .order_by(func.date(Order.order_purchase_timestamp)) \
         .all()
        
        if not sales_data:
            return []

        df = pd.DataFrame(sales_data, columns=['ds', 'y'])
        df['ds'] = pd.to_datetime(df['ds'])
        
        # Initialize and fit Prophet model
        model = Prophet()
        model.fit(df)
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        # Return relevant columns
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods + 30)
        return result.to_dict(orient='records')
