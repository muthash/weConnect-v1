from flask_bcrypt import Bcrypt

USERS = {}


class User():
    def __init__(self):
        """Initialize the user with an email and a password."""
        self.email = None
        self.username = None
        self.password = None

    def create_account(self, email, username, password):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        USERS[self.email] = [self.username, self.password]

    def login(self, email, password):
        self.email = email
        self.password = password
        """ Method to check if passwords match"""
        dbvalues = USERS[self.email]
        if Bcrypt().check_password_hash(dbvalues[1], self.password):
            return True
        return False
