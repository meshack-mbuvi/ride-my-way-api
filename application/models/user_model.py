from validate_email import validate_email
from werkzeug.security import generate_password_hash

from application import db


class User():

    def __init__(self, user_data):
        self.firstname = user_data['firstname']
        self.secondname = user_data['secondname']
        self.username = user_data['username']
        self.email = user_data['email']
        self.password = generate_password_hash(
            user_data['password'], method='sha256')
        self.phone = user_data['phone']
        self.driver = user_data['driver']

    def save(self):
        # insert new record
        query = "INSERT INTO users (firstname,secondname,username,email,password,phone,driver)\
        VALUES ('{}' , '{}', '{}', '{}', '{}', '{}', '{}')"\
                . format(self.firstname, self.secondname ,self.username,self.email, self.password,\
                self.phone, self.driver)

        return db.execute(query)
