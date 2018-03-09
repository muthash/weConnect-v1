import os
import random
from app.v1 import v1

from flask import Blueprint, make_response, request, abort, jsonify, json
from flask_bcrypt import Bcrypt
from app.v1.user import User
from app.v1 import validate as val
from app.v1.business import Business

users = []
bizneses = []


@v1.route('/register', methods=['GET', 'POST'])
def register():
    """This route registers a new user."""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        if val.check_email(email):
            emails = [user.email for user in users]
            if email not in emails:
                try:
                    created_user = User(email, username, password)
                    users.append(created_user)
                    response = {'message': 'You registered successfully'}
                    return jsonify(response), 201
                except Exception as e:
                    response = {'message': str(e)}
                    return make_response(response)
            response = {'message': 'User already exists. Please login'}
            return jsonify(response), 202
        response = {'message': 'Invalid Email'}
        return jsonify(response), 403
    response = {'message': 'Invalid HTTP request. Make a Post request'}
    return jsonify(response), 403


@v1.route('/login', methods=['GET', 'POST'])
def login():
    """This route  logs in a user."""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        credentials = {user.email: user.password for user in users}
        if email in credentials.keys():
            try:
                encrypted_password = credentials[email]
                if Bcrypt().check_password_hash(encrypted_password, password):
                    access_token = User.generate_token(email)
                    if access_token:
                        response = {
                            'message': 'Login successfull',
                            'access_token': access_token.decode()
                        }
                        return jsonify(response), 200
                response = {'message': 'Invalid email or password'}
                return jsonify(response), 401
            except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 500
        response = {'message': 'User does not exist. Proceed to register'}
        return jsonify(response), 401
    response = {'message': 'Invalid HTTP request. Make a Post request'}
    return jsonify(response), 403


@v1.route('/reset-password', methods=['POST'])
def reset_password():
    """Handles password reset"""
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    if access_token:
        email = User.decode_token(access_token)
        credentials = {user.email: user.username for user in users}
        if email in credentials.keys():
            data = request.get_json()
            new_pass = Bcrypt().generate_password_hash(
                                data.get('new_password')).decode()
            try:
                for user in users:
                    if user.email == email:
                        user.password = new_pass
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
        email = User.decode_token(access_token)
        credentials = {user.email: user.username for user in users}
        if request.method == 'POST':
            if email in credentials.keys():
                data = request.get_json()
                businessId = random.randint(1, 10000)
                businessName = data.get('businessName')
                category = data.get('category')
                location = data.get('location')
                created_by = email
                try:
                    if val.check_name(businessName):
                        bizneses.append(Business(businessId, businessName,
                                                 category, location,
                                                 created_by))
                        businessNames = [biz.businessName for biz in bizneses]
                        businessIds = [biz.businessId for biz in bizneses]
                        response = {
                            'message': 'business created successfully',
                            'business': businessNames,
                            'id': businessIds
                        }
                        return make_response(jsonify(response)), 201
                    response = {'message': 'Invalid business name input'}
                    return make_response(jsonify(response)), 401
                except Exception as e:
                    response = {'message': str(e)}
                    return make_response(jsonify(response)), 401
            response = {'message': 'Register to continue'}
            return make_response(jsonify(response)), 401
        for biz in bizneses:
            obj = [{
                'id': biz.businessId,
                'name': biz.businessName,
                'categoty': biz.category,
                'location': biz.location,
                'created_by': biz.created_by
            }]
        response = {'business': obj}
        return make_response(jsonify(response)), 200
    response = {'message': 'Login in to continue'}
    return make_response(jsonify(response)), 401


@v1.route('/businesses/<int:bizid>', methods=['GET', 'PUT', 'DELETE'])
def businesses_manipulation(bizid):
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    if access_token:
        email = User.decode_token(access_token)
        credentials = {user.email: user.username for user in users}
        if email in credentials.keys():
            businessIds = [biz.businessId for biz in bizneses]
            if bizid not in businessIds:
                abort(404)
            if request.method == "DELETE":
                for biz in bizneses:
                    if biz.businessId == bizid and biz.created_by == email:
                        idx = bizneses.index(biz)
                        del bizneses[idx]
                        response = {"message": "business {} " +
                                    "deleted".format(bizid)}
                        return make_response(jsonify(response)), 200
            elif request.method == 'PUT':
                for biz in bizneses:
                    if biz.businessId == bizid and biz.created_by == email:
                        data = request.get_json()
                        businessName = data.get('businessName')
                        category = data.get('category')
                        location = data.get('location')
                        idx = bizneses.index(biz)
                        if val.check_name(businessName):
                            bizneses[idx] = (Business(bizid, businessName,
                                             category, location, email))
                            update = bizneses[idx]
                            obj = {
                                'id': update.businessId,
                                'name': update.businessName,
                                'category': update.category,
                                'location': update.location,
                                'created_by': update.created_by
                            }
                            response = {'business': obj}
                            return make_response(jsonify(response)), 200
                        response = {'message': 'Invalid business name input'}
                        return make_response(jsonify(response)), 401
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
        response = {'message': 'Register to continue'}
        return make_response(jsonify(response)), 401
    response = {'message': 'Login in to continue'}
    return make_response(jsonify(response)), 401


@v1.route('/businesses/<int:bizid>/reviews', methods=['POST', 'GET'])
def reviews(bizid):
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    if access_token:
        email = User.decode_token(access_token)
        credentials = {user.email: user.username for user in users}
        if email in credentials.keys():
            if request.method == 'POST':
                data = request.get_json()
                review = data.get('name')
                if val.check_name(review):
                    try:
                        for biz in bizneses:
                            if(biz.businessId == bizid and
                               biz.created_by != email):
                                biz.reviews.append(review)
                                idx = bizneses.index(biz)
                                obj = bizneses[idx]
                        response = {
                            'message': 'review created successfully',
                            'reviews': obj.reviews
                        }
                        return make_response(jsonify(response)), 201
                    except Exception as e:
                        response = {'message': str(e)}
                        return make_response(jsonify(response)), 403
                response = {'message': 'Invalid review name input'}
                return make_response(jsonify(response)), 401
            for biz in bizneses:
                if biz.businessId == bizid:
                    obj = biz.reviews
            response = {'reviews': obj}
            return make_response(jsonify(response)), 200
        response = {'message': 'Register to continue'}
        return make_response(jsonify(response)), 401
    response = {'message': 'Login to continue'}
    return make_response(jsonify(response)), 401
