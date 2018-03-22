from flask import Flask, current_app

import jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta


class User():
    def __init__(self, email, username, password):
        """Initialize the user with an email, a username and a password"""
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

    @staticmethod
    def generate_token(email):
        """Generates the access token"""
        try:
            payload = {
                'iss': "weconnect",
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': email
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
