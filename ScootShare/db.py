import sqlite3 as lite

class DatabaseConnector:
    def __init__(self) -> None:
        self._file = 'ScootShare.db'

    def create_table():
        con = lite.connect()
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