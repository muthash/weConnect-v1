"""Test case for business manipulation view"""
import json
import datetime
from flask_jwt_extended import create_access_token
from app.business.views import store
from app.models import Business
from tests.base_test_file import BaseTestCase


class TestPostBusiness(BaseTestCase):
    """Test for post business endpoint"""
    def register_business(self, msg, code):
        self.make_test('/api/v1/businesses', data=self.business_data,
                       code=code, msg=msg)

    def test_business_creation(self):
        """Test create business works correcty"""
        result = json.loads(self.biz_res.data.decode())
        self.assertEqual(result['message'], "Business with name Andela created")
        self.assertEqual(self.biz_res.status_code, 201)

    def test_empty_name(self):
        """Test create business with space as name"""
        self.business_data['name'] = '   '
        self.register_business(code=400, msg=['The name should not be empty'])

    def test_already_registered_name(self):
        """Test create business with already registered name"""
        self.register_business(code=409, msg='Business with name Andela already exists')

    def test_not_registered_user(self):
        """Test create business for unregistered user"""
        with self.app.app_context():
            access_token = self.token
            self.header['Authorization'] = 'Bearer ' + access_token
            self.register_business(code=401, msg='Login in to register business')

    def test_valid_json_request(self):
        """Test create business request is json format"""
        self.make_test('/api/v1/businesses', jsons=False, data=self.business_data)

class TestPutBusiness(BaseTestCase):
    """Test for editing business endpoint"""
    def edit_business(self, msg, code):
        self.business_data['name'] = 'iHub'
        self.make_test('/api/v1/businesses/1', data=self.business_data,
                       method='put', code=code, msg=msg)

    def test_business_can_be_edited(self):
        """Test edit an existing business works as expected"""
        self.edit_business(code=200, msg='Business updated successfully')

    def test_missing_edit_data(self):
        """Test edit business with missing input"""
        del self.business_data['category']
        self.edit_business(code=400, msg=['The category should not be missing'])

    def test_non_existing_business(self):
        """Test edit business that is not available"""
        self.make_test('/api/v1/businesses/2', data=self.business_data, method='put',
                       code=404, msg='The business with id 2 is not available')

    def test_forbidden_business(self):
        """Test edit business that user did not create"""
        with self.app.app_context():
            access_token = self.token
            self.header['Authorization'] = 'Bearer ' + access_token
            self.edit_business(code=403, msg='The operation is forbidden for this business')

    def test_valid_json_request(self):
        """Test edit business request is json format"""
        self.make_test('/api/v1/businesses/1', jsons=False, method='put',
                       data=self.business_data)


class TestDeleteBusiness(BaseTestCase):
    """Test for delete business endpoint"""
    def delete_business(self, msg, code):
        self.make_test('/api/v1/businesses/1', data=self.password,
                       method='delete', code=code, msg=msg)

    def test_business_can_be_deleted(self):
        """Test delete an existing business"""
        self.delete_business(code=200, msg='Business with id 1 deleted')

    def test_missing_password(self):
        """Test delete with missing password"""
        self.password={}
        self.delete_business(code=400, msg=['The password should not be missing'])

    def test_incorrect_password(self):
        """Test delete with incorrect password"""
        self.password={'password':'Test12345'}
        self.delete_business(code=401, msg='Enter correct password to delete')

    def test_delete_another_user_business(self):
        """Test delete a business that user did not create"""
        with self.app.app_context():
            self.reg_data['email'] = 'anotheruser@test.com'
            self.make_request('/api/v1/register', 'post', data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.delete_business(code=403, 
                                 msg='The operation is forbidden for this business')

    def test_not_user(self):
        """Test delete by unregistered user"""
        with self.app.app_context():
            access_token = self.token
            self.header['Authorization'] = 'Bearer ' + access_token
            self.delete_business(code=401, msg='Please login to delete business')

    def test_not_exist_business(self):
        """Test delete non existing business"""
        self.make_test('/api/v1/businesses/10', data=self.password,
                       method='delete', code=404,
                       msg='The business with id 10 is not available')

    def test_valid_json_request(self):
        """Test delete business request is json format"""
        self.make_test('/api/v1/businesses/1', jsons=False, method='delete',
                       data=self.password)


class TestGetBusiness(BaseTestCase):
    """Test for get business endpoint"""
    def get_business(self, url):
        res = self.client.get(path=url)
        return json.loads(res.data.decode())

    def test_all_businesses(self):
        """Test get all registered businesses"""
        result = self.get_business('/api/v1/businesses')
        self.assertTrue(result['businesses'])

    def test_empty_businesses(self):
        """Test get all with no registered businesses"""
        with self.app.app_context():
            store.clear()
            result = self.get_business('/api/v1/businesses')
            self.assertEqual(result['message'],
                             "There are no businesses registered currently")
    
    def test_filter_businesses_by_category(self):
        """Test get all registered businesses in a category"""
        result = self.get_business('/api/v1/businesses?category=IT')
        self.assertTrue(result['businesses'])

    def test_not_found_category(self):
        """Test filter not available category"""
        result = self.get_business('/api/v1/businesses?category=Farming')
        self.assertEqual(result['message'],
                         'There are no businesses registered in Farming category')

    def test_business_id(self):
        """Test get single business"""
        result = self.get_business('/api/v1/businesses/1')
        self.assertTrue(result['businesses'])

    def test_invalid_business_id(self):
        """Test get not available single business"""
        result = self.get_business('/api/v1/businesses/10')
        self.assertTrue(result['message'], 'The business 10 is not available')


class TestGetReview(BaseTestCase):
    """Test for get reviews endpoint"""
    def test_get_businesses(self):
        """Test get all reviews for a business"""
        res = self.client.get('/api/v1/businesses/1/reviews')
        result = json.loads(res.data.decode())
        self.assertTrue(result['businesses'])


class TestPostReview(BaseTestCase):
    """Test for post review endpoint"""
    def create_review(self, msg, code):
        self.make_test('/api/v1/businesses/1/reviews', data=self.review_data,
                       code=code, msg=msg)

    def test_review_creation(self):
        """Test create review works correcty"""
        with self.app.app_context():
            self.reg_data['email'] = 'anotheruser@test.com'
            self.make_request('/api/v1/register', 'post', data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.create_review(code=201, 
                               msg='Review for business with id 1 created')

    def test_review_own_business(self):
        """Test create review by business owner"""
        self.create_review(code=403, 
                           msg='The operation is forbidden for own business')

    def test_review_not_available_business(self):
        """Test create review for non existing business"""
        self.make_test('/api/v1/businesses/10/reviews', data=self.review_data,
                       code=404, msg='The business with id 10 is not available')

    def test_null_data(self):
        """Test create review with null data"""
        self.review_data = {}
        self.create_review(code=400, msg=['The review should not be missing'])

    def test_valid_json_request(self):
        """Test create review request is json format"""
        self.make_test('/api/v1/businesses/1/reviews', jsons=False, data=self.review_data)
