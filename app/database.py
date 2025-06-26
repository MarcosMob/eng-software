import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="supermercado_db",
        user="postgres",
        password="12345678"
    )
    return conn


