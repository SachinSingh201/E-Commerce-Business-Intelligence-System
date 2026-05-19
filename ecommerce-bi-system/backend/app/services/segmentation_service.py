import pandas as pd
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..models.order import Order
from ..models.payment import Payment
from ..models.customer import Customer

class SegmentationService:
    @staticmethod
    def perform_rfm_segmentation(db: Session, n_clusters: int = 4):
        # ... (keep existing code)
        query = db.query(
            Customer.customer_unique_id,
            func.max(Order.order_purchase_timestamp).label('last_purchase'),
            func.count(Order.order_id).label('frequency'),
            func.sum(Payment.payment_value).label('monetary')
        ).join(Order, Customer.customer_id == Order.customer_id) \
         .join(Payment, Order.order_id == Payment.order_id) \
         .group_by(Customer.customer_unique_id)
        
        data = pd.DataFrame(query.all(), columns=['customer_id', 'last_purchase', 'frequency', 'monetary'])
        
        if data.empty:
            return []

        latest_date = data['last_purchase'].max()
        data['recency'] = (latest_date - data['last_purchase']).dt.days
        
        rfm_features = data[['recency', 'frequency', 'monetary']]
        
        import numpy as np
        rfm_log = np.log1p(rfm_features)
        
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm_log)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        data['cluster'] = kmeans.fit_predict(rfm_scaled)
        
        return data.sample(100).to_dict(orient='records')

    @staticmethod
    def get_latest_customers(db: Session, limit: int = 100):
        # Fetch latest customers based on order purchase timestamp
        query = db.query(
            Customer.customer_id,
            Order.order_purchase_timestamp,
            func.sum(Payment.payment_value).label('monetary')
        ).join(Order, Customer.customer_id == Order.customer_id) \
         .join(Payment, Order.order_id == Payment.order_id) \
         .group_by(Customer.customer_id, Order.order_purchase_timestamp) \
         .order_by(desc(Order.order_purchase_timestamp)) \
         .limit(limit)
        
        results = query.all()
        return [{"customer_id": r.customer_id, "order_time": r.order_purchase_timestamp.strftime('%Y-%m-%d %H:%M:%S'), "monetary": r.monetary} for r in results]
