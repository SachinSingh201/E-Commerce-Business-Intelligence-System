import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="your_db_name",
    user="your_username",
    password="your_password"
)

print("Database Connected Successfully!")

conn.close()