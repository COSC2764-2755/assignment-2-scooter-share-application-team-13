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

#Discuss if we will merge all the create table methods 
#Also this seems to be incrementing incorrectly
    def create_scooter_table(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS Scooter")
            cur.execute("CREATE TABLE IF NOT EXISTS Scooter (      \
                        scooter_id INTEGER PRIMARY KEY AUTOINCREMENT,         \
                        status VARCHAR(255),          \
                        make VARCHAR(255),          \
                        color VARCHAR(255),         \
                        location VARCHAR(255),      \
                        power DECIMAL(10, 2),       \
                        cost DECIMAL(10, 2));")
            con.commit()



    #This is auto incrementing correctly, though each run of the program is added a new instance to the db
    def create_booking_table(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS Booking")
            cur.execute("CREATE TABLE IF NOT EXISTS Booking (      \
                        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,                              \
                        booking_location VARCHAR(255),               \
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
                        report_id INTEGER PRIMARY KEY AUTOINCREMENT,  \
                        scooter_id INT,                             \
                        description TEXT,                          \
                        time_of_report DATETIME,                    \
                        status VARCHAR(255));")
            con.commit()

    def create_repair_table(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Repair (      \
                        repair_id INTEGER PRIMARY KEY AUTOINCREMENT,  \
                        scooter_id INT,                             \
                        description TEXT,                          \
                        linked_report_id INT,                      \
                        time_of_repair DATETIME,    \
                        status VARCHAR(255));")
            
            con.commit()



     #Scooteer related methods      

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

    
#Takes in an id and updates the status of that scooter 
    def change_scooter_status(self, scooter_id, new_status):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "UPDATE Scooter SET status = ? WHERE id = ?"
            cur.execute(query, (new_status, scooter_id))
            con.commit()


#Get a specfic scooter by ID 
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
            
#Gets all scooters in the db
    def get_scooters_from_db(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT status, make, color, location, power, cost, scooter_id FROM Scooter;"
            cur.execute(query)
            scooters_data = cur.fetchall()

        scooters = [Scooter(*row) for row in scooters_data]

        return scooters
            



#Booking related methods
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


    # Returns all bookings ever made
    def get_all_bookings_orignal(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT booking_location, scooter_id, customer_id, start_time, duration, cost, status, booking_id FROM Booking"
            cur.execute(query)
            booking_data = cur.fetchall()
            print("------------Showing all existing bookings-----------")
            for row in booking_data:
                booking = Booking(*row)
                print("Location:", booking.location)
                print("Booking ID:", booking.booking_id)
                print("Scooter ID:", booking.scooter_id)
                print("Customer ID:", booking.customer_id)
                print("Start Time:", booking.start_time)
                print("Duration:", booking.duration)
                print("Cost:", booking.cost)
                print("Status:", booking.status)
                print("-----------")

        bookings = [Booking(*row) for row in booking_data]
        return bookings

    

    def get_all_bookings(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Booking"
            cur.execute(query)
            results = cur.fetchall()
            
            bookings = []
            for result in results:
                booking_location, scooter_id, customer_id, start_time, duration, cost, status, booking_id = result
                booking = Booking(booking_location, scooter_id, customer_id, start_time, duration, cost, status, booking_id)
                print(booking)
                bookings.append(booking)

            return bookings




#Takes in a customerID and gets all bookings attached to that customer
    def get_bookings_by_customer_id(self, customer_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Booking WHERE customer_id = ?"
            cur.execute(query, (customer_id,))
            booking_data = cur.fetchall()

        bookings = [Booking(*row) for row in booking_data]
        return bookings
    

    #Takes in a scooterID and gets all bookings for that scooter
    def get_bookings_by_scooter_id(self, scooter_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Booking WHERE scooter_id = ?"
            cur.execute(query, (scooter_id,))
            booking_data = cur.fetchall()

        bookings = [Booking(*row) for row in booking_data]
        return bookings


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

    def set_booking_status(self, new_status, booking_id):
            con = lite.connect(self._file)
            with con:
                cur = con.cursor()
                query = "UPDATE Booking SET status = ? WHERE booking_id = ?"
                cur.execute(query, (new_status, booking_id))
                con.commit()



# Repair methods

    def get_repairs_by_scooter_id(self, scooter_id):
            con = lite.connect(self._file)
            with con:
                cur = con.cursor()
                query = "SELECT * FROM Repair WHERE scooter_id = ?"
                cur.execute(query, (scooter_id,))
                repair_data = cur.fetchall()

            repairs = [Repair(*row) for row in repair_data]
            return repairs


    def add_repair(self, new_repair: Repair):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "INSERT INTO Repair (scooter_id, description, linked_report_id, time_of_repair) VALUES (?, ?, ?, ?)"
            repair_data = (new_repair.scooter_id, new_repair.description, new_repair.linked_report_id, new_repair.time_of_repair)
            cur.execute(query, repair_data)
            con.commit()





#Report methods
    def add_report(self, new_report: Report):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "INSERT INTO Report (scooter_id, description, time_of_report, status) VALUES (?, ?, ?, ?)"
            report_data = (new_report.scooter_id, new_report.description, new_report.time_of_report, new_report.status)
            cur.execute(query, report_data)
            con.commit()

    def set_report_status(self, report_id, new_status):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "UPDATE Report SET status = ? WHERE id = ?"
            cur.execute(query, (new_status, report_id))
            con.commit()


#returns a report based on a reportID
    def get_report(self, report_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Report WHERE id = ?"
            cur.execute(query, (report_id,))
            result = cur.fetchone()
            if result:
                report_id, scooter_id, description, time_of_report, status = result
                return Report(report_id, scooter_id, description, time_of_report, status)
            else:
                return None

    def get_all_reports(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Report"
            cur.execute(query)
            results = cur.fetchall()
            
            reports = []
            for result in results:
                report_id, scooter_id, description, time_of_report, status = result
                report = Report(report_id, scooter_id, description, time_of_report, status)
                reports.append(report)

            return reports


    def get_reports_by_scooter_id(self, scooter_id):
                con = lite.connect(self._file)
                with con:
                    cur = con.cursor()
                    query = "SELECT * FROM Report WHERE scooter_id = ?"
                    cur.execute(query, (scooter_id,))
                    report_data = cur.fetchall()

                reports = [Report(*row) for row in report_data]
                return reports

