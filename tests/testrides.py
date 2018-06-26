import json
import unittest

from application import create_app


class RidesofferTests(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment """

        self.app = create_app('testing')
        self.app = self.app.test_client()
        """Change start time to be a several days from now for self.ride"""
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
        """Release flask app instance"""
        self.app = None
        self.ride = None
        self.past_ride = None

    def test_create_ride(self):
        """test user can create a ride"""
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'ride offer added successfully.')

    def test_cannot_create_ride_with_wrong_date_time(self):
        """Tests that date is parsed in the specified format
        The date format is Month day Year hour:minutes"""
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(self.ride_with_wrong_date),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "use correct format for date and time.")

    def test_cannot_create_ride_without_details(self):
        ride = {}
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "make sure you provide all required fields.")

    def test_available_space_can_only_be_numbers(self):
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(self.wrong_ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "available space can only be numbers.")

    def test_get_all_rides(self):
        """test user can get available ride offers"""
        response = self.app.get('/api/v1/rides',
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_a_ride(self):
        """test user can get a single ride offer.
        Create a ride offer and retrieve it"""
        self.app.post('/api/v1/rides',
                      data=json.dumps(self.ride),
                      content_type='application/json')
        # Get ana offer, assuming the order is assigned id=1
        response = self.app.get('/api/v1/rides/1',
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['id'], 1)

    def test_get_ride_that_does_not_exist(self):
        """Assumes no ride with a negative id number"""
        id = -1
        response = self.app.get('/api/v1/rides/{}'.format(id),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Ride does not exist')

    def test_user_can_request_a_ride(self):
        """test user can join a ride"""
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        ride_id = int(response_data['offer id'])
        response = self.app.post('/api/v1/rides/{}/requests' . format(ride_id),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "Your request has been send.")

    def test_user_cannot_request_a_non_existing_ride(self):
        response = self.app.post('/api/v1/rides/-1/requests',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "That ride does not exist")

    def test_user_cannot_request_a_past_ride(self):
        """Create a past ride and request to join it.It should fail"""
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(self.past_ride),
                                 content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        ride_id = int(response_data['offer id'])
        response = self.app.post('/api/v1/rides/{}/requests' . format(ride_id),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "The ride requested has already expired")

    def test_user_can_view_user_requests_to_join_a_ride(self):
        """Test users can view users requests to join a ride offer."""
        # Create an offer
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json')
        # request to join the ride
        response_data = json.loads(response.get_data().decode('utf-8'))
        ride_id = int(response_data['offer id'])
        self.app.post('/api/v1/rides/{}/requests' . format(ride_id),
                      content_type='application/json')
        # view user requests
        response = self.app.get('/api/v1/rides/{}/requests' . format(ride_id),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertIn('requests', response_data)

    def test_user_cannot_view_user_requests_for_no_existind_offer(self):
        """test user cannot view user requests for non existing ride offer. """
        response = self.app.get('/api/v1/rides/{}/requests' . format(-1),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertNotIn('requests', response_data)


if __name__ == '__main__':
    unittest.main()
