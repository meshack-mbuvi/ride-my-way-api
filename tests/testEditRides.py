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
        self.ride = {
            "start point": "Juja",
            "destination": "Ngara Market",
            "route": "Thika superhighway",
            "start time": "June 10 2030 6:00AM",
            "available space": 5
        }
    def tearDown(self):
        super().tearDown()

    def test_can_edit_ride_offer(self):
        """test that user can change offer details """
        response = self.app.put('/api/v1/users/rides/1',
                            data=json.dumps(self.ride),
                            content_type='application/json',
                            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['start point'],'Juja')

    def test_user_cannot_edit_ride_offer_he_does_not_own(self):
        """test that user cannot change offer details he does not own """
        response = self.app.put('/api/v1/users/rides/1',
                            data=json.dumps(self.ride),
                            content_type='application/json',
                            headers=self.headers_for_passenger)
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],'You cannot change \
                        details of ride offer you do not own')
    
    def test_can_edit_non_existing_ride_offer(self):
        """test that user cannot change details of a non-existing offer"""
        response = self.app.put('/api/v1/users/rides/-1',
                            data=json.dumps(self.ride),
                            content_type='application/json',
                            headers=self.headers)
        self.assertEqual(response.status_code, 404)
    
    def test_cannot_update_ride_with_wrong_date_time(self):
        """test for invalid date format when updating offer details
        The date format is Month day Year hour:minutes."""
        response = self.app.put('/api/v1/users/rides/1',
                                 data=json.dumps(self.ride_with_wrong_date),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response_data['message'],
                         "use correct format for date and time.")

if __name__ == '__main__':
    unittest.main()
