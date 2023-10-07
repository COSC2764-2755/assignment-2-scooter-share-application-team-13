import socket
from passlib.hash import sha256_crypt

HOST = input("Enter IP address of server: ") # Defaults to listen on all Ip's
PORT = 65000
ADDRESS = (HOST, PORT)






username = input("Enter Username : ")
password = input("Enter password: ")
scooter_id = input("Enter the scooter ID for your booked scooter: ")

hashed_password = sha256_crypt.hash(password)

print("Attempting to connect to the server...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(ADDRESS)
    print("Connected to the server.")

    # Send cusotmer_id and hashed password to server
    s.sendall(f"{username}:{hashed_password}".encode())
    print("Username and password sent")
    #response = s.recv(4096).decode()
    #print(response)

    print("Disconnecting from server.")
print("Connection closed.")







#Beginining notes

#We need a login function , to take username and password
#We need to also ask for the scooter id that the user has booked for

#On login send credentials to MP/server.   #server will contact API and get credentials to match from db
#Recive a true or false to determine if login was successful 


#If the login was successful we now want to deal with booking tracking/activation 
#We need to determine whihch booking in the db is the intented to be used 

#Get all bookings for a scooter id
#Filter those bookings by customer id, that way we have all bookibgs for a particualr user for a particualr scooter 

#Loop through list of these bookings
#If current time  is after the start time of the booking but also before the end time of the booking instance we can determine that this is the booking we are looking for
# 
#  #The booking status also needs to be kept in mind as we will need to change this, aswell as maybe the scooter status\

#One more not iis that a scooter is locked or unlocked, during the duration of a bokking it is set as unlocked - double check this -


#We may need an alarm for endtime
#If the booking status is started/in progress we want to end the booking when the current time = to end time 
# Updated data will also need to be resent to the MP and to the db 