import json
import unittest

from baseSetUp import Base

class EditRides(Base):

    def setUp(self):
        super().setUp()
        self.app.post('/api/v1/users/rides',
                                 data=json.dumps(self.ride),
                                 content_type='application/json',
                                 headers=self.headers)
        
    def tearDown(self):
        super().tearDown()

    def test_user_can_delete_ride_offer(self):
        """test that user can delete their own rides """
        response = self.app.delete('/api/v1/users/rides/1',
                            content_type='application/json',
                            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],'Ride offer deleted successfully')

    def test_user_cannot_delete_non_existing_ride_offer(self):
        """test that user cannot delete ride that does not exist """
        response = self.app.delete('/api/v1/users/rides/-1',
                            content_type='application/json',
                            headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],'Ride offer not found.')

if __name__ == '__main__':
    unittest.main()
