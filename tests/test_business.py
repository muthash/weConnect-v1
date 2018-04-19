"""Test case for business manipulation view"""
import json
import datetime
from flask_jwt_extended import create_access_token
from app.business.views import store
from app.models import Business
from tests.test_base import BaseTestCase


class TestPostBusiness(BaseTestCase):
    """Test for post business endpoint"""
    def test_business_creation(self):
        """Test create business works correcty"""
        result = self.register_business(self.business_data)
        self.assertEqual(result['message'], "Business with name KTDA created")

    def test_missing_data(self):
        """Test create business with an empty data"""
        result = self.register_business(self.review_data)
        self.assertTrue(result['message'])
    
    def test_valid_json_request(self):
        """Test create business request is json format"""
        self.get_login_token()
        del self.header['Content-Type']
        change_res = self.make_request('/api/v1/businesses', data=self.business_data)
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')

    def test_missing_user(self):
        """Test create business for unregistered user"""
        with self.app.app_context():
            access_token = create_access_token(identity=2, expires_delta=datetime.timedelta(minutes=5))
            self.header['Authorization'] = 'Bearer ' + access_token
            res = self.make_request('/api/v1/businesses', data=self.business_data)
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], "Please login to continue")


class TestPutBusiness(BaseTestCase):
    """Test for editing business endpoint"""
    def test_business_can_be_edited(self):
        """Test edit an existing business works as expected"""
        self.get_login_token()
        res = self.make_request('/api/v1/businesses/15', data=self.update_data, method='put')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Business updated successfully")

    def test_null_edit_data(self):
        """Test edit business with null input"""
        self.get_login_token()
        res = self.make_request('/api/v1/businesses/1', data=self.review_data, method='put')
        result = json.loads(res.data.decode())
        self.assertTrue(result['message'])

    def test_non_existing_business(self):
        """Test edit business that is not available"""
        self.get_login_token()
        res = self.make_request('/api/v1/businesses/2', data=self.business_data, method='put')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'The business 2 is not available')

    def test_forbidden_business(self):
        """Test edit business that user did not create"""
        with self.app.app_context():
            access_token = create_access_token(identity=2, expires_delta=datetime.timedelta(minutes=5))
            self.header['Authorization'] = 'Bearer ' + access_token
            res = self.make_request('/api/v1/businesses/15', data=self.business_data, method='put')
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], 'The operation is forbidden for this business')

    def test_valid_json_request(self):
        """Test edit business request is json format"""
        self.get_login_token()
        del self.header['Content-Type']
        change_res = self.make_request('/api/v1/businesses/1', data=self.business_data, method='put')
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')


class TestDeleteBusiness(BaseTestCase):
    """Test for delete business endpoint"""
    def test_business_can_be_deleted(self):
        """Test delete an existing business"""
        self.register_business(self.business_data)
        res = self.make_request('/api/v1/businesses/2', data={'password':'test1234'}, method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Business 2 deleted')

    def test_null_password(self):
        """Test delete with null password"""
        self.get_login_token()
        res = self.make_request('/api/v1/businesses/2', data={}, method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], ['Please enter your password'])

    def test_not_user(self):
        """Test delete by unregistered user"""
        with self.app.app_context():
            access_token = create_access_token(identity=2, expires_delta=datetime.timedelta(minutes=5))
            self.header['Authorization'] = 'Bearer ' + access_token
            res = self.make_request('/api/v1/businesses/2', data={'password':'test1234'}, method='delete')
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], 'Please login to continue')

    def test_incorrect_password(self):
        """Test delete with incorrect password"""
        self.get_login_token()
        res = self.make_request('/api/v1/businesses/1', data={'password':'test123'}, method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Enter correct password to delete')

    def test_not_exist_business(self):
        """Test delete non existing business"""
        self.get_login_token()
        res = self.make_request('/api/v1/businesses/100', data={'password':'test1234'}, method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'The business 100 is not available')

    def test_delete_another_user_business(self):
        """Test delete a business that user did not create"""
        with self.app.app_context():
            business = Business(**self.business_data, created_by='m@m.com')
            store.append(business)
            self.get_login_token()
            res = self.make_request('/api/v1/businesses/4', data={'password':'test1234'}, method='delete')
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], 'The operation is forbidden for this business')

    def test_valid_json_request(self):
        """Test delete business request is json format"""
        self.get_login_token()
        del self.header['Content-Type']
        change_res = self.make_request('/api/v1/businesses/1', data={'password':'test1234'}, method='delete')
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], 'The Request should be JSON format')


class TestGetBusiness(BaseTestCase):
    """Test for get business endpoint"""
    def test_all_businesses(self):
        """Test get all registered businesses"""
        self.register_business(self.business_data)
        res = self.client.get('/api/v1/businesses')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "The following businesss are registered")
        self.assertTrue(result['businesses'])

    def test_empty_businesses(self):
        """Test get all with no registered businesses"""
        with self.app.app_context():
            store.clear()
            res = self.client.get('/api/v1/businesses')
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], "There are no businesses registered currently")

    def test_business_id(self):
        """Test get single business"""
        self.register_business(self.business_data)
        res = self.client.get('/api/v1/businesses/4')
        result = json.loads(res.data.decode())
        self.assertTrue(result['businesses'])

    def test_invalid_business_id(self):
        """Test get not available single business"""
        self.register_business(self.business_data)
        res = self.client.get('/api/v1/businesses/20')
        result = json.loads(res.data.decode())
        self.assertTrue(result['message'], 'The business 20 is not available')
