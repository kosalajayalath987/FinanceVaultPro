import mysql.connector
import bcrypt

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="petty_cash_mgt"
)

cursor = connection.cursor()
def login_and_get_access(username, provided_password):


    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="pw", database="sys")
        cursor = conn.cursor(dictionary=True)

    query = "SELECT password_hash, role FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user_record = cursor.fetchone()

    if user_record:
        stored_hash = user_record['password_hash'].encode('utf-8')

        if bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash):
            return user_record['role']

        finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

            role = login_and_get_access("john", "secure_pass123")
            role = login_and_get_access("Max", "secure_pass123")
            role = login_and_get_access("Jane", "secure_pass123")
            role = login_and_get_access("Anne", "secure_pass123")
            role = login_and_get_access("Sam", "secure_pass123")

            if role == "Admin":
                print("Welcome, Admin. Accessing Financial Overviews...")

                elif role ="Custodian"
                print("Welcome, Custodian. Accessing Financial Overviews...")

            else:
                print("Access Denied: Invalid credentials.")



