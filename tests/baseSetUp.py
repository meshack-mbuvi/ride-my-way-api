import json
import unittest

from application import create_app


class Base(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()
        from application import db
        self.db = db
        self.db.drop_all()
        self.db.create_all()

        # create user
        self.user_data = {
            "firstname":"sita",
            "secondname":"mbevo",
            "email": "mesh@gmail.com",
            "driver": True,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        self.app.post('/api/v1/auth/signup',
                        data=json.dumps(self.user_data),
                        content_type='application/json')

        # login to get token
        user_login_data = {
            "email": "mesh@gmail.com",
            "password": "mbuvi1"
        }
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(user_login_data),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        
        token = response_data['token']
        # add the token to the authorization header
        self.headers = {'Authorization': 'Bearer {}'.format(token)}
        self.invalid_token = {
            'Authorization': 'Bearer {}'.format((token)[:-1] + '0')}

        # signup a passenger
        self.passenger = {
            "firstname":"passenger1",
            "secondname":"passenger1",
            "email": "passenger1@gmail.com",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800519",
            "confirm password": "mbuvi1"
        }
        self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.passenger),
                                 content_type='application/json')
        # login to get token
        passenger_login_data = {
            "email": "passenger1@gmail.com",
            "password": "mbuvi1"
        }
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(passenger_login_data),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        passenger_token = response_data['token']
        self.headers_for_passenger = {
            'Authorization': 'Bearer {}'.format(passenger_token)}

        self.ride = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "June 10 2030 6:00AM",
            "available space": 6
        }

        self.past_ride = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "June 10 1900 6:00AM",
            "available space": 6
        }
        self.wrong_ride = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "June 10 2018 6:00AM",
            "available space": "Ten"
        }
        self.ride_with_wrong_date = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "111111",
            "available space": 6
        }

    def tearDown(self):
        """Clean memory."""
        self.db.drop_all()
        self.app = None
        self.ride = None
        self.past_ride = None
        