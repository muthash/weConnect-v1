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

class TestLoginUser(BaseTestCase):
    """Test for Login User endpoint"""
    def test_user_login(self):
        """Test registered user can login"""
        self.make_request('/api/v1/register', data=self.user_data)
        res = self.make_request('/api/v1/login', data=self.login_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Login successfull. Welcome stephen')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(result['access_token'])
    
    def test_unregistered_user_login(self):
        """Test unregistered user cannot login"""
        res = self.make_request('/api/v1/login', data=self.login_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Invalid email or password")
        self.assertEqual(res.status_code, 401)

    def test_invalid_password_login(self):
        """Test invalid password cannot login"""
        self.make_request('/api/v1/register', data=self.user_data)
        res = self.make_request('/api/v1/login', data=self.invalid_pass)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Invalid email or password")
        self.assertEqual(res.status_code, 401)

    def test_valid_json_request(self):
        """Test login request is json format"""
        self.header = {}
        res = self.make_request('/api/v1/login', data=self.login_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')
        self.assertEqual(res.status_code, 400)

    def test_login_missing_field(self):
        """Test user login with missing field"""
        res = self.make_request('/api/v1/login', data=self.missing_pass)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], ['Please enter your password'])
        self.assertEqual(res.status_code, 400)


class TestLogoutUser(BaseTestCase):
    """Test for Logout User endpoint"""
    def test_logout_user(self):
        """Test if logged in user can logout"""
        self.get_login_token()
        logout_res = self.client.post('/api/v1/logout', headers=self.header)
        result = json.loads(logout_res.data.decode())
        self.assertEqual(result['message'], "Successfully logged out")
        self.assertEqual(logout_res.status_code, 200)

    def test_already_logout_user(self):
        """Test logout for aleady logged out user"""
        self.get_login_token()
        self.client.post('/api/v1/logout', headers=self.header)
        logout_res = self.client.post('/api/v1/logout', headers=self.header)
        result = json.loads(logout_res.data.decode())
        self.assertEqual(result['msg'], "Token has been revoked")
        self.assertEqual(logout_res.status_code, 401)