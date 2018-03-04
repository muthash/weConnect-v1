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