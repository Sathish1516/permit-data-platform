import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",  
        database="permits_db",
        user="postgres",
        password="postgres",
        port="5432"
    )