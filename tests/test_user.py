"""Test case for the user"""
import json
import datetime
from flask_jwt_extended import create_access_token
from tests.test_base import BaseTestCase


class TestRegisterUser(BaseTestCase):
    """Test for Register User endpoint"""
    def test_registration(self):
        """Test user registration works correcty"""
        res = self.make_request('/api/v1/register', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Account created successfully")
        self.assertEqual(res.status_code, 201)
    
    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
        self.make_request('/api/v1/register', data=self.user_data)
        second_res = self.make_request('/api/v1/register', data=self.user_data)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists. Please login")
        self.assertEqual(second_res.status_code, 409)
    
    def test_register_invalid_email(self):
        """Test user registration with an invalid email address"""
        res = self.make_request('/api/v1/register', data=self.invalid_email)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "The email address is not valid."+
                                            " It must have exactly one @-sign.")
        self.assertEqual(res.status_code, 400)

    def test_register_empty_username(self):
        """Test user registration with an empty username"""
        res = self.make_request('/api/v1/register', data=self.login_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], ['Please enter your username'])
        self.assertEqual(res.status_code, 400)

    def test_valid_json_request(self):
        """Test register request is json format"""
        self.header = {}
        res = self.make_request('/api/v1/register', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')
        self.assertEqual(res.status_code, 400)

    def test_valid_request_method(self):
        """Test another request method apart from post"""
        self.header = {}
        res = self.make_request('/api/v1/register', method="put", data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['error'], 'The HTTP request Method is not allowed')
        self.assertEqual(res.status_code, 405)