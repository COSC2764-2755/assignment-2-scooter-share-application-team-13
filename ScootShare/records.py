# Store classes

class Customer():
    def __init__(self, id, f_name, l_name, ph_num, email, username, password, balance) -> None:
        self._customer_id = id
        self._first_name = f_name
        self._last_name = l_name
        self._phone_number = ph_num
        self._email_address = email
        self._username = username
        self._password = password
        self._balance = balance

