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
    
    def register_user(self, email="reviewer@test.com", username="stephen", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {'email': email, 'username': username, 'password': password}
        return self.client().post(
                '/api/v1/register',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def login_user(self, email="reviewer@test.com", password="test1234"):
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
        bizIds = json.loads(res2.data.decode())['id']
        
        self.register_user("reviewer2@test.com", "stephen", "test1234")
        res4 = self.login_user("reviewer2@test.com", "test1234")
        access_token = json.loads(res4.data.decode())['access_token']
        res3 = self.client().post(
            '/api/v1/businesses/{}/reviews'.format(bizIds[0]),
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(self.review)
        )
        reviews = json.loads(res3.data.decode())['reviews']
        self.assertEqual(res3.status_code, 201)
        self.assertIn('A very awesome review', reviews)

    def test_get_all_business_reviews(self):
        """Test the API can get all business reviews"""
        self.register_user("reviewer3@test.com", "stephen", "test1234")
        res = self.login_user("reviewer3@test.com", "test1234")
        access_token = json.loads(res.data.decode())['access_token']
        res2 = self.client().post(
            '/api/v1/businesses',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(self.business)
        )
        bizIds = json.loads(res2.data.decode())['id']
        self.register_user("reviewer4@test.com", "stephen", "test1234")
        res4 = self.login_user("reviewer4@test.com", "test1234")
        access_token = json.loads(res4.data.decode())['access_token']
        res3 = self.client().post(
            '/api/v1/businesses/{}/reviews'.format(bizIds[0]),
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + access_token},
            data=json.dumps(self.review)
        )
        res3 = self.client().get(
            '/api/v1/businesses/{}/reviews'.format(bizIds[0]),
            headers={'Authorization': 'Bearer ' + access_token}
        )
        biz = json.loads(res3.data.decode())['reviews']
        self.assertTrue(biz)
        self.assertEqual(res.status_code, 200)