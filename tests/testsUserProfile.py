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

    def test_user_can_view_his_or_her_profile(self):
        """test that user is able to view his profile details"""
        response = self.app.post('/api/v1/auth/login', data=json.dumps(self.valid_user),
                                                       content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        token = received_data['token']
        response = self.app.get('/api/v1/auth/profile', 
                                headers = {'content_type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['username'], 'musyoka')


if __name__ == '__main__':
    unittest.main()
