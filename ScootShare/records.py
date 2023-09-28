# Store classes

class Customer():
    def __init__(self, id, f_name, l_name, ph_num, email, username, password, balance) -> None:
        self.customer_id = id
        self.first_name = f_name
        self.last_name = l_name
        self.phone_number = ph_num
        self.email_address = email
        self.username = username
        self.password = password
        self.balance = balance


class Scooter():
    def __init__(self, status, make, color, location, power, cost,id=None) -> None:
        self.scooter_id = id
        self.status = status
        self.make = make
        self.color = color
        self.location = location
        self.power = power
        self.cost = cost


class History():
    def __init__(self, id, scooter_id) -> None:
        self.id = id
        self.scooter_id = scooter_id
        self.bookings = []  
        self.reports = []
        self.repairs = []  

class Booking():
    def __init__(self, location, booking_id, scooter_id, customer_id, start_time, duration, cost, status) -> None:
        self.location = location
        self.booking_id = booking_id
        self.scooter_id = scooter_id
        self.customer_id = customer_id
        self.start_time = start_time
        self.duration = duration
        self.cost = cost
        self.status = status


class Report():
    def __init__(self, report_id, scooter_id, description, time_of_report, status) -> None:
        self.scooter_id = scooter_id
        self.id = report_id
        self.description = description
        self.time_of_report = time_of_report
        self.status = status
       

class Repair():
    def __init__(self, repair_id, scooter_id, description, linked_report_id, time_of_repair) -> None:
        self.scooter_id =scooter_id
        self.repair_id = repair_id
        self.description = description
        self.linked_report_id = linked_report_id
        self.time_of_repair = time_of_repair


