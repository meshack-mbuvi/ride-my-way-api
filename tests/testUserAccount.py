import json
import unittest
from psycopg2 import connect

from application import create_app, database
from application.models import dbname, user, host, password


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
            "password": "",
            "phone": "0719800509",
            "confirm password": ""
        }

        self.data_with_short_password = {
            "email": "meshmbuvi@gmail.com",
            "username": "mbuvi",
            "driver": True,
            "password": "mfcf",
            "phone": "0719800509",
            "confirm password": "mfcf"
        }

        self.db = database()
        self.db.create_all()

    def tearDown(self):
        self.app = None
        self.db.drop_all()

    def test_user_can_sign_up(self):
        """tests user can create an account."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json')

        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'],
                         'Account created.')

    def test_user_cannot_sign_up_with_unmatching_passwords(self):
        """tests user cannot sign up with unmatching passwords."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(
                                     self.data_with_unmatching_passwords),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'Passwords do not match')

    def test_user_cannot_sign_up_with_invalid_email(self):
        """tests user cannot sign up with invalid email."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.data_with_invali_email),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'Email is invalid')

    def test_user_cannot_sign_up_twice(self):
        """tests user cannot sign up twice."""
        self.app.post('/api/v1/auth/signup',
                      data=json.dumps(self.user_data),
                      content_type='application/json')
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response_data['message'],
                         'User exists.')

    def test_user_cannot_sign_up_with_empty_passwords(self):
        """tests user cannot sign up with empty fields."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(
                                     self.data_with_empty_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'All fields are required.')

    def test_password_cannot_be_less_than_six_characters(self):
        """tests user cannot sign up with empty fields."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(
                                     self.data_with_short_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'password should be 6 characters or more.')

if __name__ == '__main__':
    unittest.main()
