import requests, json
from records import *

BASE = "http://127.0.0.1:5000/"




def create_user():
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


def create_scooters():

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




def create_bookings():

    #Test create Booking 
    # Test create booking
    # Define the booking data for testing
    booking_data = {
        "location": "Location C",
        "scooter_id": 1,  
        "customer_id": 1,  
        "start_time": "2023-09-28 14:00:00",  
        "duration": 45,  # 
        #The cost of a booking will be durtion (in mins) * scootercostPerMin
        "cost": 1.0,  
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

def create_report():
    # Define the report data for testing
    report_data = {
        "scooter_id": "1",
        "description": "Broken headlight",
        "time_of_report": "2023-09-28 15:30:00",
        "status": "Reported"
    }

    headers = {"Content-Type": "application/json"}  # Set the Content-Type header
    report_endpoint = "new_report"
    report_response = requests.put(BASE + report_endpoint, data=json.dumps(report_data), headers=headers)

    print("----------------------------report sent-----reponse:---------")
    print(report_response.json())

  
   



def create_repair_job():
    print("----------------------------Sending a repair job------------")

    # Define the repair data for testing
    repair_data = {
        "scooter_id": "1",
        "description": "Replace brake pads", #Should consider logic to get the report descrition and make it the repair description on making a repair
        "linked_report_id": "1",
        "time_of_repair": "2023-09-29 10:00:00"
    }
    headers = {"Content-Type": "application/json"}  # Set the Content-Type header
    repair_endpoint = "new_repair"
    repair_response = requests.put(BASE + repair_endpoint, data=json.dumps(repair_data), headers=headers)

    print("Repair Response:")
    print(repair_response.json())

def get_all_repairs():
    #This gets a list of all repairs, this is a good starting example of how to get data from the api
    repair_endpoint = "all_repairs"
    repair_response = requests.get(BASE + repair_endpoint)
    print("----------------------------Getting all repair jobs--------------")

    print(repair_response.json())  # Print the response content, which contains all repairs 
    #This is returned: [{'repair_id': 1, 'scooter_id': 1, 'description': 'Replace brake pads', 'linked_report_id': 1, 'time_of_repair': '2023-09-29 10:00:00'}]

    repairs_data =repair_response.json()
    repairs = []
    for data in repairs_data:
        repair = Repair(
            scooter_id=data['scooter_id'],
            description=data['description'],
            linked_report_id=data['linked_report_id'],
            time_of_repair=data['time_of_repair'],
            repair_id=data['repair_id']
        )
        repairs.append(repair)
    # Now, the 'repairs' list contains instances of the Repair class
    #This code will extract the JSON data from repair_response and iterate through it, 
    # creating instances of the Repair class for each repair entry in the JSON data. The resulting repairs list will contain these instances.

    print('---------Here are all repairs--------------')
    for repair in repairs:
        print(repair.__str__())
    print('-----------------------')



def get_all_reports():
    reports_endpoint = "all_reports"
    reports_response = requests.get(BASE + reports_endpoint)

    print("----------------------------Getting all reports from json-------------")
    print(reports_response.json())  # Print the response content, which contains all reports

    # Assuming reports_data is a list of dictionaries containing report information
    reports_data = reports_response.json()
    reports = []

    for data in reports_data:
        report = Report(
            scooter_id=data['scooter_id'],
            description=data['description'],
            time_of_report=data['time_of_report'],
            status=data['status'],
            report_id=data['report_id']
        )
        reports.append(report)

    # Now, the 'reports' list contains instances of the Report class
    # This code will extract the JSON data from report_response and iterate through it, creating instances of the Report class for each report entry in the JSON data. The resulting reports list will contain these instances.

    print('---------All reports from report objects--------------')
    for report in reports:
        print(report.__str__())
    print('-----------------------')



#Need to test
def get_all_customers():
    customers_endpoint = "all_customers"
    customers_response = requests.get(BASE+ customers_endpoint)
    print("----------------------------Getting all reports from json-------------")
    print(customers_response.json())  # Print the response content, which contains all customers

    customers_data = customers_response.json()
    customers = []

    for data in customers_data:
        customer = Customer(
            id=data['customer_id'],
            f_name=data['first_name'],
            l_name=data['last_name'],
            ph_num=data['phone_number'],
            email=data['email_address'],
            username=data['username'],
            password=data['password'],
            balance=data['balance']
        )
        customers.append(customer)

    # Now, the 'customers' list contains instances of the Customer class
    # This code will extract the JSON data from customers_response and iterate through it, creating instances of the Customer class for each customer entry in the JSON data. The resulting customers list will contain these instances.

    print('---------All customers from Customer objects--------------')
    for customer in customers:
        print(customer.__str__())
    print('-----------------------')
    

def get_single_customer():
    customer_endpoint = "get_customer"
    customers_response = requests.get(BASE+ customer_endpoint, data=json.dumps(customer_data))

    customer_data = {
        "id": 1
    }



def main():
    #Creates users,scooters,bookings and reports on api call
    create_user()
    create_scooters()
    create_bookings()
    create_report()

#Youl notice that the report is initially created as reported, after creating a repair job for that report it will set the report to addressed
    get_all_reports() #will show a reported report (unaddressed)
    create_repair_job() #This method creates a report job to address the created report
    get_all_reports() #will show a addressed report
    get_all_repairs() #This is the repair done
    

if __name__ == "__main__":
    main()