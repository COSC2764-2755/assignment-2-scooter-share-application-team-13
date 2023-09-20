import requests, json

BASE = "http://127.0.0.1:5000/"

# Test create user
test_username = "Garry"
payload = {"id": 1,
           "first_name": "Garry",
           "last_name": "Howitzer",
           "phone_number": "1122334455",
           "email_address": "test@example.com",
           "username": "Gazza",
           "password": "Howie123",
           "balance": 69.96}
headers = {"Content-Type": "application/json"}  # Set the Content-Type header
endpoint = "register"
response = requests.put(BASE + endpoint, data=json.dumps(payload), headers=headers)  # Use json.dumps to convert the payload to JSON

print(response.json())