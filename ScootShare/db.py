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



#Scooter related database interactions - Bookings, repairs and reports # check if we need to make an individual histroy table

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


    def create_booking_table(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Booking (      \
                        booking_id INT PRIMARY KEY AUTOINCREMENT, \                               \
                        scooter_id INT,                              \
                        customer_id INT,                             \
                        start_time DATETIME,                         \
                        duration DECIMAL(10, 2),                     \
                        cost DECIMAL(10, 2),                         \
                        status VARCHAR(255));")
            con.commit()


    def create_report_table(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Report (      \
                        report_id INT PRIMARY KEY AUTOINCREMENT,  \
                        time_of_report DATETIME,                    \
                        scooter_id INT,                             \
                        start_time DATETIME,                         \
                        status VARCHAR(255));")
            con.commit()


    def create_rapair_table(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Repair (      \
                        repair_id INT PRIMARY KEY AUTOINCREMENT,  \
                        time_of_repair DATETIME,                    \
                        scooter_id INT,                             \
                        start_time DATETIME,                         \
                        linked_report_id INT);")
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


#Takes in a single id and retrives the booking, tho assumes the id is unique 
    def get_booking_by_id(self, booking_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Booking WHERE id = ?"
            cur.execute(query, (booking_id))
            row = cur.fetchone()
                #Double check that this maps out correctly when getting the db data in an instance
            if row:
                Booking = Booking(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                return Booking
            else:
                return None

#Takes in a booking instance and sends it to the database, id is left out as it is assinged in the db
    def add_booking(self, new_booking:Booking):
        con = lite.connect(self._file)
        with con: 
            cur = con.cursor() 
            query = "INSERT INTO Booking (booking_location, scooter_id, customer_id, start_time, duration, cost, status) VALUES (?, ?, ?, ?, ?, ?, ?)"
            booking_data = (new_booking.location,
                            new_booking.scooter_id,
                            new_booking.customer_id, 
                            new_booking.start_time, 
                            new_booking.duration, 
                            new_booking.cost, 
                            new_booking.status)
            cur.execute(query, booking_data)
            con.commit()



