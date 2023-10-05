# Flask main
from datetime import datetime, timedelta
from db import DatabaseConnector
from flask import Flask
from flask_restful import Api, Resource, reqparse
from records import *



app = Flask(__name__)
api = Api(app)
database_controller = DatabaseConnector() # TODO: Find somewhere better to initialise db
database_controller.create_table()
database_controller.create_booking_table()
database_controller.create_report_table()
database_controller.create_scooter_table()
database_controller.create_repair_table()

def parse_datetime(value: str):
        try:
            # Parse the input string as a datetime object # takes in something like this: "2023-10-05 14:30:00"
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")  # Adjust the format as needed
        # if you attempt to parse a string as a datetime, and the string does not match the expected format, this exception will be raised
        except Exception as thrown_exception: #bad practise to catch general exceptions but for the moment helps in debugging
            print(f"Error: {thrown_exception}")


class Registration(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._cust_put_args = reqparse.RequestParser()
        self._cust_put_args.add_argument("id", type=int, help="CustomerID")
        self._cust_put_args.add_argument("first_name", type=str, help="Customer fName")
        self._cust_put_args.add_argument("last_name", type=str, help="Customer lName")
        self._cust_put_args.add_argument("phone_number", type=str, help="phone num")
        self._cust_put_args.add_argument("email_address", type=str, help="email")
        self._cust_put_args.add_argument("username", type=str, help="username")
        self._cust_put_args.add_argument("password", type=str, help="password")
        self._cust_put_args.add_argument("balance", type=float, help="balance")

    def put(self):
        args = self._cust_put_args.parse_args()
        customer_object = Customer(args['id'], args['first_name'], 
                                   args['last_name'], args['phone_number'], 
                                   args['email_address'], args['username'], 
                                   args['password'], args['balance'])
        
        # check if we want to do the validation here to check if the customer id already exists, this is already done in the edit customer class so it would be easy to move accross
        database_controller.add_customer(customer_object)
        #Shows the unhashed pw
        return f"{customer_object.first_name} has the password {customer_object.password}"
    

class editCustomer(Resource):
    def __init__(self) -> None:
            super().__init__()
            self._cust_put_args = reqparse.RequestParser()

            self._cust_put_args.add_argument("current_id", type=int, help="CustomerID")

            #Pretty sure these need match the database names 
            self._cust_put_args.add_argument("id", type=int, help="New CustomerID")
            self._cust_put_args.add_argument("first_name", type=str, help="Customer fName")
            self._cust_put_args.add_argument("last_name", type=str, help="Customer lName")
            self._cust_put_args.add_argument("phone_number", type=str, help="phone num")
            self._cust_put_args.add_argument("email_address", type=str, help="email")
            self._cust_put_args.add_argument("username", type=str, help="username")
            self._cust_put_args.add_argument("password", type=str, help="password")
            self._cust_put_args.add_argument("balance", type=float, help="balance")

    def put(self):
        args = self._cust_put_args.parse_args()
        updated_customer_object = Customer(
            args['id'], args['first_name'], args['last_name'],
            args['phone_number'], args['email_address'],
            args['username'], args['password'], args['balance']
        )

        # Get the original information of this customer
        original_customer_data = database_controller.get_customer_by_id(args['current_id'])

         # Perform validation to see what changes were made to any of the attributes
         #add balance, 
        changes = {}
        if updated_customer_object.first_name != original_customer_data.first_name:
            changes['first_name'] = updated_customer_object.first_name
        if updated_customer_object.last_name != original_customer_data.last_name:
            changes['last_name'] = updated_customer_object.last_name
        if updated_customer_object.phone_number != original_customer_data.phone_number:
            changes['phone_number'] = updated_customer_object.phone_number
        if updated_customer_object.email_address != original_customer_data.email_address:
            changes['email_address'] = updated_customer_object.email_address
        if updated_customer_object.username != original_customer_data.username:
            # Check if the new username is available
            if database_controller.get_customer_by_id(updated_customer_object.username) is None:
                changes['id'] = updated_customer_object.username
            else:
                return "Username is already in use, please choose a different one." #, 400  # Return an error response, don't tink we need this, double check

        # Update the customer's profile based on the changes dictionary
        if changes:
            # Apply the changes to the customer profile in the database
            database_controller.update_customer_profile(args['current_id'], changes)
            return "You have successfully updated your profile." #, #200
        else:
            return f"(You have made no changes for this user: {original_customer_data.customer_id})"

class editScooter(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._scooter_put_args = reqparse.RequestParser()
        self._scooter_put_args.add_argument("scooter_id", type=str, help="Scooter id") # At minimum 

        #It may be better practise to get the scooter id and get the most recent data 
        self._scooter_put_args.add_argument("status", type=str, help="Scooter status")
        self._scooter_put_args.add_argument("make", type=str, help="Scooter make")
        self._scooter_put_args.add_argument("color", type=str, help="Scooter color")
        self._scooter_put_args.add_argument("location", type=str, help="Scooter location")
        self._scooter_put_args.add_argument("power", type=float, help="Power remaining")
        self._scooter_put_args.add_argument("cost", type=float, help="Cost per min")
        
    def put(self):
        args = self._scooter_put_args.parse_args()
        updated_scooter_object = Scooter(
            status=args['status'],
            make=args['make'],
            color=args['color'],
            location=args['location'],
            power=args['power'],
            cost=args['cost']
        )
        original_scooter_data = database_controller.get_scooter_by_id(args['scooter_id']) #check this is all good
        # Perform validation to see what changes were made to any of the attributes

        #Note that it is important that these match the tables of the database
        changes = {}
        if updated_scooter_object.status != original_scooter_data.status:
            changes['status'] = updated_scooter_object.status
        if updated_scooter_object.make != original_scooter_data.make:
            changes['make'] = updated_scooter_object.make
        if updated_scooter_object.color != original_scooter_data.color:
            changes['color'] = updated_scooter_object.color
        if updated_scooter_object.location != original_scooter_data.location:
            changes['location'] = updated_scooter_object.location
        if updated_scooter_object.power != original_scooter_data.power:
            changes['power'] = updated_scooter_object.power
        if updated_scooter_object.cost != original_scooter_data.cost:
            changes['cost'] = updated_scooter_object.cost

        # Update the scooter's profile based on the changes dictionary
        if changes:
            # Apply the changes to the scooter profile in the database
            database_controller.update_scooter_data(args['current_id'], changes)
            return "You have successfully updated the scooter profile." #, 200
        else:
            return "You have made no changes for this scooter."

                

class addScooter(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._scooter_put_args = reqparse.RequestParser()
        self._scooter_put_args.add_argument("status", type=str, help="Scooter status")
        self._scooter_put_args.add_argument("make", type=str, help="Scooter make")
        self._scooter_put_args.add_argument("color", type=str, help="Scooter color")
        self._scooter_put_args.add_argument("location", type=str, help="Scooter location")
        self._scooter_put_args.add_argument("power", type=float, help="Power remaining")
        self._scooter_put_args.add_argument("cost", type=float, help="Cost per min")

    def put(self):
        args = self._scooter_put_args.parse_args()
        scooter = Scooter(
            status=args['status'],
            make=args['make'],
            color=args['color'],
            location=args['location'],
            power=args['power'],
            cost=args['cost']
        )
        database_controller.add_scoooter(scooter)
        listOfScooters = database_controller.get_scooters_from_db()

        # Loop here to test 
        for scooter in listOfScooters:
            print("Status:", scooter.status)
            print("Make:", scooter.make)
            print("Color:", scooter.color)
            # ScooterID will alwaysd be one if the create tables method stays in this class
            print("Scooter ID:", scooter.scooter_id)
            print("-----------") 

        return f"You added a new scooter to the db colored {scooter.color} and with a charge of {scooter.power}"
       
  

  #No validation yet, this would come in the form of making sure an in progress booking cannot be cancled and a completed booking cannot be cancled 
  #Though a way to assit this before it gets to this point is to only allow the user to select bookings to cancle that are valid
class cancelBooking(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._booking_put_args = reqparse.RequestParser()
        #self._booking_put_args.add_argument("customer_id", type=int, help="Customer ID")
        self._booking_put_args.add_argument("booking_id", type=int, help="booking ID") #Double check but all we should need to cancle a booking is the id


    def put(self):
        args = self._booking_put_args.parse_args()
        booking_to_cancel_id = args['booking_id']
        database_controller.set_booking_status('canceled', booking_to_cancel_id) # Change the status to cancled 

        return f"You canceled a booking of id: {booking_to_cancel_id}"



class Make_Booking(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._booking_put_args = reqparse.RequestParser()
        #First interation 
        self._booking_put_args.add_argument("location", type=str, help="Booking location")
        self._booking_put_args.add_argument("scooter_id", type=int, help="Scooter ID")
        self._booking_put_args.add_argument("customer_id", type=int, help="Customer ID")
        #parse the time here so we can do operations to do with the starttime and checking if it conflicts with other bookings# assuming we get the data as a string 
        #We should recive a string like this, "2023-10-05 14:30:00". Double check that we we recive data from the api call it will be a
        self._booking_put_args.add_argument("start_time", type=parse_datetime, help="Start time")
        self._booking_put_args.add_argument("duration", type=int, help="Duration")
        self._booking_put_args.add_argument("cost", type=float, help="Booking cost per min")
        self._booking_put_args.add_argument("status", type=str, help="Booking status")



    def put(self):
        args = self._booking_put_args.parse_args()
        purposed_booking = Booking(
            location=args['location'],
            scooter_id=args['scooter_id'],
            customer_id=args['customer_id'],
            start_time=args['start_time'],
            duration=args['duration'],
            cost=args['cost'],
            status=args['status']
        )
       
        # Check if the user has enough balance in their account  #The amount is taken only when the booking is initiated
        booking_customer = database_controller.get_customer_by_id(args['customer_id'])
        booking_cost = args['duration'] * args['cost']
        if booking_customer.balance - booking_cost < 0:
            return "Insufficient funds to make the booking."#, 400  # Return an error response

        
        #Check if scooter is avalable
        scooter_to_book = database_controller.get_scooter_by_id(purposed_booking.scooter_id)

        if scooter_to_book.status != 'Avalable':
            return f"sorry, your choosen scooter is {scooter_to_book.status}"
    

       
        #Purposed booking time cannot conflicts with with booking times of other bookings, meaning the start and end time cannot overlap
        #Addionally a scooter can only be booked if it has the status avalable , it might be under repair or in use 

        bookings_for_scooter = database_controller.get_bookings_by_scooter_id(args['scooter_id'])

        for existing_booking in bookings_for_scooter:
            existing_start_time = existing_booking.start_time #This should be the correct type thanks to the parse datetime method
            existing_end_time = existing_start_time + timedelta(minutes=existing_booking.duration)

            purposed_start_time = purposed_booking.start_time
            purposed_end_time = purposed_start_time + timedelta(minutes=purposed_booking.duration)

            # Check if the proposed booking overlaps with any existing booking, # btw \ is a line continuater
            if (existing_start_time <= purposed_start_time < existing_end_time) or \
            (existing_start_time < purposed_end_time <= existing_end_time):
                return "Booking time conflicts with an existing booking."#, 400


        database_controller.add_booking(purposed_booking)        
        return f"You have made a booking for {purposed_booking.start_time} under the customer id: {purposed_booking.customer_id}"

# Double check if we want a made report to have any impact on scooter avalbility 
class Make_Report(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._report_put_args = reqparse.RequestParser()
        self._report_put_args.add_argument("scooter_id", type=str, help="Scooter ID")
        self._report_put_args.add_argument("description", type=str, help="Description of the repair")
        self._report_put_args.add_argument("linked_report_id", type=str, help="Linked report ID")
        self._report_put_args.add_argument("time_of_report", type=str, help="Time of report")
        self._report_put_args.add_argument("status", type=str, help="Report status")

    def put(self):
        args = self._report_put_args.parse_args()
        report = Report(
            scooter_id=args['scooter_id'],
            description=args['description'],
            time_of_report=args['time_of_report'],
            status=args['status']
        )
        database_controller.add_report(report)
        return f"You made a report for scooter: {report.scooter_id} to address: {report.description}"

        

class Make_Repair(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._repair_put_args = reqparse.RequestParser()
        self._repair_put_args.add_argument("scooter_id", type=str, help="Scooter ID")
        self._repair_put_args.add_argument("description", type=str, help="Description of the repair")
        self._repair_put_args.add_argument("linked_report_id", type=str, help="Linked report ID")
        self._repair_put_args.add_argument("time_of_repair", type=str, help="Time of repair")
        #Either get this passed in or set it here as 'unaddressed' since that is what it will always be 
        self._repair_put_args.add_argument("status", type=str, help="Repair status")

    def put(self):
        args = self._repair_put_args.parse_args()
        repair = Repair(
            scooter_id=args['scooter_id'],
            description=args['description'],
            linked_report_id=args['linked_report_id'],
            time_of_repair=args['time_of_repair']
        )
        print('repair')
        database_controller.add_repair(repair)
        database_controller.set_report_status(repair.linked_report_id, "addressed") # may not want this hardcoded here
        return f"You did a repair at: {repair.time_of_repair} to address: {repair.description}"

#This will be needed to top up the balance, though it is editing account details it is seperate from the editcustomer class
class Top_up_Balanace(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._customer_put_args = reqparse.RequestParser()
        self._customer_put_args.add_argument("customerid", type=str, help="CustomerID")
        self._customer_put_args.add_argument("top_up", type=str, help="Amount to add")

    def put(self):
        args = self._customer_put_args.parse_args()
        customer_id=args['customer_id']
        amount=args['top_up']
                
            # Validate customer_id and amount # decide if we want error messages here
        if not isinstance(amount, float) or amount <= 0:
            return "Invalid input. Please provide a valid customer ID and a positive amount."

        customer = database_controller.get_customer_by_id(customer_id)

        if customer is None:
            return f"Customer with ID {customer_id} not found."

        # Update the balance
        customer.balance += amount
        database_controller.update_balance(customer_id, customer.balance)

        return f"You topped up user {customer_id} with an amount of {amount}. New balance: {customer.balance}"




class GetCompleteHistroy(Resource):
     def __init__(self) -> None:
        super().__init__()


class GetAllRepairs(Resource):
    def __init__(self) -> None:
        super().__init__()

    def get(self):
         # Retrieve all repair instances from the database
        repairs = database_controller.get_all_repairs()
        print('-----------------------')
        for repair in repairs:
            print(repair.__str__())

        print('-----------------------')
        # Format the repairs data as needed
        formatted_repairs = [{"repair_id": repair.repair_id, "scooter_id": repair.scooter_id, "description": repair.description, "linked_report_id": repair.linked_report_id, "time_of_repair": repair.time_of_repair} for repair in repairs]
        return formatted_repairs


class GetAllReports(Resource):
    def __init__(self) -> None:
        super().__init__()

    def get(self):
        # Retrieve all report instances from the database
        reports = database_controller.get_all_reports()
        print('-----------------------')
        for report in reports:
            print(report.__str__())

        print('-----------------------')
        # Format the reports data as needed
        formatted_reports = [{"report_id": report.id, "scooter_id": report.scooter_id, "description": report.description, "time_of_report": report.time_of_report, "status": report.status} for report in reports]
        return formatted_reports

#Retreives 
api.add_resource(GetAllRepairs, "/all_repairs")
api.add_resource(GetAllReports, "/all_reports")

# Actions
api.add_resource(addScooter, "/add_scooter")
api.add_resource(Make_Booking, "/add_booking")    
api.add_resource(Registration, "/register")
api.add_resource(Make_Report, "/new_report")
api.add_resource(Make_Repair, "/new_repair")
api.add_resource(Top_up_Balanace, "/top_up")
api.add_resource(editScooter, "/edit_scooter")
api.add_resource(editCustomer, "/edit_customer")
api.add_resource(cancelBooking, "/cancel_booking")

if __name__ == "__main__":
    app.run(debug=True)
    
    

