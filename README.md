# E-Commerce Business Intelligence System

## Setup Instructions

1.  **Database Setup:**
    Ensure you have PostgreSQL running and a database created.
    The default credentials used are:
    - User: `your_username`
    - Password: `your_password`
    - Host: `localhost`
    - Port: `5432`
    - Database: `your_db_name`

2.  **Run ETL:**
    Populate the database with the Olist dataset:
    ```bash
    python backend/app/etl.py
    ```

3.  **Run Backend (FastAPI):**
    ```bash
    uvicorn backend.app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

4.  **Run Frontend (Flask):**
    ```bash
    python frontend/app.py
    ```
    The Dashboard will be available at `http://localhost:5000`.

## Features
- **Dashboard:** High-level KPIs and sales trends.
- **Customer Segmentation:** RFM analysis using KMeans clustering.
- **Revenue Forecasting:** 30-day forecast using Facebook Prophet.
