import requests, json, unittest
from records import *


BASE = "http://127.0.0.1:5000/api/"
TESTUSERNAME = "Gazza"
TESTPASSWORD = "Howie123"


class TestUserMethods(unittest.TestCase):
    def test_create_user(self):
        # Test create user
        payload = {"username": TESTUSERNAME,
                "first_name": "Garry",
                "last_name": "Howitzer",
                "phone_number": "1122334455",
                "email_address": "test@example.com",
                "password": TESTPASSWORD,
                "balance": 69.96}
        headers = {"Content-Type": "application/json"}  # Set the Content-Type header
        endpoint = "register"
        response = requests.post(BASE + endpoint, data=json.dumps(payload), headers=headers)  # Use json.dumps to convert the payload to JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Account with username Gazza created successfully!")

    def test_login_user(self):
        payload = {
            "username": TESTUSERNAME,
            "password": TESTPASSWORD
        }
        headers = {"Content-Type": "application/json"}  # Set the Content-Type header
        endpoint = "login"
        response = requests.post(BASE + endpoint, data=json.dumps(payload), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"user_type": "customer", "username": "Gazza"})


    def test_get_all_customers(self):
        customers_endpoint = "all_customers"
        response = requests.get(BASE+ customers_endpoint)
        customers_data = response.json()

        customers = []
        for data in customers_data:
            customer = Customer(
                username=data['username'],
                f_name=data['first_name'],
                l_name=data['last_name'],
                ph_num=data['phone_number'],
                email=data['email_address'],
                password=data['password'],
                balance=data['balance']
            )
            customers.append(customer)

        expected = Customer{"username": TESTUSERNAME,
                "first_name": "Garry",
                "last_name": "Howitzer",
                "phone_number": "1122334455",
                "email_address": "test@example.com",
                "password": TESTPASSWORD,
                "balance": 69.96}
        self.assertIn(expected, customers)


    def test_get_single_customer(self):
        customer_endpoint = "get_customer"
        headers = {"Content-Type": "application/json"}
        customer_data = {
            "username": TESTUSERNAME
        }
        response = requests.get(BASE+ customer_endpoint, data=json.dumps(customer_data, headers=headers))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"username": TESTUSERNAME, "first_name": "Garry"})

class TestScooterMethods(unittest.TestCase):
    def create_scooter(self):

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
        response = requests.post(BASE + endpoint, data=json.dumps(scooter_data), headers=headers)  # Use json.dumps to convert the payload to JSON
        self.assertEqual(response.status_code, 200)
        expected_message = f"You added a new scooter to the db colored {scooter_data['color']} and with a charge of {scooter_data['power']}"
        self.assertEqual(response.json(), expected_message)

   

class TestBookingMethods(unittest.TestCase):
    def test_make_booking_success(self):
        # Create a request args dictionary to simulate the booking request data
        booking_data = {
            "location": "Location C",
            "scooter_id": 1,
            "username": TESTUSERNAME,
            "start_time": "2023-09-28 14:00:00",
            "duration": 45,
            "cost": 1.0,
            "status": "Upcoming"
        }


        headers = {"Content-Type": "application/json"}  # Set the Content-Type header
        endpoint = "add_booking"  # Replace with the appropriate endpoint for adding a booking
        response = requests.post(BASE + endpoint, data=json.dumps(booking_data), headers=headers)  # Use json.dumps to convert the payload to JSON

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "You have made a booking!")

    def test_cancel_booking_success(self):
        data ={
            "booking_id": 1
        }
        headers = {"Content-Type": "application/json"}  # Set the Content-Type header
        endpoint = "cancel_booking"  # Replace with the appropriate endpoint for adding a booking
        response = requests.post(BASE + endpoint, data=json.dumps(data), headers=headers)  # Use json.dumps to convert the payload to

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), f"You canceled a booking of id: {data['booking_id']}")



class TestReportMethods(unittest.TestCase):
    def create_report(self):
        # Define the report data for testing
        report_data = {
            "scooter_id": "1",
            "description": "Broken headlight",
            "time_of_report": "2023-09-28 15:30:00",
            "status": "Reported"
        }

        headers = {"Content-Type": "application/json"}  # Set the Content-Type header
        report_endpoint = "new_report"
        report_response = requests.post(BASE + report_endpoint, data=json.dumps(report_data), headers=headers)
        expected_response = f"You made a report for scooter: {report_data['scooter_id']} to address: {report_data['description']}" # Same as the return statement of the method

        # Assert that the response content matches the expected response
        self.assertEqual(report_response.text, expected_response)

       
    def get_all_reports(self):
        reports_endpoint = "all_reports"
        reports_response = requests.get(BASE + reports_endpoint)

        # reports_data is a list of dictionaries containing report information
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

            expected_report_data = Report{
                "scooter_id": "1",
                "description": "Broken headlight",
                "time_of_report": "2023-09-28 15:30:00",
                "status": "Reported"
            }
            self.assertIn(expected_report_data, reports)


   
class TestRepairMethods(unittest.TestCase):
    def create_repair_job(self):
        # Define the repair data for testing
        repair_data = {
            "scooter_id": "1",
            "description": "Replace brake pads", 
            "linked_report_id": "1",
            "time_of_repair": "2023-09-29 10:00:00"
        }
        headers = {"Content-Type": "application/json"}  # Set the Content-Type header
        repair_endpoint = "new_repair"
        repair_response = requests.post(BASE + repair_endpoint, data=json.dumps(repair_data), headers=headers)
        expected_response = f"You did a repair at: {repair_data['time_of_repair']} to address: {repair_data['description']} for scooter {repair_data['scooter_id']}"
         # Return of the make_Repair API

        # Assert that the response content matches the expected response
        self.assertEqual(repair_response.text, expected_response)
        

    def get_all_repairs(self):
        #This gets a list of all repairs, this is a good starting example of how to get data from the api
        repair_endpoint = "all_repairs"
        repair_response = requests.get(BASE + repair_endpoint)
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

        expected_repair = Repair{
            "scooter_id": "1",
            "description": "Replace brake pads", 
            "linked_report_id": "1",
            "time_of_repair": "2023-09-29 10:00:00",
            "repair_id": 1
        }
        # Assert that the expected repair is present in the list of repairs
        #compares objects of the same class
        self.assertIn(expected_repair, repairs)
  




    

# def main():
#     #Creates users,scooters,bookings and reports on api call
#     create_user()
#     create_scooters()
# #     create_bookings()
# #     create_report()

# # #Youl notice that the report is initially created as reported, after creating a repair job for that report it will set the report to addressed
# #     get_all_reports() #will show a reported report (unaddressed)
# #     create_repair_job() #This method creates a report job to address the created report
# #     get_all_reports() #will show a addressed report
# #     get_all_repairs() #This is the repair done
    
# #     create_user()
# #     login_user()

# if __name__ == "__main__":
#     main()

