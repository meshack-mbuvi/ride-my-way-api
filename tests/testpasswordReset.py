import json
import unittest


from application import create_app, db
class PasswordReset(unittest.TestCase):

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

    def tearDown(self):
        self.app = None
        self.db = db
        self.db.create_all()

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

    def test_users_new_email_is_valid(self):
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
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Email is invalid')

    def test_user_new_passwords_match(self):
        """test that users email when changing password is valid"""
        user_data = {
            "email": "meshmbuvi@gmail.com",
            "username": "musyoka",
            "password": "mbuvi1",
            "confirm password": "mbuviq1"
        }
        response = self.app.put('/api/v1/auth/reset_password',
                                data=json.dumps(user_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Passwords do not match')

if __name__ == '__main__':
    unittest.main()
