import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="doubt_machine",
        user="yusuff",
        password="yusuff"
    )