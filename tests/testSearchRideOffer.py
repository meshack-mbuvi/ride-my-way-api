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
        self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.another_ride),
                                 content_type='application/json',
                                 headers=self.headers)
        self.request_data = {
            "pick-up point": "Juja",
            "drop-off point": "Githurai",
            "seats_booked" : 3
        }

    def tearDown(self):
        """Clean memory."""
        super().tearDown()

    def test_filter_rides_by_destination(self):
        """test user can get rides with specified destination"""
        response = self.app.get('/api/v1/rides?key=destination&destination=Nairobi',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data[0]['destination'], 'Nairobi')
        self.assertEqual(len(response_data), 1)

    def test_filter_rides_by_start_point(self):
        """test user can get rides with specified start_point"""
        response = self.app.get('/api/v1/rides?key=start_point&start_point=Githurai',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data[0]['start point'], 'Githurai')
        self.assertEqual(len(response_data), 1)


if __name__ == '__main__':
    unittest.main()
