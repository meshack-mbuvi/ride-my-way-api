import json
import unittest
from baseUserAccountSetUp import BaseUserAccount


class UserProfileTests(BaseUserAccount):

    def setUp(self):
        """Prepare testing environment."""

        super().setUp()
        userData = {
            "firstname":"mbuvi",
            "secondname":"kamila",
            "email": "philip@gmail.com",
            "driver": True,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(userData),
                                 content_type='application/json')
        response = self.app.post('/api/v1/auth/login', data=json.dumps(userData),
                                                       content_type='application/json')
        received_data = json.loads(response.get_data().decode('utf-8'))
        self.token = received_data['token']
                

    def tearDown(self):
        super().tearDown()

    def test_user_can_view_his_or_her_profile(self):
        """test that user is able to view his profile details"""

        response = self.app.get('/api/v1/auth/profile', 
                                headers = {'content_type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(self.token)})        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['email'], 'philip@gmail.com')


if __name__ == '__main__':
    unittest.main()
