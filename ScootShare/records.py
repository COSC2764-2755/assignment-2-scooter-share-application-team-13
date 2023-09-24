# Store classes

class Customer():
    def __init__(self, username, f_name, l_name, ph_num, email, password, balance) -> None:
        self.username = username
        self.first_name = f_name
        self.last_name = l_name
        self.phone_number = ph_num
        self.email_address = email
        self.password = password
        self.balance = balance