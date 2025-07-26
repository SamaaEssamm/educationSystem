import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="complaint_app",
        user="postgres",
        password="1234"  # ← اكتبي الباسورد اللي ضبطيه
    )
