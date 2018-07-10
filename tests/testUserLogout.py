import json
import unittest
from baseUserAccountSetUp import BaseUserAccount


class LogoutTests(BaseUserAccount):

    def setUp(self):
        """Prepare testing environment."""

        super().setUp()
        self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.userData),
                                 content_type='application/json')


    def tearDown(self):
        super().tearDown()

    def test_user_can_logout(self):
        """Test user can logout
        Register a new user, log him in, and then try to log him out."""
        response = self.app.post('/api/v1/auth/login', data=json.dumps(self.userData),
                                                       content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        token = received_data['token']
        response = self.app.post('/api/v1/auth/logout',
                                headers={'content_type': 'application/json',
                                'Authorization': 'Bearer {}'.format(token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['message'], "Successfully logged out")

if __name__ == '__main__':
    unittest.main()