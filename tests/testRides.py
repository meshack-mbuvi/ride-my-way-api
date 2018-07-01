import json
import unittest
from psycopg2 import connect

from application import create_app, database
from application.models import dbname, user, host, password


class RidesOfferTests(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()
        self.db = database()
        self.db.create_all()

        # create user
        self.user_data = {
            "email": "meshmbuvi@gmail.com",
            "username": "mbuvi",
            "driver": True,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json')

        # login to get token
        user_login_data = {
            "username": "mbuvi",
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

        self.ride = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "June 10 2030 6:00AM",
            "available space": 10
        }

        self.past_ride = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "June 10 1900 6:00AM",
            "available space": 10
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
            "available space": 10
        }

    def tearDown(self):
        """Clean memory."""
        self.app = None
        self.ride = None
        self.past_ride = None
        self.db.drop_all()

    def test_create_ride(self):
        """test user can create a ride."""
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json',
                                 headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'],
                         'ride offer added successfully.')

    def test_cannot_create_same_ride_offer_twice(self):
        """test user cannot create a ride."""
        self.app.post('/api/v1/users/rides',
                      data=json.dumps(self.ride),
                      content_type='application/json',
                      headers=self.headers)
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json',
                                 headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response_data['message'],
                         'offer exists.')

    def test_cannot_create_ride_with_wrong_date_time(self):
        """Tests that date is parsed in the specified format
        The date format is Month day Year hour:minutes."""
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride_with_wrong_date),
                                 content_type='application/json',
                                 headers=self.headers)

        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "use correct format for date and time.")

    def test_user_cannot_create_a_past_ride(self):
        """test cannot create a past ride """
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.past_ride),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "Cannot create an expired ride")

    def test_cannot_create_ride_without_details(self):
        ride = {}
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(ride),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "make sure you provide all required fields.")

    def test_available_space_can_only_be_numbers(self):
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.wrong_ride),
                                 content_type='application/json',
                                 headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['message'],
                         "available space can only be numbers.")

    def test_get_all_rides(self):
        """test user can get available ride offers."""
        # Create a ride offer to be sure there is an offer
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json',
                                 headers=self.headers)
        response = self.app.get('/api/v1/rides/',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertTrue(response_data[0] is not None)

    def test_get_a_rides(self):
        """test user can get available ride offers."""
        # Create a ride offer to be sure there is an offer
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json',
                                 headers=self.headers)
        response = self.app.get('/api/v1/rides/1',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertTrue(response_data[0] is not None)

    def test_user_can_request_a_ride(self):
        """test user can join a ride."""
        # create a ride to be sure a ride exists.
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json',
                                 headers=self.headers)
        response = self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'],
                         "Your request has been send.")

    def test_user_cannot_request_same_ride_twice(self):
        """test user cannot request to join a ride more than once."""
        # create a ride to be sure a ride exists.
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json',
                                 headers=self.headers)
        # Requests same ride more than once
        self.app.post('/api/v1/rides/1/requests',
                      content_type='application/json',
                      headers=self.headers)
        response = self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data['message'],
                         "You already requested this ride.")

    def test_user_cannot_request_a_non_existing_ride(self):
        """test user cannot request a non existing ride offer."""
        response = self.app.post('/api/v1/rides/-1/requests',
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "That ride does not exist")


if __name__ == '__main__':
    unittest.main()
