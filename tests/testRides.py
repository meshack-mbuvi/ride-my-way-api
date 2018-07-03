import json
import unittest

from application import create_app, db


class RidesOfferTests(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()
        self.db = db
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

        # create second user
        self.passenger = {
            "email": "meshmbuvi@gmail.comqw",
            "username": "musyoka",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm password": "mbuvi1"
        }
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(self.passenger),
                                 content_type='application/json')

        # login to get token
        passenger_login_data = {
            "username": "musyoka",
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

    def test_get_a_ride(self):
        """test user can get a single ride offer.
        Create a ride offer and retrieve it"""
        self.app.post('/api/v1/users/rides',
                      data=json.dumps(self.ride),
                      headers=self.headers,
                      content_type='application/json')

        # Get an offer, assuming the order is assigned id=1
        response = self.app.get('/api/v1/rides/{}'.format(1),
                                content_type='application/json',
                                headers=self.headers)
        # self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data[0]['id'], 1)

    def test_get_ride_that_does_not_exist(self):
        """test user cannot get a ride that does not exist."""
        response = self.app.get('/api/v1/rides/-1',
                                content_type='application/json',
                                headers=self.headers)
        # self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Offer not found')

    def test_user_can_request_a_ride(self):
        """test user can join a ride."""
        # create a ride to be sure a ride exists.
        self.app.post('/api/v1/users/rides',
                      data=json.dumps(self.ride),
                      content_type='application/json',
                      headers=self.headers)
        response = self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 headers=self.headers_for_passenger)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'],
                         "Your request has been sent.")

    def test_user_cannot_request_a_ride_twice(self):
        """test user cannot request to join a ride twice."""
        # create a ride to be sure a ride exists.
        self.app.post('/api/v1/users/rides',
                      data=json.dumps(self.ride),
                      content_type='application/json',
                      headers=self.headers)

        # show interest to join the ride offer twice
        self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 headers=self.headers_for_passenger)
        response = self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 headers=self.headers_for_passenger)
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

    def test_user_can_view_user_requests_to_join_a_ride(self):
        """Test users can view users requests to join a ride offer.
        creates a new ride, sends request to join the ride offer.
        Using login details for driver, view all requests."""
        self.app.post('/api/v1/users/rides',
                      data=json.dumps(self.ride),
                      content_type='application/json',
                      headers=self.headers)
        self.app.post('/api/v1/rides/1/requests',
                      content_type='application/json',
                      headers=self.headers_for_passenger)
        response = self.app.get('/api/v1/users/rides/1/requests',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertTrue(len(response_data) > 0)

    def test_user_cannot_view_user_requests_for_no_existing_offer(self):
        """test user cannot view user requests for non existing ride offer. """
        response = self.app.get('/api/v1/users/rides/-1/requests',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertNotIn('requests', response_data)

    def test_driver_can_accept_user_request(self):
        """test that a driver can accept users request."""
        self.app.post('/api/v1/users/rides',
                      data=json.dumps(self.ride),
                      content_type='application/json',
                      headers=self.headers)
        self.app.post('/api/v1/rides/1/requests',
                      content_type='application/json',
                      headers=self.headers_for_passenger)
        data = {"action": "accept"}
        response = self.app.put('/api/v1/users/rides/1/requests/1',
                                data=json.dumps(data),
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/api/v1/users/rides/1/requests',
                                content_type='application/json',
                                headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data[0]['status'], 'Accepted')


if __name__ == '__main__':
    unittest.main()
