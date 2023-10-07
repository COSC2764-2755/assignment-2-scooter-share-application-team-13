import sqlite3 as lite
import csv
import pandas as pd
from records import *
from db_utils import hash_password, verify_password


class DatabaseConnector:
    def __init__(self) -> None:
        self._file = 'ScootShare.db'

    def create_table(self) -> None:
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            # Temporary while db is local
            cur.execute("CREATE TABLE IF NOT EXISTS Customer (  \
                        username VARCHAR(50) PRIMARY KEY,   \
                        first_name VARCHAR(255),            \
                        last_name VARCHAR(255),             \
                        phone_number VARCHAR(20),           \
                        email_address VARCHAR(255),         \
                        password VARCHAR(255),              \
                        balance DECIMAL(10, 2));"
                        )
            con.commit()

    def create_staff_table(self) -> None:
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS Staff")
            cur.execute("CREATE TABLE IF NOT EXISTS Staff (            \
                        username VARCHAR(50),       \
                        password VARCHAR(255));"
                        )
            con.commit()

    def add_customer(self, new_customer: Customer) -> None:
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "INSERT INTO Customer (username, first_name, last_name, \
                    phone_number, email_address, password, balance) VALUES (?, ?, ?, ?, ?, ?, ?)"
            customer_data = (new_customer.username,  # username is primary key
                             new_customer.first_name,
                             new_customer.last_name,
                             new_customer.phone_number,
                             new_customer.email_address,
                             hash_password(new_customer.password),
                             new_customer.balance)
            cur.execute(query, customer_data)
            con.commit()

    def get_customer(self, username: str, password: str) -> Customer:
        # connect to db
        con = lite.connect(self._file)

        try:
            with con:
                cur = con.cursor()
                # get customer record by username
                query = "SELECT * FROM Customer WHERE username = ?;"
                print("Querying database for username:", username)
                cur.execute(query, (username,))
                result = cur.fetchone()
                if result is None:
                    # Handle the case where the user is not found
                    return None

                # Check if the password matches
                # Get stored password from db result
                stored_password = result[5]
                if not verify_password(stored_password, password):
                    # Password does not match
                    return None

                # create customer object from db
                customer = Customer(
                    result[0], result[1], result[2], result[3], result[4], result[5], result[6])
                # return customer object
                return customer

        except lite.Error as e:
            # Handle any database-related errors here
            print("Database error:", str(e))
            return None

    def add_staff(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            with open('staff_login.csv', 'r') as fin:
                reader = csv.reader(fin)
                next(csv.reader(fin), None)
                for entry in reader:
                    try:
                        record = (entry[0], hash_password(entry[1]))
                        query = "INSERT INTO Staff (username, password) VALUES (?, ?)"
                        cur.execute(query, record)
                        con.commit()
                    except csv.Error as e:
                        print(f'Line:{reader.line_num}, Record:{record}')

    def get_staff(self, username: str, password: str):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Staff WHERE username = ?;"
            cur.execute(query, (username,))
            result = cur.fetchone()
            if result is None:
                return None
            stored_password_hash = result[1]
            if not verify_password(stored_password_hash, password):
                return None

            # Create a Staff object and return it
            # Adjust this line to match your Staff class constructor
            staff = Staff(username, password)
            return staff

    def get_customer_by_id(self, customer_id):
        """
        Get a customer by their ID.

        Args:
            customer_id (int): The ID of the customer to retrieve.

        Returns:
            Customer or None: A Customer object if found, or None if not found.
        """
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Customer WHERE id = ?"
            cur.execute(query, (customer_id,))
            result = cur.fetchone()

            if result:
                id, first_name, last_name, phone_number, email_address, password, balance = result
                return Customer(id, first_name, last_name, phone_number, email_address, password, balance)
            else:
                return None

# Should we add docstrings to our methods? #This may not be needed if i can do it all in the update_customer_prfile method
    def update_balance(self, customer_id, updated_balance):
        """
        Update the balance for a customer.

        Args:
            customer_id (int): The ID of the customer to update.
            updated_balance (float): The new balance for the customer.
        """
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "UPDATE Customer SET balance = ? WHERE id = ?"
            cur.execute(query, (updated_balance, customer_id))
            con.commit()

# Takes in a dic of changes and a customerID to make the changes to
    def update_customer_profile(self, customer_id, changes):
        """
        Update a customer's profile in the database with the provided changes.

        Args:
            customer_id (int): The ID of the customer to update.
            changes (dict): A dictionary of changes to apply to the customer's profile.
        """
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()

            # Create SQL query to update the customer's profile, #changes is a dictionary, get all keys amd get all values for each key then seperate by a comma
            set_values = ', '.join([f"{key} = ?" for key in changes.keys()])
            query = f"UPDATE Customer SET {set_values} WHERE id = ?"
            # Lets say a dic was put in changes = {  "first_name": "NewFirstName",    "last_name": "NewLastName",  "email_address": "newemail@example.com"
            # The query would end up like this #UPDATE Customer SET first_name = ?, last_name = ?, email_address = ? WHERE id = ?

            # Add values to update and the customer# Values will "contain id = newid, last_name = newlastname, email_address = newemail@example.com"
            values = list(changes.values())
            # append to last to match up with the WHERE id = ?" being last
            values.append(customer_id)

            # At the moment under a try catch but may just take out
            try:
                # Execute the update query with parameters
                cur.execute(query, tuple(values))
                con.commit()
                # return True  # Update successful
            except lite.Error as thrown_E:
                print(f"Error updating customer profile: {thrown_E}")
                # return False  # Update failed

    def get_all_customers(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Customer"
            cur.execute(query)
            results = cur.fetchall()

            customers = []
            for result in results:
                customer_id, f_name, l_name, ph_num, email, password, balance = result
                customer = Customer(customer_id, f_name,
                                    l_name, ph_num, email, password, balance)
                customers.append(customer)

            return customers


# Scooter related database interactions - Bookings, repairs and reports # check if we need to make an individual histroy table

# Discuss if we will merge all the create table methods
# Also this seems to be incrementing incorrectly

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

    # This is auto incrementing correctly, though each run of the program is added a new instance to the db

    def create_booking_table(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS Booking")
            cur.execute("CREATE TABLE IF NOT EXISTS Booking (      \
                        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,                              \
                        location VARCHAR(255),               \
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
                        time_of_repair DATETIME);")

            con.commit()

     # Scooteer related methods

# Simply adds a new scooter instance to the database, #Does not need to include the ID as that is auto incremented in the database

    def add_scoooter(self, new_scooter: Scooter):
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

    def update_scooter_data(self, scooter_id, changes):
        """
        Update a scooter's data in the database with the provided changes.

        Args:
            scooter_id (int): The ID of the scooter to update.
            changes (dict): A dictionary of changes to apply to the scooter's profile. Made up of the attribute to change and the new data itself
        """
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()

            # Create SQL query to update the scooter's profile
            set_values = ', '.join([f"{key} = ?" for key in changes.keys()])
            query = f"UPDATE Scooter SET {set_values} WHERE id = ?"

            # Add values to update and the scooter ID
            values = list(changes.values())
            values.append(scooter_id)

            try:
                # Execute the update query with parameters
                cur.execute(query, tuple(values))
                con.commit()
                # return True  # Update successful
            except lite.Error as thrown_E:
                print(f"Error updating scooter profile: {thrown_E}")
                # return False  # Update failed


# Takes in an id and updates the status of that scooter

    def change_scooter_status(self, scooter_id, new_status):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "UPDATE Scooter SET status = ? WHERE id = ?"
            cur.execute(query, (new_status, scooter_id))
            con.commit()


# Get a specfic scooter by ID

    def get_scooter_by_id(self, scooter_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Scooter WHERE scooter_id = ?"
            cur.execute(query, (scooter_id,))
            row = cur.fetchone()

            if row:
                # Map the retrieved data to a Scooter object, id, status, make, color , location, power, cost
                scooter = Scooter(row[0], row[1], row[2],
                                  row[3], row[4], row[5], row[6])
                return scooter
            else:
                return None

# Gets all scooters in the db
    def get_scooters_from_db(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT status, make, color, location, power, cost, scooter_id FROM Scooter;"
            cur.execute(query)
            scooters_data = cur.fetchall()

        scooters = [Scooter(*row) for row in scooters_data]

        return scooters


# Booking related methods
# Takes in a single id and retrives the booking, tho assumes the id is unique

    def get_booking_by_id(self, booking_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Booking WHERE id = ?"
            cur.execute(query, (booking_id))
            row = cur.fetchone()
            # Double check that this maps out correctly when getting the db data in an instance
            if row:
                Booking = Booking(row[0], row[1], row[2],
                                  row[3], row[4], row[5], row[6], row[7])
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
                booking = Booking(booking_location, scooter_id, customer_id,
                                  start_time, duration, cost, status, booking_id)
                print(booking)
                bookings.append(booking)

            return bookings


# Takes in a customerID and gets all bookings attached to that customer

    def get_bookings_by_customer_id(self, customer_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Booking WHERE customer_id = ?"
            cur.execute(query, (customer_id,))
            booking_data = cur.fetchall()

        bookings = [Booking(*row) for row in booking_data]
        return bookings

    # Takes in a scooterID and gets all bookings for that scooter

    def get_bookings_by_scooter_id(self, scooter_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM Booking WHERE scooter_id = ?"
            cur.execute(query, (scooter_id,))
            booking_data = cur.fetchall()

        bookings = [Booking(*row) for row in booking_data]
        return bookings


# Takes in a booking instance and sends it to the database, id is left out as it is assinged in the db


    def add_booking(self, new_booking: Booking):
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

    def get_all_repairs(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT scooter_id, description, linked_report_id, time_of_repair, repair_id FROM Repair"

            cur.execute(query)
            results = cur.fetchall()

            repairs = []
            for result in results:
                scooter_id, description, linked_report_id, time_of_repair, repair_id = result
                repair = Repair(scooter_id, description,
                                linked_report_id, time_of_repair, repair_id)
                print('--------------ALL REPAIRS-------')
                print(repair.__str__())
                repairs.append(repair)

            return repairs

    def add_repair(self, new_repair: Repair):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "INSERT INTO Repair (scooter_id, description, linked_report_id, time_of_repair) VALUES (?, ?, ?, ?)"
            repair_data = (new_repair.scooter_id, new_repair.description,
                           new_repair.linked_report_id, new_repair.time_of_repair)
            cur.execute(query, repair_data)
            con.commit()


# Report methods

    def add_report(self, new_report: Report):
        print(new_report.__str__())
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "INSERT INTO Report (scooter_id, description, time_of_report, status) VALUES (?, ?, ?, ?)"
            report_data = (new_report.scooter_id, new_report.description,
                           new_report.time_of_report, new_report.status)
            cur.execute(query, report_data)
            con.commit()


# returns a report based on a reportID

    def get_report(self, report_id):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "SELECT scooter_id, description, time_of_report, status, report_id FROM Report WHERE id = ?"
            cur.execute(query, (report_id,))
            result = cur.fetchone()
            if result:
                scooter_id, description, time_of_report, status, report_id = result
               # return Report(report_id, scooter_id, description, time_of_report, status)
                # Spent ages trying to figure this out, was assinging the values incorrectly
                return Report(scooter_id, description, time_of_report, status, report_id)
            else:
                return None

    def set_report_status(self, report_id, new_status):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "UPDATE Report SET status = ? WHERE report_id = ?"
            cur.execute(query, (new_status, report_id))
            con.commit()

    def change_report_status(self, report_id, new_status):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            query = "UPDATE Report SET status = ? WHERE id = ?"
            cur.execute(query, (new_status, report_id))
            con.commit()

    def get_all_reports(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            # query = "SELECT * FROM Report" #This does not gureentee order
            query = "SELECT scooter_id, description, time_of_report, status, report_id FROM Report"
            cur.execute(query)
            results = cur.fetchall()

            reports = []
            for result in results:
                scooter_id, description, time_of_report, status, report_id = result
                report = Report(scooter_id, description,
                                time_of_report, status, report_id)
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

    # Double check where the we are getting username and password from

    def populate_staff(self):
        con = lite.connect(self._file)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM Staff")
            count = cur.fetchone()[0]
            if count == 0:
                query = "INSERT INTO Staff (username, password) VALUES (?, ?)"
                staff_data = [
                    ('~admin', hash_password('admin')),
                    ('_engineer', hash_password('engineer'))
                ]
                cur.executemany(query, staff_data)
                con.commit()

    def get_engineer(self, username: str, password: str) -> Engineer:
        try:
            con = lite.connect(self._file)
            with con:
                cur = con.cursor()
                # get engineer record by username
                query = "SELECT * FROM Engineer WHERE username = ?;"
                print("Querying database for username:", username)
                cur.execute(query, (username,))
                result = cur.fetchone()
                if result is None:
                    # Handle the case where the user is not found
                    return None

                # Check if the password matches
                # Get stored password from db result
                stored_password = result[1]
                if not verify_password(stored_password, password):
                    # Password does not match
                    return None

                # create engineer object from db
                engineer = Engineer(
                    result[0], result[1])
                # return customer object
                return engineer
        except lite.Error as e:
            # Handle any database-related errors here
            print("Database error:", str(e))
            return None
