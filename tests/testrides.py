import json
import unittest

from application import create_app


class RidesofferTests(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment """

        self.app = create_app('testing')
        self.app = self.app.test_client()

    def tearDown(self):
        """Release flask app instance"""
        self.app = None

    def test_create_ride(self):
        """test user can create a ride"""
        ride = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "June 10 2018 6:00AM",
            "available space": 10
        }
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         'ride offer added successfully.')

    def test_cannot_create_ride_with_wrong_date_time(self):
        """Tests that date is parsed in the specified format
        The date format is Month day Year hour:minutes"""
        ride = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "111111",
            "available space": 10
        }
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(ride),
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
        ride = {
            "start point": "Witeithye",
            "destination": "Ngara",
            "route": "Thika superhighway",
            "start time": "June 10 2018 6:00AM",
            "available space": "10"
        }
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "available space can only be numbers.")

    def test_user_can_get_all_rides(self):
        """test user can get available ride offers"""
        response = self.app.get('/api/v1/rides',
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_get_a_ride(self):
        """test user can get a single ride offer"""
        response = self.app.get('/api/v1/rides/1',
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data['id'], 1)

    def test_user_cannot_get_ride_that_does_not_exist(self):
        """Assumes no ride with a negative id number"""
        response = self.app.get('/api/v1/rides/-1',
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(len(response_data), 0)

    def test_user_can_join_a_ride(self):
        """test user can join a ride"""
        response = self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "Your request has been send.")

    def test_user_cannot_join_a_non_existing_ride(self):
        response = self.app.post('/api/v1/rides/-1/requests',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "That ride does not exist")


if __name__ == '__main__':
    unittest.main()
