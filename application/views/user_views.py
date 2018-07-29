# from validate_email import validate_email
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash
from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime
import re

from application.models.user_model import Passenger, Driver
from application import db
from . import blacklist

api = Namespace('Users', Description='User operations')

usermodel = api.model('sign up', {
    'first name': fields.String(description='your first name'),
    'second name': fields.String(description='your second name'),
    'email': fields.String(description='Your email address'),
    'phone': fields.Integer(description='Your phone number'),
    'password': fields.String(description='Your password'),
    'confirm_password': fields.String(description='confirm password'),
    'driver': fields.Boolean(description='true if driver, false otherwise')
})

def validate_email(email):
    match = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)",email)
    if match is not None:
        return True
    return False

class UserSignUp(Resource):

    @api.doc('user accounts',
             responses={201: 'CREATED',
                        400: 'BAD FORMAT', 409: 'CONFLICT'})
    @api.expect(usermodel)
    def post(self):
        """User sign up"""
        userData = request.get_json()
        firstname = userData['firstname']
        secondname = userData['secondname']
        confirmPassword = userData['confirm_password']
        phone = userData['phone']
        email = userData['email']
        password = userData["password"]
        
        if email == "" or phone.strip() == ""\
                or confirmPassword.strip() == "" or password.strip() == ""\
                or firstname.strip() == "" or secondname.strip() == "":
            return {"message": "Please ensure all fields are non-empty."}, 400

        if len(password) < 6:
            return {'message': 'password should be 6 characters or more.'}, 400

        if not validate_email(email):
            return {"message": "Email is invalid"}, 400

        if not password == confirmPassword:
            return {'message': 'Passwords do not match'}, 400

        try:
            query = "select email from users where email='%s'\
             or phone='%s'" % (email, phone)
            result = db.execute(query)
            user = result.fetchone()
            if user is None:
                if userData['driver']:
                    userObject = Driver(userData)
                    userObject.save()
                else:
                    userObject = Passenger(userData)
                    userObject.save()
                return {'message': 'Account created.'}, 201
            return {'message': 'User exists.'}, 409
        except Exception as e:
            print(e)
            return {'message': 'Request not successful'}, 500

# model for login
model_login = api.model('Login', {'email': fields.String,
                                  'password': fields.String})


class UserLogin(Resource):

    @api.doc('user accounts',
             responses={201: 'CREATED',
                        400: 'BAD REQUEST',
                        401: 'INVALID CREDENTIALS',
                        404: 'NOT FOUND'})
    @api.expect(model_login)
    def post(self):
        """User login
        :returns JWT after successful login
        """

        userData = request.get_json()
        email = userData['email']
        password = userData['password']

        if email.strip() == "" or password.strip() == "":
            return {"message": "Password or email cannot be empty."}, 401

        try:
            query = "select password,user_type,firstname from users where email='{}'"\
                    . format(email)
            result = db.execute(query)
            user = result.fetchone()

            if user is None:
                return {'message': 'User not found.'}, 404

            if check_password_hash(user[0], password):
                token = create_access_token(identity=email)
                return {'message': 'logged in.', 'token': token, \
                        'user_type': user[1], 'firstname': user[2]}, 201
            else:
                return {'message': 'Invalid password.'}, 401
        except Exception as e:
            print(e)
            return {'message': 'Request not successful'}, 500


class ResetPassword(Resource):

    @api.doc('user accounts',
             responses={200: 'OK', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    @api.expect(model_login)
    def put(self):
        userData = request.get_json()
        confirmPassword = userData['confirm password']
        email = userData['email']
        password = userData["password"]

        if email.strip() == "" or confirmPassword.strip() == ""\
             or password.strip() == "":
            return {"message": "Please ensure all fields are non-empty."}, 400

        if len(password.strip()) < 6:
            return {'message': 'passwords should be 6 characters or more.'}, 400

        if not (validate_email(email)):
            return {"message": "Email is invalid"}, 400

        if not password == confirmPassword:
            return {'message': 'Passwords do not match'}, 400

        # update user details now
        try:
            query = "SELECT *  from users where email='{}'"\
                . format(email)
            result = db.execute(query)
            row = result.fetchone()
            if row is not None:
                query = "UPDATE users SET password = '{}' \
                    where email='{}'"\
                    . format(generate_password_hash(password,
                                                    method='sha256'),
                             email)
                db.execute(query)
                return {'message': 'password updated'}
            else:
                return {'message': 'user not found'}, 404
        except Exception as e: return {'message': 'Request not successful'}, 500

class Logout(Resource):
    """handles user logout."""
    @jwt_required
    def post(self):
        """Log out a given user by blacklisting user's token
        :return
            message and status code.
        """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return ({'message': "Successfully logged out"}), 200

class Profile(Resource):
    @jwt_required
    def get(self):
        """Retrieves user account details."""
        email = get_jwt_identity()
        query = "select firstname,secondname, phone, \
           user_type from users where email='{}'".format(email)
        result = db.execute(query)
        users = result.fetchone()     
        return {'firstname': users[0], 'secondname':users[1], \
                'phone number': users[2], 'email': email, \
                'user type': users[3]}, 200


class AccountUpgrade(Resource):
    @jwt_required
    def put(self):
        """Upgrades user account for user to be a driver."""
        action = request.args['query']
        email = get_jwt_identity()
        if action == 'upgrade':
            query = "update users set user_type='{}' where email='{}'"\
               .format('driver', email)
            db.execute(query)
            query = "select user_type from users where email='{}'".format(email)
            result = db.execute(query)
            user_type = result.fetchone()
            return {'user type': user_type[0]}, 200
        return {'message': 'Bad format used'}, 400


api.add_resource(UserSignUp, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(Profile, '/auth/profile')
api.add_resource(AccountUpgrade, '/auth/upgrade')
api.add_resource(ResetPassword, '/auth/reset_password')
