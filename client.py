import socket
from passlib.hash import sha256_crypt

HOST = input("Enter IP address of server: ")
PORT = 65000
ADDRESS = (HOST, PORT)

scooter_id = input("Enter scooter ID: ")
password = input("Enter scooter password: ")

hashed_password = sha256_crypt.hash(password)

print("Attempting to connect to the server...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(ADDRESS)
    print("Connected to the server.")

    # Send scooter_id and hashed password to server
    s.sendall(f"{scooter_id}:{hashed_password}".encode())
    response = s.recv(4096).decode()
    print(response)

    print("Disconnecting from server.")
print("Connection closed.")
