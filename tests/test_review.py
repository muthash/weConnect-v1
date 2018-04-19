"""Test case for business manipulation view"""
import json
import datetime
from flask_jwt_extended import create_access_token
from app.business.views import store
from app.models import Business
from tests.test_base import BaseTestCase


class TestGetReview(BaseTestCase):
    """Test for get reviews endpoint"""
    def test_get_businesses(self):
        """Test get all reviews for a business"""
        res = self.client.get('/api/v1/businesses/20/reviews')
        result = json.loads(res.data.decode())
        self.assertTrue(result['businesses'])


class TestPostReview(BaseTestCase):
    """Test for post review endpoint"""
    def test_review_creation(self):
        """Test create review works correcty"""
        self.make_request('/api/v1/register', data=self.review_user)
        self.get_login_token(self.login_reviewer)
        res = self.make_request('/api/v1/businesses/25/reviews',
                                data=self.review_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Review for business 25 created")

    def test_review_own_business(self):
        """Test create review by business owner"""
        self.get_login_token(self.user_data)
        res = self.make_request('/api/v1/businesses/25/reviews',
                                data=self.review_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "The operation is forbidden for own business")

    def test_review_not_available_business(self):
        """Test create review for non existing business"""
        self.get_login_token(self.user_data)
        res = self.make_request('/api/v1/businesses/100/reviews',
                                data=self.review_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "The business 100 is not available")

    def test_null_data(self):
        """Test create review with null data"""
        self.make_request('/api/v1/register', data=self.review_user)
        self.get_login_token(self.login_reviewer)
        result = self.register_review(data={})
        self.assertEqual(result['message'], ['Please enter your review'])

    def test_valid_json_request(self):
        """Test create review request is json format"""
        self.get_login_token(self.user_data)
        del self.header['Content-Type']
        result = self.register_review(self.review_data)
        self.assertEqual(result['message'], 'The Request should be JSON format')