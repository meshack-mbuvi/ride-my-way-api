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

    def tearDown(self):
        """Clean memory."""
        super().tearDown()

    def test_get_all_rides(self):
        """test user can get available ride offers."""
        response = self.app.get('/api/v1/rides/',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertTrue(response_data[0] is not None)

    def test_get_a_ride(self):
        """test user can get a single ride offer."""
        # Get an offer, assuming the order is assigned id=1
        response = self.app.get('/api/v1/rides/{}'.format(1),
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data[0]['id'], 1)

    def test_get_ride_that_does_not_exist(self):
        """test user cannot get a ride that does not exist."""
        response = self.app.get('/api/v1/rides/-1',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Offer not found')

    def test_user_can_request_a_ride(self):
        """test user can join a ride."""
        response = self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 data = json.dumps(self.request_data),
                                 headers=self.headers_for_passenger)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'],
                         "Your request has been send.")

    def test_user_cannot_request_a_ride_twice(self):
        """test user cannot request to join a ride twice."""
        self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 data = json.dumps(self.request_data),
                                 headers=self.headers_for_passenger)
        response = self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 data = json.dumps(self.request_data),
                                 headers=self.headers_for_passenger)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data['message'],
                         "You already requested this ride.")

    def test_user_cannot_request_seats_than_available_ones_in_the_car(self):
        """test user cannot request more seats than the available space."""
        request_data = {
            "pick-up point": "Juja",
            "drop-off point": "Githurai",
            "seats_booked" : 13
        }
        response = self.app.post('/api/v1/rides/1/requests',
                                 content_type='application/json',
                                 data = json.dumps(request_data),
                                 headers=self.headers_for_passenger)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data['message'],
                         "No available space for you.")

    def test_user_cannot_request_a_non_existing_ride(self):
        """test user cannot request a non existing ride offer."""
        response = self.app.post('/api/v1/rides/-1/requests',
                                 content_type='application/json',
                                 data = json.dumps(self.request_data),
                                 headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "That ride does not exist")

    def test_user_can_view_user_requests_to_join_a_ride(self):
        """test user can view users requests to join a ride offer."""
        self.app.post('/api/v1/rides/1/requests',
                      content_type='application/json',
                      data = json.dumps(self.request_data),
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
        self.app.post('/api/v1/rides/1/requests',
                      content_type='application/json',
                      data = json.dumps(self.request_data),
                      headers=self.headers_for_passenger)
        action = {"action": "accept"}
        # driver accepts ride offer
        response = self.app.put('/api/v1/users/rides/requests/1',
                                data=json.dumps(action),
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/api/v1/users/rides/1/requests',
                                content_type='application/json',
                                headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data[0]['status'], 'accepted')

       # confirm that seats available are decremented accordingly
        response = self.app.get('/api/v1/rides/1',
                                content_type='application/json',
                                headers=self.headers_for_passenger)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data[0]['available space'], 3)

    def test_driver_can_cancel_an_accepted_request(self):
        """test that a driver can cancel an accepted request."""
        self.app.post('/api/v1/rides/1/requests',
                      content_type='application/json',
                      data = json.dumps(self.request_data),
                      headers=self.headers_for_passenger)
        action = {"action": "accept"}
        # driver accepts ride offer
        self.app.put('/api/v1/users/rides/requests/1',
                                data=json.dumps(action),
                                content_type='application/json',
                                headers=self.headers)
        action = {'action': 'canceled'}
        response = self.app.put('/api/v1/users/rides/requests/1',
                                data=json.dumps(action),
                                content_type='application/json',
                                headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Request canceled')

        # confirm that seats available are decremented accordingly
        response = self.app.get('/api/v1/rides/1',
                                content_type='application/json',
                                headers=self.headers_for_passenger)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data[0]['available space'], 6)
    
    def test_driver_can_reject_a_request(self):
        """test that a driver can reject a user request."""
        self.app.post('/api/v1/rides/1/requests',
                      content_type='application/json',
                      data = json.dumps(self.request_data),
                      headers=self.headers_for_passenger)
        action = {"action": "reject"}
        response = self.app.put('/api/v1/users/rides/requests/1',
                                data=json.dumps(action),
                                content_type='application/json',
                                headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Request rejected')

    def test_driver_cannot_reject_an_already_rejected_request(self):
        """test that a driver cannot reject an already rejected request."""
        self.app.post('/api/v1/rides/1/requests',
                      content_type='application/json',
                      data = json.dumps(self.request_data),
                      headers=self.headers_for_passenger)
        action = {"action": "reject"}
        self.app.put('/api/v1/users/rides/requests/1',
                                data=json.dumps(action),
                                content_type='application/json',
                                headers=self.headers)
        response = self.app.put('/api/v1/users/rides/requests/1',
                                data=json.dumps(action),
                                content_type='application/json',
                                headers=self.headers)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'], 'Request already rejected')
        

if __name__ == '__main__':
    unittest.main()
