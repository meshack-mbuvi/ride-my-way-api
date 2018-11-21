import json
import unittest
from application import create_app, db

class BaseUserAccount(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()
        from application import db

        self.userData = {
            "firstname":"meshack",
            "secondname":"musyoka",
            "email": "meshmbuvi@gmail.com",
            "driver": True,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm_password": "mbuvi1"
        }
        self.details_with_invalid_password = {
            "email": "meshmbuvi@gmail.com",
            "password": "mbuvimusyoka",
        }
        self.user_not_exist = {
            "email": "meshmbuvi@gmail3435xbfg.com",
            "password": "mbuvimusyoka",
        }
        self.login_with_empty_password = {
            "email": "meshmbuvi@gmail.com",
            "password":""
        }
        self.data_with_unmatching_passwords = {
            "firstname":"mbuvi",
            "secondname":"kamila",
            "email": "meshmbuvi@gmail.com",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm_password": "mbuvi11"
        }
        self.data_with_invali_email = {
            "firstname":"mbuvi",
            "secondname":"kamila",
            "email": "meshmbuvi@gmail",
            "driver": False,
            "password": "mbuvi1",
            "phone": "0719800509",
            "confirm_password": "mbuvi1"
        }
        self.data_with_empty_password = {
            "firstname":"mbuvi",
            "secondname":"kamila",
            "email": "meshmbuvi@gmail.com",
            "driver": True,
            "password": "  ",
            "phone": "0719800509",
            "confirm_password": "  "
        }

        self.data_with_short_password = {
            "firstname":"mbuvi",
            "secondname":"kamila",
            "email": "meshmbuvi@gmail.com",
            "driver": True,
            "password": "mfcf",
            "phone": "0719800509",
            "confirm_password": "mfcf"
        }

        self.db = db
        self.db.drop_all()
        self.db.create_all()

    def tearDown(self):
        self.db.drop_all()
        self.app = None
        