from flask_bcrypt import Bcrypt


class User():
    """user contains an email, a username and a password"""
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

    def update_password(self, password):
        self.password = Bcrypt().generate_password_hash(password).decode()

    def __repr__(self):
        return 'user is {}'.format(self.email)


class Business():
    """contains the business model"""
    this_id = 0

    def __init__(self, name, category, location, created_by):
        Business.this_id += 1
        self.id = Business.this_id
        self.name = name
        self.category = category
        self.location = location
        self.created_by = created_by
        self.reviews = []

    def serialize(self):
        return {'business_id': self.id,
                'business_name': self.name,
                'category': self.category,
                'location': self.location,
                'reviews': self.reviews
                }

    def __repr__(self):
        return 'business is {}'.format(self.id)
