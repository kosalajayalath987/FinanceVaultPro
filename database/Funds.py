import mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="petty_cash_mgt"

)

cursor = connection.cursor()
query = """
INSERT INTO `funds` (`fund_id`, `user_id`, `fund_name`, `balance`)
VALUES (NULL, '1', 'Petty Cash - Main', 160000)
"""

cursor.execute(query)
connection.commit()
cursor.close()
connection.close()
