# Flask main
from flask import Flask
from flask_restful import Api, Resource, reqparse
from records import Customer
from db import DatabaseConnector

app = Flask(__name__)
api = Api(app)

class Registration(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._cust_reg_args = reqparse.RequestParser()
        self._cust_reg_args.add_argument("username", type=str, help="username")
        self._cust_reg_args.add_argument("first_name", type=str, help="Customer fName")
        self._cust_reg_args.add_argument("last_name", type=str, help="Customer lName")
        self._cust_reg_args.add_argument("phone_number", type=str, help="phone num")
        self._cust_reg_args.add_argument("email_address", type=str, help="email")
        self._cust_reg_args.add_argument("password", type=str, help="password")
        self._cust_reg_args.add_argument("balance", type=float, help="balance")

    def post(self):
        args = self._cust_reg_args.parse_args()
        customer_object = Customer(args['username'], args['first_name'], args['last_name'], 
                                   args['phone_number'], args['email_address'], 
                                   args['password'], args['balance'])
        
        database_controller = DatabaseConnector() # TODO: Find somewhere better to initialise db
        database_controller.create_table()
        
        database_controller.add_customer(customer_object)

        return f"{customer_object.first_name} has the password {customer_object.password}"
    
    
class Login(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._cust_login_args = reqparse.RequestParser()
        self._cust_login_args.add_argument("username", type=str, help="username")
        self._cust_login_args.add_argument("password", type=str, help="password")

    def post(self):
            args = self._cust_login_args.parse_args()
            database_controller = DatabaseConnector() # TODO: Find somewhere better to initialise db
            db_user = database_controller.get_customer(args['username'], args['password'])
            if db_user:
                 return f"Successfully signed in as {db_user.username}"

api.add_resource(Registration, "/api/register")
api.add_resource(Login, '/api/login')

if __name__ == "__main__":
    app.run(debug=True)