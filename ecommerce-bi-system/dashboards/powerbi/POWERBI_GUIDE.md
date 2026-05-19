# Power BI Real-Time Integration Guide

This guide explains how to connect Power BI to your E-Commerce BI System database with real-time updates.

## 1. Prerequisites
- **Power BI Desktop** installed.
- **Npgsql** (PostgreSQL .NET provider) installed on your machine.
- Database credentials (from `backend/app/core/config.py`):
  - **Host:** `localhost`
  - **Port:** `5432`
  - **Database:** `your_db_name`
  - **User:** `your_username`
  - **Password:** `your_password`

## 2. Connect to Database
1. Open Power BI Desktop.
2. Go to **Get Data** -> **PostgreSQL database**.
3. Enter the **Server** (`localhost:5432`) and **Database** (`your_db_name`).
4. **CRITICAL:** Under **Data Connectivity mode**, select **DirectQuery**.
   - *Why?* DirectQuery does not import data; it queries the database every time a visual is refreshed, allowing for real-time updates.
5. Click **OK**.
6. Enter your database username and password when prompted.

## 3. Enable Real-Time (Auto-Refresh)
Power BI visuals don't refresh by themselves unless you tell them to.
1. Once your report is built, go to the **Format** pane (paint roller icon) on the right.
2. Select **Page refresh**.
3. Toggle it to **On**.
4. Set the **Refresh interval** to a low value (e.g., `5 Seconds`).
5. Power BI will now automatically re-run its queries against PostgreSQL every 5 seconds.

## 4. Recommended Visuals
- **Card:** Total Revenue (`SUM(payment_value)`).
- **Line Chart:** Sales Trend (Axis: `order_purchase_timestamp`, Values: `SUM(payment_value)`).
- **Pie Chart:** Category Distribution.
- **Map:** Geo Analytics using `customer_city` and `customer_state`.

## 5. Deployment Note
If you publish this report to the **Power BI Service (Cloud)**, you will need to install the **On-premises data gateway** on your local machine to allow the Power BI cloud service to talk to your local PostgreSQL database.
