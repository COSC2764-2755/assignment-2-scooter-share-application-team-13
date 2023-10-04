# Flask main
from flask import Flask
from flask_restful import Api, Resource, reqparse
from records import Customer
from db import DatabaseConnector

app = Flask(__name__)
api = Api(app)
database_controller = DatabaseConnector() 
# Temp methods while db is local
database_controller.create_customer_table() 
database_controller.create_staff_table()
database_controller.populate_staff() # Populate staff table with dummy accounts


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
        
        database_controller.add_customer(customer_object)

        return f"Account with username {customer_object.username} created successfully!"
        
class Login(Resource):
    def __init__(self) -> None:
        super().__init__()
        self._cust_login_args = reqparse.RequestParser()
        self._cust_login_args.add_argument("username", type=str, help="username")
        self._cust_login_args.add_argument("password", type=str, help="password")

    def post(self):
            args = self._cust_login_args.parse_args()
            username = args['username']
            password = args['password']
            #if username starts with ~ or _ then user is a staff member
            # ~ prefix is for admins, _ prefix is for engineers
            if username[0] == '~' or username[0] == '_':
                db_user = database_controller.get_staff(username, password)
                if db_user:
                    return f"Successfully signed in as {db_user.username}"
                else:
                    return "Invalid username or password"
            # else user is a customer  
            else: 
                db_user = database_controller.get_customer(args['username'], args['password'])
                if db_user:
                    return f"Successfully signed in as {db_user.username}"

api.add_resource(Registration, "/api/register")
api.add_resource(Login, '/api/login')

if __name__ == "__main__":
    app.run(debug=True)