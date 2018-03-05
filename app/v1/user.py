from flask import Flask, current_app

import jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
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

    def reset_password(self, email, old_pass, new_pass):
        user_values = USERS[email]
        if Bcrypt().check_password_hash(user_values[1], old_pass):
            self.password = Bcrypt().generate_password_hash(new_pass).decode()
            USERS[email][1] = self.password
            if USERS[email][1] == self.password:
                return True
            return False
        return False

    def generate_token(self, email):
        """Generates the access token"""
        self.email = email
        try:
            payload = {
                'iss': "weconnect",
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': self.email
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the authorization header"""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
