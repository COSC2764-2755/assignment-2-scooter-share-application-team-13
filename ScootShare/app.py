# Flask main
from flask import Flask, render_template, make_response
from flask_restful import Api, Resource, reqparse
from records import Customer
from db import DatabaseConnector


app = Flask(__name__)
api = Api(app)


class Registration(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._cust_reg_args = reqparse.RequestParser()
        self._cust_reg_args.add_argument(
            "username", type=str, help="username", location='form')
        self._cust_reg_args.add_argument(
            "first_name", type=str, help="Customer fName", location='form')
        self._cust_reg_args.add_argument(
            "last_name", type=str, help="Customer lName", location='form')
        self._cust_reg_args.add_argument(
            "phone_number", type=str, help="phone num", location='form')
        self._cust_reg_args.add_argument(
            "email_address", type=str, help="email", location='form')
        self._cust_reg_args.add_argument(
            "password", type=str, help="password", location='form')
        self._cust_reg_args.add_argument(
            "balance", type=float, help="balance", location='form')

    def post(self):
        args = self._cust_reg_args.parse_args()
        customer_object = Customer(args['username'], args['first_name'], args['last_name'],
                                   args['phone_number'], args['email_address'],
                                   args['password'], args['balance'])
        # TODO: Find somewhere better to initialise db
        database_controller = DatabaseConnector()
        database_controller.create_table()

        database_controller.add_customer(customer_object)

        return f"Account with username {customer_object.username} created successfully!"

    def get(self):
        return make_response(render_template("register.html"))


class Login(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._cust_login_args = reqparse.RequestParser()
        self._cust_login_args.add_argument(
            "username", type=str, help="username", location='form')
        self._cust_login_args.add_argument(
            "password", type=str, help="password", location='form')

    def post(self):
        args = self._cust_login_args.parse_args()
        # TODO: Find somewhere better to initialise db
        database_controller = DatabaseConnector()
        password = None

        db_user = database_controller.get_customer(
            args['username'], args['password'])
        if db_user:
            return f"Successfully signed in as {db_user.username}"

    def get(self):
        return make_response(render_template("login.html"))


class Landing(Resource):
    def get(self):
        return make_response(render_template("landing.html"))


class Booking(Resource):
    def get(self):
        return make_response(render_template("booking.html"))


api.add_resource(Landing, '/')
api.add_resource(Registration, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Booking, '/booking')

if __name__ == "__main__":
    app.run(debug=True)
