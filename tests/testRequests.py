

# class Request(testRides):

#     def test_user_can_request_a_ride(self):
#         """test user can join a ride."""
#         # create a ride to be sure a ride exists.
#         self.app.post('/api/v1/users/rides',
#                       data=json.dumps(self.ride),
#                       content_type='application/json',
#                       headers=self.headers)
#         response = self.app.post('/api/v1/rides/1/requests',
#                                  content_type='application/json',
#                                  headers=self.headers_for_passenger)
#         response_data = json.loads(response.get_data().decode('utf-8'))
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response_data['message'],
#                          "Your request has been sent.")

#     def test_user_cannot_request_a_ride_twice(self):
#         """test user cannot request to join a ride twice."""
#         # create a ride to be sure a ride exists.
#         self.app.post('/api/v1/users/rides',
#                       data=json.dumps(self.ride),
#                       content_type='application/json',
#                       headers=self.headers)

#         # show interest to join the ride offer twice
#         self.app.post('/api/v1/rides/1/requests',
#                                  content_type='application/json',
#                                  headers=self.headers_for_passenger)
#         response = self.app.post('/api/v1/rides/1/requests',
#                                  content_type='application/json',
#                                  headers=self.headers_for_passenger)
#         response_data = json.loads(response.get_data().decode('utf-8'))
#         self.assertEqual(response.status_code, 403)
#         self.assertEqual(response_data['message'],
#                          "You already requested this ride.")

#     def test_user_cannot_request_a_non_existing_ride(self):
#         """test user cannot request a non existing ride offer."""
#         response = self.app.post('/api/v1/rides/-1/requests',
#                                  content_type='application/json',
#                                  headers=self.headers)
#         self.assertEqual(response.status_code, 404)
#         response_data = json.loads(response.get_data().decode('utf-8'))
#         self.assertEqual(response_data['message'],
#                          "That ride does not exist")

#     def test_user_can_view_user_requests_to_join_a_ride(self):
#         """Test users can view users requests to join a ride offer.
#         creates a new ride, sends request to join the ride offer.
#         Using login details for driver, view all requests."""
#         self.app.post('/api/v1/users/rides',
#                       data=json.dumps(self.ride),
#                       content_type='application/json',
#                       headers=self.headers)
#         self.app.post('/api/v1/rides/1/requests',
#                       content_type='application/json',
#                       headers=self.headers_for_passenger)
#         response = self.app.get('/api/v1/users/rides/1/requests',
#                                 content_type='application/json',
#                                 headers=self.headers)
#         self.assertEqual(response.status_code, 200)
#         response_data = json.loads(response.get_data().decode('utf-8'))
#         self.assertTrue(response_data > 0)

#     def test_user_cannot_view_user_requests_for_no_existing_offer(self):
#         """test user cannot view user requests for non existing ride offer. """
#         response = self.app.get('/api/v1/users/rides/-1/requests',
#                                 content_type='application/json',
#                                 headers=self.headers)
#         self.assertEqual(response.status_code, 404)
#         response_data = json.loads(response.get_data().decode('utf-8'))
#         self.assertNotIn('requests', response_data)

#     def test_driver_can_accept_user_request(self):
#         """test that a driver can accept users request."""
#         self.app.post('/api/v1/users/rides',
#                       data=json.dumps(self.ride),
#                       content_type='application/json',
#                       headers=self.headers)
#         self.app.post('/api/v1/rides/1/requests',
#                       content_type='application/json',
#                       headers=self.headers_for_passenger)
#         data = {"action": "accept"}
#         response = self.app.put('/api/v1/users/rides/1/requests/1',
#                                 data=json.dumps(data),
#                                 content_type='application/json',
#                                 headers=self.headers)
#         self.assertEqual(response.status_code, 200)

#         response = self.app.get('/api/v1/users/rides/1/requests',
#                                 content_type='application/json',
#                                 headers=self.headers)
#         response_data = json.loads(response.get_data().decode('utf-8'))
#         self.assertEqual(response_data[0]['status'], 'Accepted')


# if __name__ == '__main__':
#     unittest.main()