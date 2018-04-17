"""
Base Test case with setup and methods that other
test classes inherit
"""
import unittest
import json
from app import create_app
from app.auth.views import users
from app.business.views import store


class BaseTestCase(unittest.TestCase):
    """Base Test Case"""
    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.header = {'Content-Type': 'application/json'}
        self.user_data = {'email': 'user@test.com', 'username': 'stephen',
                          'password': 'test1234'}
        self.reset_user = {'email': 'reset@test.com', 'username': 'muthama',
                          'password': 'test1234'}
        self.invalid_email = {'email': 'user', 'username': 'stephen',
                              'password': 'test1234'}
        self.login_data = {'email': 'user@test.com', 'password': 'test1234'}
        self.unregisterd = {'email': 'notuser@me.com', 'password': 'test1234'}
        self.incorrect_pass = {'email': 'user@test.com', 'password': 'test123'}
        self.missing_pass = {'email': 'user@test.com'}
        self.passwords = {'old_password': "test1234", 'new_password': "newtestpass"}
        self.invalid_pass = {'old_password': "test123", 'new_password': "newpass"}
        self.null_pass = {'old_password': "    ", 'new_password': "newpass"}
        self.business_data = {'name': 'KTDA', 'category': 'Farming', 'location': 'Narok'}
        self.update_data = {'name':'ABCD', 'category':'Farming', 'location':'Narok'}
        self.review_data = {'review': 'KTDA services are the best'}
        self.url = None
        self.reg_res = self.make_request('/api/v1/register', data=self.user_data)
        self.make_request('/api/v1/register', data=self.reset_user)

    def make_request(self, url, method='post', **kwargs):
        """Make a request to the given url with the given method"""
        self.url = str(url)
        data = json.dumps(kwargs['data'])
        if method == 'put':
            return self.client.put(path=self.url,
                                   headers=self.header, data=data)
        elif method == 'delete':
            return self.client.delete(path=self.url,
                                      headers=self.header, data=data)
        return self.client.post(path=self.url, headers=self.header, data=data)

    def get_login_token(self):
        """Get the access token and add it to the header"""
        # self.make_request('/api/v1/register', data=self.user_data)
        login_res = self.make_request('/api/v1/login', data=self.login_data)
        result = json.loads(login_res.data.decode())
        self.header['Authorization'] = 'Bearer ' + result['access_token']
        return result

    def register_business(self, data):
        """Register a test business"""
        self.get_login_token()
        res = self.make_request('/api/v1/businesses', data=data)
        result = json.loads(res.data.decode())
        return result

    def register_review(self, data):
        """Register a test review for the registered business"""
        self.register_business(self.business_data)
        res = self.make_request('/api/v1/business/1/reviews',
                                data=data)
        result = json.loads(res.data.decode())
        return result

    def tearDown(self):
        """teardown all initialized variables"""
        users.clear()


if __name__ == "__main__":
    unittest.main()
