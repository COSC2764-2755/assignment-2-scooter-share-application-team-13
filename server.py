import socket
import requests, json
from passlib.hash import sha256_crypt
import datetime


BASE = "http://127.0.0.1:5000/api/" #
USERNAME = "admin"
PASSWORD_HASH = sha256_crypt.hash("pass123")
HOST = ""
PORT = 65000
ADDRESS = (HOST, PORT)







def validate_login(received_username, received_hash):
    endpoint = "login"  # Make sure this matches the API endpoint
    customer_data = {
        "customer": received_username,
        "password": received_hash
    }
    response = requests.get(BASE + endpoint, data=json.dumps(customer_data))  #Assumes the api returns true or false #API login method needs to be made
    response_data = response.json()
    if response_data.get("success") is True:
        print("Logged in")
        return True
    else:
        print("Login failed")
        return False


def find_booking(received_username, booked_scooter_id, time):
    endpoint = "get_single_booking" #Need to make this
    booking_data = {
        "customer": received_username,
        "scooter_id":booked_scooter_id,
        "time": time #Time is a datetime and not a string 
    }
    response = requests.get(BASE + endpoint, data=json.dumps(booking_data))

    if response.status_code == 200:
        booking_data = response.json()
        if booking_data:
            # Create a Booking object if data is present
            booking = Booking( #Add records import 
                location=booking_data['location'],
                scooter_id=booking_data['scooter_id'],
                customer=booking_data['customer'],
                start_time=booking_data['start_time'],
                duration=booking_data['duration'],
                cost=booking_data['cost'],
                status=booking_data['status']
            )
            return booking
        else:
            # No booking data found
            return None
    else:
        # Handle the API request error here
        print("Error: Unable to retrieve booking data.")
        return None

    

def wait_for_login_input():
    print("Server Initializing...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        s.listen()

        while True:
            print(f"Listening on {ADDRESS}...")
            conn, addr = s.accept()
            with conn:
               
                # Receive username and hashed password from client
                data = conn.recv(4096).decode()
                received_username, received_hash, scooter_id = data.split(":")
                print(f"Received username: {received_username} Received hash: {received_hash}")

                return received_username,received_hash, scooter_id


def sendBooking(endTime):
    #Send booking details to Client
    
def updateBookingStatus(booking_id, new_status):


for username, passowrd, scooter in wait_for_login_input():
    if not validate_login(username, passowrd):
        print('Failure to sign in') # Restart 
    
    booking_object = find_booking(username, scooter, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if booking_object is not None and isinstance(booking_object, Booking()):

  
        


        



