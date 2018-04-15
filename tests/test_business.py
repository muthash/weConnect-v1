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


class TestPutBusiness(BaseTestCase):
    """Test for editing business endpoint"""
    def test_business_can_be_edited(self):
        """Test API can edit an existing business"""
        self.register_business(self.business_data)
        res = self.make_request('/api/v1/businesses/2', data=self.update_data, method='put')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Business updated successfully")

    def test_null_edit_data(self):
        """Test edit business with null input"""
        self.register_business(self.business_data)
        res = self.make_request('/api/v1/businesses/1', data=self.review_data, method='put')
        result = json.loads(res.data.decode())
        self.assertTrue(result['message'])

    def test_non_existing_business(self):
        """Test edit business that is not available"""
        self.register_business(self.business_data)
        res = self.make_request('/api/v1/businesses/10', data=self.business_data, method='put')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'The business 10 is not available')

    def test_forbidden_business(self):
        """Test edit business that user did not create"""
        with self.app.app_context():
            self.register_business(self.business_data)
            access_token = create_access_token(identity=2, expires_delta=datetime.timedelta(minutes=5))
            self.header['Authorization'] = 'Bearer ' + access_token
            res = self.make_request('/api/v1/businesses/3', data=self.business_data, method='put')
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], 'The operation is forbidden for this business')

    def test_valid_json_request(self):
        """Test post business request is json format"""
        self.get_login_token()
        del self.header['Content-Type']
        change_res = self.make_request('/api/v1/businesses/1', data=self.business_data, method='put')
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')