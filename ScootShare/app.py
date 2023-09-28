# Flask main
from flask import Flask
from flask_restful import Api, Resource, reqparse
from records import *
from db import DatabaseConnector


app = Flask(__name__)
api = Api(app)

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
        
        database_controller = DatabaseConnector() # TODO: Find somewhere better to initialise db
        database_controller.create_table()
        
        database_controller.add_customer(customer_object)

        return f"{customer_object.first_name} has the password {customer_object.password}"
    

class Make_Booking(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._booking_put_args = reqparse.RequestParser()
        self._booking_put_args.add_argument("location", type=str, help="Booking location")
        self._booking_put_args.add_argument("booking_id", type=int, help="Booking ID")
        self._booking_put_args.add_argument("scooter_id", type=int, help="Scooter ID")
        self._booking_put_args.add_argument("customer_id", type=int, help="Customer ID")
        self._booking_put_args.add_argument("start_time", type=str, help="Start time")
        self._booking_put_args.add_argument("duration", type=float, help="Booking duration")
        self._booking_put_args.add_argument("cost", type=float, help="Booking cost")
        self._booking_put_args.add_argument("status", type=str, help="Booking status")

    def put(self):
        args = self._booking_put_args.parse_args()
        booking_object = Booking(args['location'], args['booking_id'],
            args['scooter_id'], args['customer_id'],
            args['start_time'], args['duration'],
            args['cost'], args['status'])

        database_controller = DatabaseConnector()  # TODO: Find somewhere better to initialize db
        database_controller.create_table()
        database_controller.add_booking(booking_object)

        return f"You have made a booking for {booking_object.start_time} under the customer id: {booking_object.customer_id}"

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

        database_controller = DatabaseConnector() # TODO: Find somewhere better to initialise db
        database_controller.create_scooter_table()
        database_controller.add_scoooter(scooter)

        listOfScooters = database_controller.fetch_scooters_from_db()

#Loop here to test 
        for scooter in listOfScooters:
            print("Status:", scooter.status)
            print("Make:", scooter.make)
            print("Color:", scooter.color)
            #You will notice that the id repeats itself, 1,1 i'm not sure what the cause
            #is, though the database is assinging 1 but not incremnting right 
            print("Scooter ID:", scooter.scooter_id)
            print("-----------") 

        return f"You added a new scooter to the db colored {scooter.color} and with a charge of {scooter.power}"


class AddBooking(Resource):
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
        database_controller = DatabaseConnector() # TODO: Find somewhere better to initialise db
        database_controller.create_booking_table()
        database_controller.add_booking(booking)
        listOfBookings = database_controller.get_all_bookings()
    # Perform actions with the booking object, such as storing it in the database or processing the booking.
    





api.add_resource(addScooter, "/add_scooter")
api.add_resource(Make_Booking, "/add_booking")    
api.add_resource(Registration, "/register")

if __name__ == "__main__":
    app.run(debug=True)