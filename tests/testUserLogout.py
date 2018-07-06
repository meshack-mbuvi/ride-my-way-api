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

    def tearDown(self):
        self.app = None
        self.db = db
        self.db.create_all()

    def test_user_can_logout(self):
        """Test user can logout
        Register a new user, log him in, and then try to log him out."""

        self.app.post('/api/v1/auth/signup', data=json.dumps(self.user_data), 
                                             content_type='application/json')
        response = self.app.post('/api/v1/auth/login', data=json.dumps(self.valid_user),
                                                       content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        token = received_data['token']
        response = self.app.post('/api/v1/auth/logout', headers={'content_type': 'application/json',
                                                                 'Authorization': 'Bearer {}'.format(token)})
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(received_data['message'], "Successfully logged out")

if __name__ == '__main__':
    unittest.main()