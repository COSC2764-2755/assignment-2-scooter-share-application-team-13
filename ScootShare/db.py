import sqlite3 as lite
from records import Customer
class DatabaseConnector:
    def __init__(self) -> None:
        self._file = '.\ScootShare\ScootShare.db'

    def create_table(self):
        con = lite.connect(self._file)
        with con: 
            cur = con.cursor() 
            cur.execute("DROP TABLE IF EXISTS Customer") # Temporary while db is local
            cur.execute("CREATE TABLE Customer (    \
                        id INT PRIMARY KEY,         \
                        first_name VARCHAR(255),    \
                        last_name VARCHAR(255),     \
                        phone_number VARCHAR(20),   \
                        email_address VARCHAR(255), \
                        username VARCHAR(50),       \
                        password VARCHAR(255),      \
                        balance DECIMAL(10, 2));"
                        )
            con.commit()
    
    def add_customer(self, new_customer:Customer):
        con = lite.connect(self._file)
        with con: 
            cur = con.cursor() 
            query = "INSERT INTO Customer (id, first_name, last_name, phone_number, email_address, username, password, balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            customer_data = (new_customer.customer_id,
                             new_customer.first_name,
                             new_customer.last_name,
                             new_customer.phone_number,
                             new_customer.email_address,
                             new_customer.username,
                             new_customer.password,
                             new_customer.balance)
            cur.execute(query, customer_data)
            con.commit()