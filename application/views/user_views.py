from validate_email import validate_email
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token
from werkzeug.security import generate_password_hash
from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime

from application.models.user_model import User
from application import db
from . import blacklist

api = Namespace('Users', Description='User operations')

usermodel = api.model('sign up', {
    'username': fields.String(description='your username'),
    'email': fields.String(description='Your email address'),
    'phone': fields.Integer(description='Your phone number'),
    'password': fields.String(description='Your password'),
    'confirm password': fields.String(description='confirm password'),
    'driver': fields.Boolean(description='true if driver, false otherwise')
})


class UserSignUp(Resource):

    @api.doc('user accounts',
             responses={201: 'CREATED',
                        400: 'BAD FORMAT', 409: 'CONFLICT'})
    @api.expect(usermodel)
    def post(self):
        """User sign up"""
        userData = request.get_json()
        username = userData['username']
        confirmPassword = userData['confirm password']
        phone = userData['phone']
        email = userData['email']
        password = userData["password"]

        if username.strip() == "" or email == "" or phone.strip() == ""\
                or confirmPassword.strip() == "" or password.strip() == "":
            return {"message": "Please ensure all fields are non-empty."}, 400

        if len(password) < 6:
            return {'message': 'password should be 6 characters or more.'}, 400

        if not validate_email(email):
            return {"message": "Email is invalid"}, 400

        if not password == confirmPassword:
            return {'message': 'Passwords do not match'}, 400

        try:
            query = "select username from users where username='%s'\
             or email='%s' or phone='%s'" % (username, email, phone)
            result = db.execute(query)
            user = result.fetchone()
            if user is None:
                userObject = User(userData)
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
        username = userData['username']
        password = userData['password']

        if username.strip() == "" or password.strip() == "":
            return {"message": "Password or username cannot be empty."}, 401

        try:
            query = ""
            if 'email' in userData:
                email = userData['email']
                query = "select password from users where email='{}'". format(
                    email)
            else:
                query = "select password from users where username='{}'"\
                    . format(username)
            result = db.execute(query)
            user = result.fetchone()

            if user is None:
                return {'message': 'User not found.'}, 404

            if check_password_hash(user[0], password):
                token = create_access_token(identity=username)
                return {'message': 'logged in.', 'token': token}, 201
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
        username = userData['username']
        confirmPassword = userData['confirm password']
        email = userData['email']
        password = userData["password"]

        if username.strip() == "" or email == "" or \
                confirmPassword.strip() == "" or password.strip() == "":
            return {"message": "Please ensure all fields are non-empty."}, 400

        if len(password) < 6:
            return {'message': 'passwords should be 6 characters or more.'}, 400

        if not (validate_email(email)):
            return {"message": "Email is invalid"}, 400

        if not password == confirmPassword:
            return {'message': 'Passwords do not match'}, 400

        # update user details now
        try:
            query = "SELECT *  from users where username='{}' and email='{}'"\
                . format(username, email)
            result = db.execute(query)
            row = result.fetchone()
            if row is not None:
                query = "UPDATE users SET password = '{}' \
                    where username='{}' and email='{}'"\
                    . format(generate_password_hash(password,
                                                    method='sha256'),
                             username, email)
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


api.add_resource(UserSignUp, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(ResetPassword, '/auth/reset_password')
