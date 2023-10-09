import socket
import requests, json
from passlib.hash import sha256_crypt
import datetime
import socket_utils
from records import *
#Import records
BASE = "http://127.0.0.1:5000/api/" #
#USERNAME = "admin"
#PASSWORD_HASH = sha256_crypt.hash("pass123")
HOST = ""
PORT = 65000
ADDRESS = (HOST, PORT)







def main():
    
    for username, passowrd in wait_for_login_input():
        if not validate_login_from_api(username, passowrd):
            print('Failure to sign in') # Restart 

    for username,scooter_id in wait_for_scooter_id():      
        booking_object = find_booking_from_api(username, scooter_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        #Send the booking details to client, determine if they are starting the booking #(retruns a true or false)
        if send_booking_determine_ifto_start(booking_object):
                updateBookingStatus(booking_object.id, 'started') #ensure this matches up with the records class

                wait_for_booking_end()
                updateBookingStatus(booking_object.booking_id, 'completed')

            #Make a method to wait for the scooter to tell us the booking is over 
        



#   Wait for login input
def wait_for_login_input():
    print("Waiting for login details")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        s.listen()

        while True:
            print(f"Listening on {ADDRESS}...")
            conn, addr = s.accept()
            with conn:
               
                # Receive username and hashed password from client
                data = conn.recv(4096).decode()
                received_username, received_hash = data.split(":")
                print(f"Received username: {received_username} Received hash: {received_hash}")

                return received_username,received_hash



#Test login input
def validate_login_from_api(received_username, received_hash):
    endpoint = "booking_login"  # Make sure this matches the API endpoint
    customer_data = {
        "customer": received_username,
        "password": received_hash
    }
    response = requests.get(BASE + endpoint, data=json.dumps(customer_data))  #Assumes the api returns true or false #API login method needs to be made
    response_data = response.json()

    #Doube check how we will do the reponse
    if response_data.get("success") is True:
        print("Logged in")
        return True
    else:
        print("Login failed")
        return False

def send_login_result():
    #Success or failure

            
def wait_for_scooter_id():
    print("Waiting to receive id")
    username = 1
    scooter_id = 2

    return username, scooter_id

def find_booking_from_api(received_username, booked_scooter_id, time):
    endpoint = "get_single_booking" #Need to make this
    booking_data_to_send = {
        "customer": received_username,
        "scooter_id":booked_scooter_id,
        "time": time #Time is a datetime and not a string 
    }
    response = requests.get(BASE + endpoint, data=json.dumps(booking_data_to_send))

    if response.status_code == 200: # error code 200 means success 
        booking_data = response.json()
        if booking_data:
            # Create a Booking object if data is present
            booking = Booking( #Add records import 
                
                booking_id=booking_data['booking_id'],
                location=booking_data['location'],
                scooter_id=booking_data['scooter_id'],
                customer_id=booking_data['customer'],
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


#Send booking details # Wait for reply , send even if none as that will automically make the reply no. #Wait for reply
def send_booking_determine_ifto_start(booking):

    #if booking is None:
     #   return False


    # Send booking details to Client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(ADDRESS)
        print("Connected.")
        socket_utils.sendJson(s, booking)

        # Ask if the user wants to start the booking on the client side
        while True:
            response = socket_utils.recvJson(s)
            if "yes" in response:
                return True
            elif "no" in response:
                return False



#Update booking status when send_booking_determine_ifto_start() returns true, and when waitforbookingtoend recives a end message
def updateBookingStatus(booking_id, new_status):
    endpoint= "update_booking"
    booking_data = {
        "booking_id": booking_id,
        "new_status": new_status
    }
    reponse = requests.get(BASE + endpoint, data=json.dumps(booking_data)) #consider validation for the reponse
    print(f"booking status for booking id: {booking_id} changed to {new_status}")

    


  
def wait_for_booking_end():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(ADDRESS)
        print("Connected, waitng for the booking to end")
        response = socket_utils.recvJson(s)
        #See if this needs to return anything




