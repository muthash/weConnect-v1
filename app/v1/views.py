import os
from app.v1 import v1

from flask import Blueprint, make_response, request, jsonify, json
from app.v1.user import User, USERS
from app.v1 import validate as val
from app.v1.business import Business

user = User()
business = []

@v1.route('/register', methods=['GET', 'POST'])
def register():
    """This class registers a new user."""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        if not val.check_email(email):
            response = {'message': 'Invalid email address'}
            return make_response(jsonify(response)), 400
        if not email in USERS.keys():
            try:
                user.create_account(email, username, password)
                response = {'message': 'You registered successfully'}
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 401
        response = {'message': 'User already exists.Please login'}
        return make_response(jsonify(response)), 202


@v1.route('/login', methods=['GET', 'POST'])
def login():
    """This view handles user login and access token generation."""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if email in USERS.keys():
            try:
                if user.login(email, password):
                    access_token = user.generate_token(email)
                    if access_token:
                        response = {
                            'message': 'You logged in successfully',
                            'access_token': access_token.decode()
                        }
                        return make_response(jsonify(response)), 200
                response = {'message': 'Invalid email or password'}
                return make_response(jsonify(response)), 401
            except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 500
        response = {'message': 'This user does not exist. Please register'}
        return make_response(jsonify(response)), 401


@v1.route('/reset-password', methods=['POST'])
def reset_password():
    """This view handles user login and access token generation."""
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    if access_token:
        email = user.decode_token(access_token)
        if email in USERS.keys():
            data = request.get_json()
            old_pass = data.get('old_password')
            new_pass = data.get('password')
            try:
                if user.reset_password(email, old_pass, new_pass):
                    response = {'message': 'password_reset successfull'}
                    return make_response(jsonify(response)), 201
            except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 500
    response = {'message': 'Login in to continue'}
    return make_response(jsonify(response)), 401

@v1.route('/businesses', methods=['POST', 'GET'])
def businesses():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    if access_token:
        email = user.decode_token(access_token)
        if request.method == 'POST':
            if email in USERS.keys():
                data = request.get_json()
                businessId = data.get('businessId')
                businessName = data.get('businessName')
                category = data.get('category')
                location = data.get('location')
                created_by = email
                try:
                    created_biz = Business(businessId, businessName, category, location, created_by)
                    business.append(created_biz)
                    for ids in business:
                        bizId = ids.businessId
                    response = {
                        'message': 'business created successfully',
                        'business': bizId
                    }
                    return make_response(jsonify(response)), 201
                except Exception as e:
                    response = {'message': str(e)}
                    return make_response(jsonify(response)), 401
        response = { 'business': business}
        return make_response(jsonify(response)), 200
    response = {'message': 'Login in to continue'}
    return make_response(jsonify(response)), 401
