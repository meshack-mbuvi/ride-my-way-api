from validate_email import validate_email
from werkzeug.security import generate_password_hash

from . import *


class User():

    def __init__(self, user_data):
        self.username = user_data['username']
        self.email = user_data['email']
        self.password = generate_password_hash(
            user_data['password'], method='sha256')
        self.phone = user_data['phone']
        self.driver = user_data['driver']

    def save(self):
        # insert new record
        query = "INSERT INTO users (username,email,password,phone,driver) VALUES " \
            "('" + self.username + "', '" + self.email + "', '" + self.password + "', \
             {},{})". format(self.phone, self.driver)
        cursor.execute(query)
        connection.commit()
