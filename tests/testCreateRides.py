import json
import unittest
from baseSetUp import Base


class RidesCreation(Base):

    def setUp(self):
        """Prepare testing environment."""
        super().setUp()

    def tearDown(self):
        """Clean memory."""
        super().tearDown()

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
        """test for invalid date format
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
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "Cannot create an expired ride")

    def test_cannot_create_ride_without_details(self):
        """test that details are provided for a given a ride offer."""
        ride = {}
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(ride),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "make sure you provide all required fields.")

    def test_available_space_is_a_number(self):
        """test that available space is a number"""
        response = self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.wrong_ride),
                                 content_type='application/json',
                                 headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['message'],
                         "available space can only be numbers.")

if __name__ == '__main__':
    unittest.main()