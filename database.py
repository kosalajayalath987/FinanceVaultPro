import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="petty_cash_mgt"
    )

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    query = "CREATE DATABASE IF NOT EXISTS petty_cash_mgt"

    conn.commit()
    cursor.close()
    conn.close()