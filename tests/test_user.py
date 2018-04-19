"""Test case for the user"""
import json
import datetime
from flask_jwt_extended import create_access_token
from tests.test_base import BaseTestCase


class TestRegisterUser(BaseTestCase):
    """Test for Register User endpoint"""
    def test_registration(self):
        """Test user registration works correcty"""
        result = json.loads(self.reg_res.data.decode())
        self.assertEqual(result['message'], "Account created successfully")
        self.assertEqual(self.reg_res.status_code, 201)
    
    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
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
        result = self.get_login_token()
        self.assertEqual(result['message'], 'Login successfull. Welcome stephen')
        self.assertTrue(result['access_token'])
    
    def test_unregistered_user_login(self):
        """Test unregistered user cannot login"""
        res = self.make_request('/api/v1/login', data=self.unregisterd)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Invalid email or password")
        self.assertEqual(res.status_code, 401)

    def test_invalid_password_login(self):
        """Test invalid password cannot login"""
        res = self.make_request('/api/v1/login', data=self.incorrect_pass)
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


class TestResetPassword(BaseTestCase):
    """Test reset password user endpoint"""
    def test_password_reset(self):
        """Test password reset works as expected"""
        self.make_request('/api/v1/register', data=self.reset_user)
        reset_res = self.make_request('/api/v1/reset-password', data=dict(email='reset@test.com'))
        result = json.loads(reset_res.data.decode())
        self.assertEqual(result['message'], 'Password reset successfull'+
                                            ' Check your email for your new password')
        self.assertEqual(reset_res.status_code, 201)

    def test_valid_json_request(self):
        """Test reset password request is json format"""
        self.header = {}
        res = self.make_request('/api/v1/reset-password', data=dict(email='user@test.com'))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')
        self.assertEqual(res.status_code, 400)

    def test_not_user_reset(self):
        """Test reset password with a non existing account"""
        reset_res = self.make_request('/api/v1/reset-password', data=dict(email='none@test.com'))
        result = json.loads(reset_res.data.decode())
        self.assertEqual(result['message'], "Email address not ragistered")
        self.assertEqual(reset_res.status_code, 401)

    def test_reset_null_email(self):
        """Test reset password with a missing email address"""
        reset_res = self.make_request('/api/v1/reset-password', data={})
        result = json.loads(reset_res.data.decode())
        self.assertEqual(result['message'], ['Please enter your email'])
        self.assertEqual(reset_res.status_code, 400)


class TestChangetPassword(BaseTestCase):
    """Test change password user endpoint"""
    def change_password(self, data):
        self.get_login_token()
        change_res = self.make_request('/api/v1/change-password', data=data, method='put')
        result = json.loads(change_res.data.decode())
        return result

    def test_password_change(self):
        """Test password change works as expected"""
        result = self.change_password(self.passwords)
        self.assertEqual(result['message'], "Password change successfull Login to continue")

    def test_incorrect_initial_password(self):
        """Test password with incorrect old password input"""
        result = self.change_password(self.invalid_pass)
        self.assertEqual(result['message'], "Enter correct initial password or reset password")

    def test_empty_initial_password(self):
        """Test password with incorrect old password input"""
        result = self.change_password(self.null_pass)
        self.assertEqual(result['message'], ['Please enter your old_password'])

    def test_missing_user(self):
        """Test password change for unregistered user"""
        with self.app.app_context():
            access_token = create_access_token(identity='na', expires_delta=datetime.timedelta(hours=1))
            self.header['Authorization'] = 'Bearer ' + access_token
            res = self.make_request('/api/v1/change-password', data=self.passwords, method='put')
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], "Please login to continue")

    def test_valid_json_request(self):
        """Test reset password request is json format"""
        self.get_login_token()
        del self.header['Content-Type']
        change_res = self.make_request('/api/v1/change-password', data=self.passwords, method='put')
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')