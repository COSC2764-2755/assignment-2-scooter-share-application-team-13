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


#Test create scooter
        # Define the scooter data for testing
scooter_data = {
            "status": "Available",
            "make": "XYZ",
            "color": "Red",
            "location": "Location A",
            "power": 80,
            "cost": 5.0
        }
headers = {"Content-Type": "application/json"}  # Set the Content-Type header
endpoint = "add_scooter"
response = requests.put(BASE + endpoint, data=json.dumps(scooter_data), headers=headers)  # Use json.dumps to convert the payload to JSON

print(response.json())

#Test create scooter
        # Define the scooter data for testing
scooter_data = {
            "status": "Available",
            "make": "ABC",
            "color": "Blue",
            "location": "Location A",
            "power": 90,
            "cost": 6.0
        }
headers = {"Content-Type": "application/json"}  # Set the Content-Type header
endpoint = "add_scooter"
response = requests.put(BASE + endpoint, data=json.dumps(scooter_data), headers=headers)  # Use json.dumps to convert the payload to JSON

print(response.json())   

#Test create Booking 
# Test create booking
# Define the booking data for testing
booking_data = {
    "location": "Location C",
    "scooter_id": 1,  
    "customer_id": 3,  
    "start_time": "2023-09-28 14:00:00",  
    "duration": 45,  # 
    #The cost of a booking will be durtion (in mins) * scootercostPerMin
    "cost": 5.0,  
    "status": "Upcoming"
}
headers = {"Content-Type": "application/json"}  # Set the Content-Type header
endpoint = "add_booking"  # Replace with the appropriate endpoint for adding a booking
response = requests.put(BASE + endpoint, data=json.dumps(booking_data), headers=headers)  # Use json.dumps to convert the payload to JSON

print(response.json())


#Test create Booking 
# Test create booking
# Define the booking data for testing
booking_data = {
    "location": "Location B",
    "scooter_id": 1,  
    "customer_id": 1,  
    "start_time": "2023-09-28 14:00:00",  
    "duration": 50,  # 
    #The cost of a booking will be durtion (in mins) * scootercostPerMin
    "cost": 7.0,  
    "status": "Upcoming"
}
headers = {"Content-Type": "application/json"}  # Set the Content-Type header
endpoint = "add_booking"  # Replace with the appropriate endpoint for adding a booking
response = requests.put(BASE + endpoint, data=json.dumps(booking_data), headers=headers)  # Use json.dumps to convert the payload to JSON

print(response.json())