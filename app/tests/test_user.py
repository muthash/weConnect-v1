import unittest
import json
from app import create_app


class AuthTestCase(unittest.TestCase):
    """Test case for the user creation and login"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
    
    def register_user(self, email="user@test.com", username="stephen", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {'email': email, 'username': username, 'password': password}
        return self.client().post(
                '/api/v1/register',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {'email': email, 'password': password}
        return self.client().post(
                '/api/v1/login',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.register_user()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "You registered successfully")
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        self.register_user("steve@test.com", "stephen", "test1234")
        second_res = self.register_user("steve@test.com", "stephen", "test1234")
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists." + "Please login")
        self.assertEqual(second_res.status_code, 202)

    def test_user_login(self):
        """Test registered user can login."""
        login_res = self.login_user()
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_unregistered_user_login(self):
        """Test unregistered user cannot login."""
        login_res = self.login_user('muthama@gmail.com', 'mypassword')
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "This user does not exist. Please register")
        self.assertEqual(login_res.status_code, 401)

    def test_incorrect_password_login(self):
        """Test registered user tries to login with incorrect password"""
        self.register_user("steve@test.com", "stephen", "test1234")
        login_res =  self.login_user('steve@test.com', 'test123')
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "Invalid email or password")
        self.assertEqual(login_res.status_code, 401)
    
    def test_password_reset(self):
        self.register_user("reset@test.com", "stephen", "test1234")
        login_res =  self.login_user("reset@test.com", "test1234")
        access_token = json.loads(login_res.data.decode())['access_token']
        new_password = {
            'old_password': 'test1234',
            'password': 'test12345'
        }
        reset_res = self.client().post(
            '/api/v1/reset-password',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(new_password))
        result = json.loads(reset_res.data.decode())
        self.assertEqual(result['message'], "password_reset successfull")
        self.assertEqual(reset_res.status_code, 201)
