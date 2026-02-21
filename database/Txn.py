import mysql.connector
from mysql.connector import Error

def setup_database()
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='',
        database='petty_cash_db'
    )

    if connection.is_connected():
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
        tx_id INT AUTO_INCREMENT PRIMARY KEY,
        fund_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        description VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""

        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'transactions' created successfully")
        cursor.close()

        insert_query = "INSERT INTO transactions (fund_id, amount, description) VALUES (%s, %s, %s)"
        data = (1, 25.50, 'Office Stationery')

        cursor.execute(insert_query, data)
        connection.commit()
        print(f"Recorded transaction. ID: {cursor.lastrowid}")

    else :
        print("Connection failed")





