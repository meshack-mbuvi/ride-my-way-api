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
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm_password": "mbuvi1"
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

    def test_user_can_upgrade_his_or_her_account(self):
        """test that user is able to upgrade his/her account to be a driver"""

        response = self.app.put('/api/v1/auth/upgrade?query=upgrade', 
                                headers = {'content_type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(self.token)})        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['user type'], 'driver')

    def test_user_uses_correct_format_to_upgrade_an_account(self):
        """test that user uses correct format to upgrade his account"""

        response = self.app.put('/api/v1/auth/upgrade?query=upg', 
                                headers = {'content_type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(self.token)})        
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
