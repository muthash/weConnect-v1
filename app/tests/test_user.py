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

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.client().post('/api/v1/register', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "You registered successfully")
        self.assertEqual(res.status_code, 201)
        new_account = self.user_data['email'] in USERS.keys()
        self.assertTrue(new_account)
    
    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        user_data = {
            'email': 'reg@example.com',
            'username': 'stephen',
            'password': 'test_password',
            'cpassword': 'test_password'
        }
        res = self.client().post('/api/v1/register', data=user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/v1/register',
                                        data=user_data)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists." +
                         "Please login")
        self.assertEqual(second_res.status_code, 202)

    def test_user_login(self):
        """Test registered user can login."""
        self.user_data = {
            'email': 'steve@example.com',
            'username': 'stephen',
            'password': 'test_password',
            'cpassword': 'test_password'
        }
        res = self.client().post('/api/v1/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        user_data = {
            'email': 'steve@example.com',
            'password': 'test_password'
        }
        login_res = self.client().post('/api/v1/login', data=user_data)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully")
        self.assertEqual(login_res.status_code, 200)

    def test_unregistered_user_login(self):
        user_data = {
            'email': 'unreg@example.com',
            'password': 'password'
        }
        login_res = self.client().post('/api/v1/login', data=user_data)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "This user does not exist." +
                         " Please register")
        self.assertEqual(login_res.status_code, 401)

