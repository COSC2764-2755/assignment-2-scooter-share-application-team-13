import requests, json

BASE = "http://127.0.0.1:5000/api/"
TESTUSERNAME = "Gazza"
TESTPASSWORD = "Howie123"

def create_user():
    # Test create user
    payload = {"username": TESTUSERNAME,
            "first_name": "Garry",
            "last_name": "Howitzer",
            "phone_number": "1122334455",
            "email_address": "test@example.com",
            "password": TESTPASSWORD,
            "balance": 69.96}
    headers = {"Content-Type": "application/json"}  # Set the Content-Type header
    endpoint = "register"
    response = requests.post(BASE + endpoint, data=json.dumps(payload), headers=headers)  # Use json.dumps to convert the payload to JSON

    print(response.json())

def login_user():
    payload = {
        "username": TESTUSERNAME,
        "password": TESTPASSWORD
    }
    headers = {"Content-Type": "application/json"}  # Set the Content-Type header
    endpoint = "login"
    response = requests.post(BASE + endpoint, data=json.dumps(payload), headers=headers)
    print(response.json())
    
create_user()
login_user()