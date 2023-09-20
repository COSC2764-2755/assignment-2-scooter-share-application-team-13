# Store classes

class Customer():
    def __init__(self, id, f_name, l_name, ph_num, email, username, password, balance) -> None:
        self.customer_id = id
        self.first_name = f_name
        self.last_name = l_name
        self.phone_number = ph_num
        self.email_address = email
        self.username = username
        self.password = password
        self.balance = balance

