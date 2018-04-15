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
        self.register_business(self.business_data)
        res = self.client.get('/api/v1/businesses/5/reviews')
        result = json.loads(res.data.decode())
        self.assertTrue(result['businesses'])