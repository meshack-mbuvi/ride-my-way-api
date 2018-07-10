import json
import unittest
from baseUserAccountSetUp import BaseUserAccount

class SignUpTests(BaseUserAccount):

    def setUp(self):
        """Prepare testing environment."""

        super().setUp()

    def tearDown(self):
        super().tearDown()

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
        """test user cannot sign up with empty password fields."""
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(
                                     self.data_with_empty_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'Please ensure all fields are non-empty.')

    def test_password_cannot_be_less_than_six_characters(self):
        """test user cannot sign up with password which is less than 6 characters long."""
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
