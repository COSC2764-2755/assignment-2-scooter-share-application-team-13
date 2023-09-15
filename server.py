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
            scooter_id = addr[0]  
            print("Scooter [{}] connected.".format(scooter_id))

            # Receive username and hashed password from client
            data = conn.recv(4096).decode()
            received_username, received_hash = data.split(":")

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
