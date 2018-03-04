USERS = {}


class User():
    def __init__(self):
        """Initialize the user with an email and a password."""
        self.email = None
        self.username = None
        # self.password = Bcrypt().generate_password_hash(password).decode()
        self.password = None

    def create_account(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        USERS[self.email] = [self.username, self.password]