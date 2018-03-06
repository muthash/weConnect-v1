import os
from app.v1 import v1

from flask import Blueprint, make_response, request, abort, jsonify, json
from app.v1.user import User, USERS
from app.v1 import validate as val
from app.v1.business import Business

user = User()
bizneses = []

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
                businessId = len(bizneses) + 1
                businessName = data.get('businessName')
                category = data.get('category')
                location = data.get('location')
                created_by = email
                try:
                    bizneses.append(Business(businessId, businessName, category, location, created_by))
                    businessIds = [biz.businessId for biz in bizneses]
                    response = {
                        'message': 'business created successfully',
                        'business': businessIds
                    }
                    return make_response(jsonify(response)), 201
                except Exception as e:
                    response = {'message': str(e)}
                    return make_response(jsonify(response)), 401
        for biz in bizneses:
            obj = [{ 
                'id': biz.businessId,
                'name': biz.businessName,
                'categoty': biz.category,
                'location': biz.location,
                'created_by': biz.created_by
            }]
        response = { 'business': obj}
        return make_response(jsonify(response)), 200
    response = {'message': 'Login in to continue'}
    return make_response(jsonify(response)), 401

@v1.route('/businesses/<int:bizid>', methods=['GET', 'PUT', 'DELETE'])
def businesses_manipulation(bizid, **kwargs):
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    if access_token:
        email = user.decode_token(access_token)
        if email in USERS.keys():
            businessIds = [biz.businessId for biz in bizneses]
            if bizid not in businessIds:
                abort(404)
            if request.method == "DELETE":
                print("Delete")
            elif request.method == 'PUT':
                for biz in bizneses:
                    if biz.businessId == bizid and biz.created_by == email:
                        data = request.get_json()
                        businessName = data.get('businessName')
                        category = data.get('category')
                        location = data.get('location')
                        bizneses[bizid-1] = (Business(bizid, businessName, category, location, email))
                        update = bizneses[bizid-1]
                        obj = { 
                            'id': update.businessId,
                            'name': update.businessName,
                            'category': update.category,
                            'location': update.location,
                            'created_by': update.created_by
                        }
                        response = {'business': obj}
                        return make_response(jsonify(response)), 200
                    response = {'message': 'Forbidden'}
                    return make_response(jsonify(response)), 403
            else:
                for biz in bizneses:
                    if biz.businessId == bizid:
                        obj = { 
                            'id': biz.businessId,
                            'name': biz.businessName,
                            'category': biz.category,
                            'location': biz.location,
                            'created_by': biz.created_by
                        }
                response = {'business': obj}
                return make_response(jsonify(response)), 200
        response = {'message': 'Login in to continue'}
        return make_response(jsonify(response)), 401


