import unittest
import json
from app import create_app


class AuthTestCase(unittest.TestCase):
    """Test case for the user creation and login"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.review = {'name': 'A very awesome review'}
        self.business = {
            'businessName': 'EABL',
            'category': 'Gumba',
            'location': 'Nairobi'
        }
    
    def register_user(self, email="review@test.com", username="stephen", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {'email': email, 'username': username, 'password': password}
        return self.client().post(
                '/api/v1/register',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def login_user(self, email="review@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {'email': email, 'password': password}
        return self.client().post(
                '/api/v1/login',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def test_review_creation(self):
        """Test the API can create a review (POST request)"""
        self.register_user()
        res = self.login_user()
        access_token = json.loads(res.data.decode())['access_token']
        res2 = self.client().post(
            '/api/v1/businesses',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(self.business)
        )
        bizIds = json.loads(res2.data.decode())['business']
        res3 = self.client().get(
            '/api/v1/businesses/{}'.format(bizIds[0]),
            headers={'Authorization': 'Bearer ' + access_token}
        )
        self.assertEqual(res3.status_code, 200)
        res3 = self.client().get(
            '/api/v1/businesses/{}/reviews'.format(bizIds[0]),
            headers={'Authorization': 'Bearer ' + access_token}
        )
        reviews = json.loads(res3.data.decode())['reviews']
        self.assertEqual(res.status_code, 201)
        self.assertIn('A very awesome review', reviews)