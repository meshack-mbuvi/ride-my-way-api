import json
import unittest

from application import create_app, db


class SignTests(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()

        self.userData = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "driver": True,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        self.data_with_unmatching_passwords = {
            "email": "meshmbuvi@gmail.com",
            "username": "mbuvi1",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi11"
        }
        self.data_with_invali_email = {
            "email": "meshmbuvi",
            "username": "mbuvi1",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        self.data_with_empty_password = {
            "email": "meshmbuvi@gmail.com",
            "username": "mbuvi",
            "driver": True,
            "password": "  ",
            "phone": "0719800509",
            "confirm password": "  "
        }

        self.data_with_short_password = {
            "email": "meshmbuvi@gmail.com",
            "username": "mbuvi",
            "driver": True,
            "password": "mfcf",
            "phone": "0719800509",
            "confirm password": "mfcf"
        }

        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.app = None
        self.db.drop_all()

    def test_user_can_sign_up(self):
        """test user can create an account."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.userData),
                                 content_type='application/json')

        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'],
                         'Account created.')

    def test_user_cannot_sign_up_with_unmatching_passwords(self):
        """test user cannot sign up with unmatching passwords."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(
                                     self.data_with_unmatching_passwords),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'Passwords do not match')

    def test_user_cannot_sign_up_with_invalid_email(self):
        """test user cannot sign up with invalid email."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.data_with_invali_email),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'Email is invalid')

    def test_user_cannot_sign_up_twice(self):
        """test user cannot sign up twice."""
        self.app.post('/api/v1/auth/signup',
                      data=json.dumps(self.userData),
                      content_type='application/json')
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.userData),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response_data['message'],
                         'User exists.')

    def test_user_cannot_sign_up_with_empty_passwords(self):
        """test user cannot sign up with empty fields."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(
                                     self.data_with_empty_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'Please ensure all fields are non-empty.')

    def test_password_cannot_be_less_than_six_characters(self):
        """test user cannot sign up with empty fields."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(
                                     self.data_with_short_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'password should be 6 characters or more.')


class LoginTests(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()
        self.db = db
        self.db.create_all()

        self.user_data = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "driver": True,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        # Register user
        self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json')
        self.valid_user = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "password": "mbuvi1"
        }
        self.invalid_password = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "password": "mbuvi1111"
        }
        self.login_with_email = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "password": "mbuvi1"
        }
        self.user_not_exist = {
            "email": "meshmbuvi@gmail.comdsghdfdhg",
            "username": "mutadbkjdhgksjdg",
            "password": "mbuvi1"
        }

        self.login_with_empty_password = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "password": ""
        }

    def tearDown(self):
        self.app = None
        self.db = db
        self.db.create_all()

    def test_user_can_login(self):
        """test user can log in"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.valid_user),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response_data)

    def test_user_cannot_login_with_invalid_password(self):
        """test user cannot login with invalid details"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.invalid_password),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['message'],
                         'Invalid password.')

    def test_non_existing_user_cannot_login(self):
        """test non-existing user cannot login"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.user_not_exist),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'], 'User not found.')

    def test_cannot_login_with_empty_password(self):
        """test cannot login with empty password"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(
                                     self.login_with_empty_password),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['message'],
                         'Password or username cannot be empty.')

    def test_user_can_reset_password(self):
        """test that user can reset his password"""
        user_data = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "password": "mbuvi1",
            "confirm password": "mbuvi1"
        }
        response = self.app.put('/api/v1/auth/reset_password',
                                data=json.dumps(user_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'password updated')

    def test_users_new_password_is_not_less_than_6_characters_long(self):
        """test that users new passwords are not less than  6 characters long"""
        user_data = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "password": "mbuv",
            "confirm password": "mbuv"
        }
        response = self.app.put('/api/v1/auth/reset_password',
                                data=json.dumps(user_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'passwords should be 6 characters or more.')

    def test_users_email_is_valid(self):
        """test that users email when changing password is valid"""
        user_data = {
            "email": "meshmbuvi",
            "username": "musyoka",
            "password": "mbuvi1",
            "confirm password": "mbuvi1"
        }
        response = self.app.put('/api/v1/auth/reset_password',
                                data=json.dumps(user_data),
                                content_type='application/json')
        # self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Email is invalid')

    def test_user_passwords_match(self):
        """test that users passwords are matching when updating user details"""
        user_data = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "password": "mbuvi1",
            "confirm password": "mbuviq1"
        }
        response = self.app.put('/api/v1/auth/reset_password',
                                data=json.dumps(user_data),
                                content_type='application/json')
        # self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Passwords do not match')

    def test_user_can_logout(self):
        """Register a new user, log him in, and then try to log him out."""

        # Register user
        self.app.post('/api/v1/auth/signup', data=json.dumps(self.user_data), 
                                             content_type='application/json')
        # login
        response = self.app.post('/api/v1/auth/login', data=json.dumps(self.valid_user),
                                                       content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        token = received_data['token']
        # logout
        response = self.app.post('/api/v1/auth/logout', headers={'content_type': 'application/json',
                                                                 'Authorization': 'Bearer {}'.format(token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['message'], "Successfully logged out")


    def test_can_get_documentation(self):
        response = self.app.get('/api/v1/docs')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
