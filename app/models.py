from flask import Flask
from flask_bcrypt import Bcrypt


class User():
    """user contains an email, a username and a password"""
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

    def __repr__(self):
        return 'user is {}'.format(self.email)


class Business():
    """contains the business model"""
    def __init__(self, business_id, business_name, category, location,
                 created_by):
        self.business_id = business_id
        self.business_name = business_name
        self.category = category
        self.location = location
        self.created_by = created_by
        self.reviews = []

    def serialize(self):
        return {'business_id': self.business_id,
                'business_name': self.business_name,
                'category': self.category,
                'location': self.location,
                'created_by': self.created_by}

    def __repr__(self):
        return 'business is {}'.format(self.business_name)