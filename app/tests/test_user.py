import unittest
import json
from app import create_app
from app.v1.user import USERS


class AuthTestCase(unittest.TestCase):
    """Test case for the user creation and login"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'email': 'test@example.com',
            'username': 'stephen',
            'password': 'test_password',
            'cpassword': 'test_password'
        }
        self.header = {'Content-Type': 'application/json'}
        self.data = json.dumps(self.user_data)
        self.login_data = {
            'email': 'test@example.com',
            'password': 'test_password'
        }
        self.login_data = json.dumps(self.user_data)

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.client().post('/api/v1/register', headers=self.header, data=self.data)
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "You registered successfully")
        new_account = self.user_data['email'] in USERS.keys()
        self.assertTrue(new_account)

    def test_user_login(self):
        """Test registered user can login."""
        login_res = self.client().post('/api/v1/login', headers=self.header, data=self.login_data)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_unregistered_user_login(self):
        user_data = {
            'email': 'unreg@example.com',
            'password': 'password'
        }
        login_res = self.client().post('/api/v1/login', headers=self.header, data=json.dumps(user_data))
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "This user does not exist. Please register")
        self.assertEqual(login_res.status_code, 401)

    def test_wrong_password_login(self):
        """Test registered user tries to login with wrong password"""
        user_data = {
            'email': 'test@example.com',
            'password': 'password'
        }
        login_res = self.client().post('/api/v1/login', headers=self.header, data=json.dumps(user_data))
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "Invalid email or password")
        self.assertEqual(login_res.status_code, 401)
    
    def test_password_reset(self):
        self.client().post('/api/v1/register', headers=self.header, data=self.data)
        login_res = self.client().post('/api/v1/login',headers=self.header,data=self.login_data)
        access_token = json.loads(login_res.data.decode())['access_token']
        new_password = {
            'old_password': 'test_password',
            'password': 'password'
        }
        reset_res = self.client().post(
            '/api/v1/reset-password',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(new_password))
        result = json.loads(reset_res.data.decode())
        self.assertEqual(result['message'], "password_reset successfull")
        self.assertEqual(reset_res.status_code, 201)
