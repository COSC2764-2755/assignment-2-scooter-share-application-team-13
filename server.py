import socket
import requests, json
from passlib.hash import sha256_crypt

BASE = "http://127.0.0.1:5000/api/" #
USERNAME = "admin"
PASSWORD_HASH = sha256_crypt.hash("pass123")
HOST = ""
PORT = 65000
ADDRESS = (HOST, PORT)

print("Server Initializing...")
print("Server Ready. Awaiting connections.")


def validate_login(received_username, received_hash):
    endpoint = "login" #We need to ensure this matches the function
    customer_data = {
        "customer": received_username,
        "password": received_hash
    }
    response = requests.get(BASE+ endpoint, data=json.dumps(customer_data))
    response_data = response.json()

    #Logic coming to decode the response
    return True



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()

    while True:
        print(f"Listening on {ADDRESS}...")
        conn, addr = s.accept()
        with conn:
            IP = addr[0]
            socket_addr = addr[1]
            print(f"IP address: {IP} Socket address: {socket_addr}")

            # Receive username and hashed password from client
            data = conn.recv(4096).decode()
            received_username, received_hash = data.split(":")

            print(f"Received username: {received_username} Received hash: {received_hash}")

            # Now use API to make a customer object based on supplied username (received_username)

            # Checking if the received username and hash match the stored values
            if sha256_crypt.verify("pass123", received_hash):
                conn.sendall("Authentication Successful!".encode())
                print(f"Authentication Successful for user: [{received_username}].")
            else:
                conn.sendall("Authentication Failed!".encode())
                print(f"Authentication Failed for user: [{received_username}].")





      





#Assumably this acts as a component of the main pi, taking messages from the AP.

#login validation 
#Booking validation # Get bookings that are both for a user and scooter id (figure out which booking the person is trying to start)
#Scooter and booking stage managment from AP to MP and through to API 