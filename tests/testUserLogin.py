import json
import unittest

from application import create_app, db
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

    def test_user_cannot_login_with_password_with_less_than_6_characters(self):
        """test user cannot login with password having less than 6 characters"""
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

if __name__ == '__main__':
    unittest.main()