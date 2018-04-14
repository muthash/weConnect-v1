from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models import User
# from app.utils import (
#     validate_null, random_string, send_reset_password, messages
# )
from app.baseview import BaseView

auth = Blueprint('auth', __name__, url_prefix='/api/v1')
users = []


class RegisterUser(BaseView):
    """Method to Register a new user"""
    def post(self):
        """Endpoint to save the data to the database"""
        if not self.validate_json():
            data = request.get_json()
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            user_data = {'email': email, 'username': username,
                        'password': password}
            if not self.validate_null(**user_data):
                if not self.check_email(email):
                    emails = [user.email for user in users]
                    if email not in emails:
                        user = User(email, username, password)
                        users.append(user)
                        response = {'message': 'Account created successfully'}
                        return jsonify(response), 201
                    response = {'message': 'User already exists. Please login'}
                    return jsonify(response), 409
                return self.check_email(email)
            return self.validate_null(**user_data)
        return self.validate_json()


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
