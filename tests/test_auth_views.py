"""Test case for the user"""
import json
from tests.base_test_file import BaseTestCase


class TestRegisterUser(BaseTestCase):
    """Test for Register User endpoint"""
    def register(self, msg, code):
        self.make_test('/api/v1/register', data=self.reg_data, code=code,
                       msg=msg)

    def test_registration(self):
        """Test user registration works correcty"""
        result = json.loads(self.reg_res.data.decode())
        self.assertEqual(result['message'], "Account created successfully")
        self.assertEqual(self.reg_res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
        self.register(msg="User already exists. Please login", code=409)

    def test_register_invalid_email(self):
        """Test user registration with an invalid email address"""
        self.reg_data['email'] = 'invalid'
        self.register(msg="The email address is not valid." +
                      " It must have exactly one @-sign.", code=400)

    def test_register_missing_password(self):
        """Test user registration with an missing password"""
        del self.reg_data['password']
        self.register(msg=['The password should not be missing'], code=400)

    def test_valid_json_request(self):
        """Test register request is json format"""
        self.make_test('/api/v1/register', jsons=False, data=self.reg_data)


class TestLoginUser(BaseTestCase):
    """Test for Login User endpoint"""
    def login(self, msg, code):
        self.make_test('/api/v1/login', data=self.reg_data, code=code, msg=msg)

    def test_user_login(self):
        """Test registered user can login"""
        self.login(code=200, msg='Login successfull. Welcome stephen')

    def test_short_password(self):
        """Test login with short password length"""
        self.reg_data['password'] = 'short'
        self.login(code=400,
                   msg=['Password should be atleast 8 characters'])

    def test_unregistered_user_login(self):
        """Test unregistered user cannot login"""
        self.reg_data['email'] = 'unreg@test.com'
        self.login(code=401, msg='Invalid email or password')

    def test_incorrect_password_login(self):
        """Test incorrect password cannot login"""
        self.reg_data['password'] = 'incorrect'
        self.login(code=401, msg='Invalid email or password')

    def test_login_missing_email(self):
        """Test user login with missing email"""
        del self.reg_data['email']
        self.login(code=400, msg=['The email should not be missing'])

    def test_valid_json_request(self):
        """Test login request is json format"""
        self.make_test('/api/v1/login', jsons=False, data=self.reg_data)


class TestLogoutUser(BaseTestCase):
    """Test for Logout User endpoint"""
    def test_logout_user(self):
        """Test if logged in user can logout"""
        self.make_test('/api/v1/logout', data=None, code=200,
                       msg='Successfully logged out')


class TestResetPassword(BaseTestCase):
    """Test reset password user endpoint"""
    def reset_password(self, code, msg, data):
        self.make_test('/api/v1/reset-password', data=data,  code=code,
                       msg=msg)

    def test_password_reset(self):
        """Test password reset works as expected"""
        data = dict(email=self.reg_data['email'])
        self.reset_password(data=data, code=201,
                            msg='Password reset successfull.' +
                            ' Check your email for your new password')

    def test_not_user_reset(self):
        """Test reset password with a non existing account"""
        data = {'email': 'non_reg@gmail.com'}
        self.reset_password(data=data, code=401,
                            msg='Email address not registered')

    def test_reset_null_email(self):
        """Test reset password with a missing email address"""
        self.reset_password(data={}, code=400,
                            msg=['The email should not be missing'])

    def test_valid_json_request(self):
        """Test reset password request is json format"""
        self.make_test('/api/v1/reset-password', jsons=False,
                       data=self.reg_data['email'])


class TestChangetPassword(BaseTestCase):
    """Test change password user endpoint"""
    def change_password(self, msg, code):
        self.make_test('/api/v1/change-password', data=self.passwords,
                       code=code, method='put', msg=msg)

    def test_password_change(self):
        """Test password change works as expected"""
        self.change_password(code=201, msg='Password change successfull' +
                                           ' Login to continue')

    def test_incorrect_initial_password(self):
        """Test password with incorrect old password input"""
        self.passwords['old_password'] = 'incorrect'
        self.change_password(code=401, msg='The initial password' +
                                           ' is not correct')

    def test_empty_initial_password(self):
        """Test password with invalid old password input"""
        self.passwords['old_password'] = '  '
        self.change_password(code=400, msg=['The old_password should' +
                                            ' not be empty'])

    def test_unregistered_user(self):
        """Test password change for unregistered user"""
        with self.app.app_context():
            access_token = self.token
            self.header['Authorization'] = 'Bearer ' + access_token
            self.change_password(code=401, msg='The user is not registered')

    def test_valid_json_request(self):
        """Test change password request is json format"""
        self.make_test('/api/v1/change-password', data=self.passwords,
                       jsons=False, method='put')
