# Flask main
from flask import Flask
from flask_restful import Api, Resource, reqparse
from records import Customer

app = Flask(__name__)
api = Api(app)

cust_put_args = reqparse.RequestParser()
cust_put_args.add_argument("id", type=int, help="CustomerID")
cust_put_args.add_argument("first_name", type=str, help="Customer fName")
cust_put_args.add_argument("last_name", type=str, help="Customer lName")
cust_put_args.add_argument("phone_number", type=str, help="phone num")
cust_put_args.add_argument("email_address", type=str, help="email")
cust_put_args.add_argument("username", type=str, help="username")
cust_put_args.add_argument("password", type=str, help="password")
cust_put_args.add_argument("balance", type=float, help="balance")


class Registration(Resource):
    def __init__(self) -> None:
        super().__init__()
        
    def put(self):
        args = cust_put_args.parse_args()
        customer_object = Customer(args['id'], args['first_name'], args['last_name'], 
                                   args['phone_number'], args['email_address'], 
                                   args['username'], args['password'], args['balance'])
        return f"{customer_object._first_name} has the password {customer_object._password}"
    
    
api.add_resource(Registration, "/register")

if __name__ == "__main__":
    app.run(debug=True)