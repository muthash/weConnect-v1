import os
from app.v1 import v1

from flask import Blueprint, make_response, request, jsonify, json
from app.v1.user import User, USERS
from app.v1 import validate as val

user = User()


@v1.route('/register', methods=['GET', 'POST'])
def register():
    """This class registers a new user."""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        cpassword = data.get('cpassword')

        validated_email = val.check_email(email)
        if not validated_email:
            response = {
                        'message': 'Invalid email address'
                    }
            return make_response(jsonify(response)), 400
        validated_username = val.check_name(username)
        if not validated_username:
            response = {
                        'message': 'Invalid username'
                    }
            return make_response(jsonify(response)), 400
        already_user = email in USERS.keys()
        if not already_user:
            try:
                user.create_account(email, username, password)
                response = {
                        'message': 'You registered successfully'
                    }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        response = {
                'message': 'User already exists.Please login'
        }
        return make_response(jsonify(response)), 202


@v1.route('/login', methods=['GET', 'POST'])
def login():
    """This view handles user login and access token generation."""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        already_user = email in USERS.keys()
        if already_user:
            try:
                try_login = user.login(email, password)
                if try_login:
                    access_token = user.generate_token(email)
                    if access_token:
                        response = {
                            'message': 'You logged in successfully',
                            'access_token': access_token.decode()
                        }
                        return make_response(jsonify(response)), 200
                response = {
                    'message': 'Invalid email or password'
                }
                return make_response(jsonify(response)), 401
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500
        response = {
                'message': 'This user does not exist. Please register'
            }
        return make_response(jsonify(response)), 401
