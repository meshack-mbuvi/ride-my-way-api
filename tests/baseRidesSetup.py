import json
import unittest

from application import create_app, db

class Base(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app = self.app.test_client()
        self.db = db
        self.db.create_all()
        print("called")

    def tearDown(self):
        """Clean memory."""
        self.app = None
        self.ride = None
        self.past_ride = None
        self.db.drop_all()