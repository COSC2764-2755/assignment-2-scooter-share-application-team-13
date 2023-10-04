# Flask main
from flask import Flask
from flask_restful import Api, Resource, reqparse
from records import *
from db import DatabaseConnector

app = Flask(__name__)
api = Api(app)
database_controller = DatabaseConnector() # TODO: Find somewhere better to initialise db
database_controller.create_table()
database_controller.create_booking_table()
database_controller.create_report_table()
database_controller.create_scooter_table()
database_controller.create_repair_table()


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
        
      
        database_controller.add_customer(customer_object)
        return f"{customer_object.first_name} has the password {customer_object.password}"
    

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
       
  
class Make_Booking(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._booking_put_args = reqparse.RequestParser()
        self._booking_put_args.add_argument("location", type=str, help="Booking location")
        self._booking_put_args.add_argument("scooter_id", type=int, help="Scooter ID")
        self._booking_put_args.add_argument("customer_id", type=int, help="Customer ID")
        self._booking_put_args.add_argument("start_time", type=str, help="Start time")
        self._booking_put_args.add_argument("duration", type=int, help="Duration")
        self._booking_put_args.add_argument("cost", type=float, help="Booking cost")
        self._booking_put_args.add_argument("status", type=str, help="Booking status")

    def put(self):
        args = self._booking_put_args.parse_args()
        booking = Booking(
            location=args['location'],
            scooter_id=args['scooter_id'],
            customer_id=args['customer_id'],
            start_time=args['start_time'],
            duration=args['duration'],
            cost=args['cost'],
            status=args['status']
        )
        
        database_controller.add_booking(booking)        
        return f"You have made a booking for {booking.start_time} under the customer id: {booking.customer_id}"


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
        print("Booking added to db")
        return f"You made a report for scooter: {report.scooter_id} to address: {report.description}"

        

class Make_Repair(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._repair_put_args = reqparse.RequestParser()
        self._repair_put_args.add_argument("scooter_id", type=str, help="Scooter ID")
        self._repair_put_args.add_argument("description", type=str, help="Description of the repair")
        self._repair_put_args.add_argument("linked_report_id", type=str, help="Linked report ID")
        self._repair_put_args.add_argument("time_of_repair", type=str, help="Time of repair")
        self._repair_put_args.add_argument("status", type=str, help="Repair status")

    def put(self):
        args = self._repair_put_args.parse_args()
        repair = Repair(
            scooter_id=args['scooter_id'],
            description=args['description'],
            linked_report_id=args['linked_report_id'],
            time_of_repair=args['time_of_repair']
        )

        database_controller.add_repair(repair)
        return f"You did a repair at: {repair.time_of_repair} to address: {repair.description}"


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


api.add_resource(addScooter, "/add_scooter")
api.add_resource(Make_Booking, "/add_booking")    
api.add_resource(Registration, "/register")
api.add_resource(Make_Report, "/new_report")
api.add_resource(Make_Repair, "/new_repair")
api.add_resource(Top_up_Balanace, "/top_up")

if __name__ == "__main__":
    app.run(debug=True)
    
    

