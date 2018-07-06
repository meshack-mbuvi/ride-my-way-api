# from testRides import *

# class TestEdit(RidesOfferTests):
#     def SetUp(self):
#         super(self.SetUp())
#     def tearDown(self):
#         super(self.tearDown())

#     def test_create_ride(self):
#         """test user can create a ride."""
#         response = self.app.post('/api/v1/users/rides',
#                                  data=json.dumps(self.ride),
#                                  content_type='application/json',
#                                  headers=self.headers)
#         response_data = json.loads(response.get_data().decode('utf-8'))
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response_data['message'],
#                          'ride offer added successfully.')