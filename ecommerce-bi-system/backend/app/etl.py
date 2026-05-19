import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os

# Add the project root to sys.path to import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

def run_etl():
    print("Starting ETL Process...")
    
    try:
        # Load Data
        print("Loading CSV files...")
        customers = pd.read_csv('data/raw/olist_customers_dataset.csv')
        orders = pd.read_csv('data/raw/olist_orders_dataset.csv')
        products = pd.read_csv('data/raw/olist_products_dataset.csv')
        order_items = pd.read_csv('data/raw/olist_order_items_dataset.csv')
        payments = pd.read_csv('data/raw/olist_order_payments_dataset.csv')

        # Rename misspelled columns in products to match model
        products = products.rename(columns={
            'product_name_lenght': 'product_name_length',
            'product_description_lenght': 'product_description_length'
        })

        # Convert date columns to datetime
        print("Processing date columns...")
        date_cols = [
            'order_purchase_timestamp', 'order_approved_at', 
            'order_delivered_carrier_date', 'order_delivered_customer_date', 
            'order_estimated_delivery_date'
        ]
        for col in date_cols:
            if col in orders.columns:
                orders[col] = pd.to_datetime(orders[col])
        
        if 'shipping_limit_date' in order_items.columns:
            order_items['shipping_limit_date'] = pd.to_datetime(order_items['shipping_limit_date'])

        # Create tables if they don't exist
        print("Creating tables (if not exist)...")
        from app.models.customer import Customer
        from app.models.order import Order
        from app.models.product import Product
        from app.models.payment import Payment
        from app.models.order_item import OrderItem
        from app.core.database import Base
        Base.metadata.create_all(engine)

        # Clear existing data to avoid UniqueViolations
        print("Clearing existing data...")
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE payments, order_items, orders, products, customers CASCADE"))
            conn.commit()

        # Insert Data
        print("Inserting data into PostgreSQL...")
        customers.to_sql('customers', engine, if_exists='append', index=False)
        orders.to_sql('orders', engine, if_exists='append', index=False)
        products.to_sql('products', engine, if_exists='append', index=False)
        order_items.to_sql('order_items', engine, if_exists='append', index=False)
        payments.to_sql('payments', engine, if_exists='append', index=False)

        print("ETL COMPLETED SUCCESSFULLY")
    except Exception as e:
        print(f"ETL FAILED: {str(e)}")

if __name__ == "__main__":
    run_etl()
