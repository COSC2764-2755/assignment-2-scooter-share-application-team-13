import socket
from passlib.hash import sha256_crypt


USERNAME = "admin"
PASSWORD_HASH = sha256_crypt.hash("pass123")
HOST = ""
PORT = 65000
ADDRESS = (HOST, PORT)

print("Server Initializing...")
print("Server Ready. Awaiting connections.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()

    while True: 
        print("Listening on {}...".format(ADDRESS))
        conn, addr = s.accept()
        with conn:
            IP = addr[0]
            socket_addr = addr[1]
            print(f"IP address: {IP} Socket address {socket_addr}")
          
            # Receive username and hashed password from client
            data = conn.recv(4096).decode()
            received_username, received_hash = data.split(":")

            print(f"IP address: {received_username} Something else {received_hash}")


        USERNAME = 'Joshua'

            # Checking the received username and hash match the stored values
            if received_username == USERNAME and sha256_crypt.verify("pass123", received_hash):
                conn.sendall("Authentication Successful!".encode())
                print("Authentication Successful for Scooter [{}].".format(scooter_id))
            else:
                conn.sendall("Authentication Failed!".encode())
                print("Authentication Failed for Scooter [{}].".format(scooter_id))

            print("Scooter [{}] disconnected.".format(scooter_id))

        print("Awaiting next scooter connection...")

    print("Server shutting down...")





#Assumably this acts as a component of the main pi, taking messages from the AP.

#login validation 
#Booking validation # Get bookings that are both for a user and scooter id (figure out which booking the person is trying to start)
#Scooter and booking stage managment from AP to MP and through to API 