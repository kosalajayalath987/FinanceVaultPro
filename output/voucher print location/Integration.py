import mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="petty_cash_mgt"
)

try:
    def get_user_balances():
    query = """
    SELECT u.username, f.fund_name, f.balance
    FROM users u
    JOIN funds f ON u.user_id = f.user_id
    """
    cursor.execute(query)
    return cursor.fetchall()
    print(get_user_balances())


    def add_transaction(fund_id, amount, description):
    sql_tx = "INSERT INTO transactions (fund_id, amount, description) VALUES (%s, %s, %s)"
    cursor.execute(sql_tx, (fund_id, amount, description))

    sql_update = "UPDATE funds SET balance = balance - %s WHERE fund_id = %s"
    cursor.execute(sql_update, (amount, fund_id))

    connection.commit()
    print("Transaction recorded successfully!")
    print(get_user_balances())

except mysql.connector.Error as err:
    print(err)

connection.rollback()
