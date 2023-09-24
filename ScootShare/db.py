import sqlite3 as lite
from records import Customer
from db_utils import hash_password

class DatabaseConnector:
    def __init__(self) -> None:
        self._file = '.\ScootShare\ScootShare.db'

    def create_table(self) -> None:
        con = lite.connect(self._file)
        with con: 
            cur = con.cursor() 
            cur.execute("DROP TABLE IF EXISTS Customer") # Temporary while db is local
            cur.execute("CREATE TABLE Customer (            \
                        username VARCHAR(50) PRIMARY KEY,   \
                        first_name VARCHAR(255),            \
                        last_name VARCHAR(255),             \
                        phone_number VARCHAR(20),           \
                        email_address VARCHAR(255),         \
                        password VARCHAR(255),              \
                        balance DECIMAL(10, 2));"
                        )
            con.commit()
    
    def add_customer(self, new_customer:Customer) -> None:
        con = lite.connect(self._file)
        with con: 
            cur = con.cursor() 
            query = "INSERT INTO Customer (username, first_name, last_name, phone_number, email_address, password, balance) VALUES (?, ?, ?, ?, ?, ?, ?)"
            customer_data = (new_customer.username, # username is primary key
                             new_customer.first_name,
                             new_customer.last_name,
                             new_customer.phone_number,
                             new_customer.email_address,
                             hash_password(new_customer.password),
                             new_customer.balance)
            cur.execute(query, customer_data)
            con.commit()