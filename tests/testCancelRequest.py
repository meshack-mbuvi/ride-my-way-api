import json
import unittest
from baseSetUp import Base


class RidesRetrievalTests(Base):

    def setUp(self):
        """Prepare testing environment."""

        super().setUp()
        self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json',
                                 headers=self.headers)
        self.request_data = {
            "pick-up point": "Juja",
            "drop-off point": "Githurai",
            "seats_booked" : 3
        }
        self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 data = json.dumps(self.request_data),
                                 headers=self.headers_for_passenger)

    def tearDown(self):
        """Clean memory."""
        super().tearDown()

    def test_user_can_cancel_request_for_a_ride(self):
        """test user can cancel thier request for a ride."""
        response = self.app.delete('api/v1/users/rides/1/requests',
                                 content_type='application/json',
                                 headers=self.headers_for_passenger)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'],
                         "Your request has been deleted.")

    def test_user_cannot_cancel_non_exsting_request_for_a_ride(self):
        """test user cannot cancel a non-existing request for a ride offer."""
        response = self.app.delete('api/v1/users/rides/-1/requests',
                                 content_type='application/json',
                                 headers=self.headers_for_passenger)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'],
                         "Request not found.")