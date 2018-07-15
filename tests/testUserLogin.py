import json
import unittest
from baseUserAccountSetUp import BaseUserAccount


class LoginTests(BaseUserAccount):

    def setUp(self):
        """Prepare testing environment."""

        super().setUp()
        self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.userData),
                                 content_type='application/json')

    def tearDown(self):
        super().tearDown()

    def test_user_can_login(self):
        """test user can log in"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.userData),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response_data)

    def test_user_cannot_login_with_invalid_password(self):
        """test user cannot login with invalid details"""
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.details_with_invalid_password),
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
                         'Password or email cannot be empty.')

if __name__ == '__main__':
    unittest.main()