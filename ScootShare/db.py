import sqlite3 as lite
from records import *
from db_utils import hash_password

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
                             hash_password(new_customer.password),
                             new_customer.balance)
            cur.execute(query, customer_data)
            con.commit()



#Scooter related database interactions 

#Scooter table with auto incrmenting to assign ID (other ways could be used). Also decide how to handle the histroy which incapsualtes bookings,
#reports and reapires for a single scooter
    def create_scooter_table(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS Scooter")
            cur.execute("CREATE TABLE Scooter (      \
                        id INT PRIMARY KEY AUTOINCREMENT,         \
                        status VARCHAR(255),          \
                        make VARCHAR(255),          \
                        color VARCHAR(255),         \
                        location VARCHAR(255),      \
                        power DECIMAL(10, 2),       \
                        cost DECIMAL(10, 2));")
            con.commit()

#Simply adds a new scooter instance to the database, #Does not need to include the ID as that is auto incremented in the database 
    def add_scoooter(self, new_scooter:Scooter):
         con = lite.connect(self._file)
         with con: 
            cur = con.cursor() 
            query = "INSERT INTO Scooter (status, make, color, location, power, cost) VALUES (?, ?, ?, ?, ?, ?)"
            scooter_data = (
                            new_scooter.status,
                            new_scooter.make,
                            new_scooter.color,
                            new_scooter.location,
                            new_scooter.power,
                            new_scooter.cost)
            cur.execute(query, scooter_data)
            con.commit()

    
#Decide if we want to pass in an already updated scooter object and pull the values from that, or if we just pass in the needed info being the 
# new status and the scooter to update it on (how its intended to work now)
    def change_scooter_status(self, scooter_id, new_status):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "UPDATE Scooter SET status = ? WHERE id = ?"
            cur.execute(query, (new_status, scooter_id))
            con.commit()


#Pass in an id and get a scooter instance, 
    def get_scooter_by_id(self, scooter_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Scooter WHERE id = ?"
            cur.execute(query, (scooter_id,))
            row = cur.fetchone()

            if row:
                # Map the retrieved data to a Scooter object, id, status, make, color , location, power, cost
                scooter = Scooter(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                return scooter
            else:
                return None



