import os
from . import v1

from flask import Flask, make_response, request, jsonify
from .user import User, USERS

user = User()


@v1.route('/register', methods=['GET', 'POST'])
def register():
    """This class registers a new user."""
    if request.method == 'POST':
        email = request.data['email']
        username = request.data['username']
        password = request.data['password']
        cpassword = request.data['cpassword']

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
        email = request.data['email']
        password = request.data['password']
        already_user = email in USERS.keys()
        if already_user:
            try:
                try_login = user.login(email, password)
                if try_login:
                    response = {
                        'message': 'You logged in successfully'
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
