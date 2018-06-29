from validate_email import validate_email
from werkzeug.security import generate_password_hash

from . import *


class User():

    def __init__(self, userData):
        self.username = userData['username']
        self.email = userData['email']
        self.password = generate_password_hash(
            userData['password'], method='sha256')
        self.phone = userData['phone']
        self.driver = userData['driver']

    def save(self):
        # insert new record
        query = "\
        INSERT INTO users (username,email,password,phone,driver) VALUES " \
            "('" + self.username + "', '" + self.email + "', '" + self.password + "', \
             {},{})". format(self.phone, self.driver)
        cursor.execute(query)
        connection.commit()
