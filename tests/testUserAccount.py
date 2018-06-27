import json
import unittest
from psycopg2 import connect

from application import create_app, db as database
from application.models import dbname, user, host, password


class SignTests(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()

        self.user_data = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "driver": True,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        self.passwords = {
            "email": "meshmbuvi@gmail.com",
            "username": "mbuvi1",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi11"
        }
        self.email = {
            "email": "meshmbuvi",
            "username": "mbuvi1",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        self.conflict_username = {
            "email": "meshmbuvi@gmail.com",
            "username": "mbuvi",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        self.empty_password = {
            "email": "meshmbuvi@gmail.com",
            "username": "mbuvi",
            "driver": True,
            "password": "",
            "phone": "0719800509",
            "confirm password": ""
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
                                 data=json.dumps(self.passwords),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'Passwords do not match')

    def test_user_cannot_sign_up_with_invalid_email(self):
        """tests user cannot sign up with invalid email."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.email),
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
                                 data=json.dumps(self.empty_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'All fields are required.')


class LoginTests(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()

        self.user_data = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "driver": True,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        # Register user
        response = self.app.post('/api/v1/auth/signup',
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
            "email": "meshmbuvi@gmail.com",
            "username": "mutadbkjdhgksjdg",
            "password": "mbuvi1"
        }

    def tearDown(self):
        self.app = None
        con = connect(database=dbname, user=user, host=host, password=password)
        con.autocommit = True
        cur = con.cursor()
        cur.execute("DELETE from users ")

    def test_user_can_login(self):
        """tests user can log in"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.valid_user),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response_data)

    def test_user_can_login_with_email(self):
        """tests user can log in"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.login_with_email),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response_data)

    def test_user_cannot_login_with_invalid_details(self):
        """tests user can log in"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.invalid_password),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['message'],
                         'Invalid crententials.')

    def test_non_existing_user_cannot_login(self):
        """tests user can log in"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.user_not_exist),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'], 'User not found.')


if __name__ == '__main__':
    unittest.main()
