"""Test case for business manipulation view"""
import json
import datetime
from flask_jwt_extended import create_access_token
from tests.test_base import BaseTestCase


class TestPostBusiness(BaseTestCase):
    """Test for post business endpoint"""
    def test_business_creation(self):
        """Test user registration works correcty"""
        result = self.register_business(self.business_data)
        self.assertEqual(result['message'], "Business with name KTDA created")

    def test_missing_data(self):
        """Test business creation with an empty data"""
        result = self.register_business(self.review_data)
        self.assertTrue(result['message'])
    
    def test_valid_json_request(self):
        """Test post business request is json format"""
        self.get_login_token()
        del self.header['Content-Type']
        change_res = self.make_request('/api/v1/businesses', data=self.business_data)
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')

    def test_missing_user(self):
        """Test business for unregistered user"""
        with self.app.app_context():
            access_token = create_access_token(identity=2, expires_delta=datetime.timedelta(minutes=5))
            self.header['Authorization'] = 'Bearer ' + access_token
            res = self.make_request('/api/v1/businesses', data=self.business_data)
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], "Please login to continue")