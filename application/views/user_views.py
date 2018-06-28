from validate_email import validate_email
from psycopg2 import connect
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token

from . import *
from application.models.user_model import User, dbname, user, host, password

api = Namespace('Users', Description='User operations')

usermodel = api.model('sign up', {
    'username': fields.String(description='your username'),
    'email': fields.String(description='Your email address'),
    'phone': fields.Integer(description='Your phone number'),
    'password': fields.String(description='Your password'),
    'confirm password': fields.String(description='confirm password'),
    'driver': fields.Boolean(description='true if driver, false otherwise')
})


connection = connect(database=dbname, user=user, host=host, password=password)
connection.autocommit = True
cursor = connection.cursor()


class UserSignUp(Resource):

    @api.doc('user accounts', responses={201: 'CREATED', 400: 'BAD FORMAT', 409: 'CONFLICT'})
    @api.expect(usermodel)
    def post(self):
        """User sign up"""
        userData = request.get_json()

        username = userData['username']
        confirmPassword = userData['confirm password']
        phone = userData['phone']
        email = userData['email']
        password = userData["password"]

        if username == "" or email == "" or phone == "" or confirmPassword == "" or password == "":
            return {"message": "All fields are required."}, 400

        if len(password) < 6:
            return {'message': 'password should be 6 characters or more.'}, 400

        if not validate_email(email):
            return {"message": "Email is invalid"}, 400

        if not password == confirmPassword:
            return {'message': 'Passwords do not match'}, 400

        user = None
        try:
            query = "select username from users where username='%s'" % username
            cursor.execute(query)
            user = cursor.fetchone()
            if user is None:
                userObject = User(userData)
                userObject.save()
                return {'message': 'Account created.'}, 201
            return {'message': 'User exists.'}, 409
        except Exception as e:
            return {'message': 'We are unable to create your account at the moment.'}, 404

# model for login
model_login = api.model('Login', {'email': fields.String,
                                  'password': fields.String})


class UserLogin(Resource):

    @api.doc('user accounts', responses={201: 'CREATED', 400: 'BAD REQUEST', 401:'INVALID CREDENTIALS',404: 'NOT FOUND'})
    @api.expect(model_login)
    def post(self):
        """User login
        :returns JWT after successful login
        """

        userData = request.get_json()
        username = userData['username']
        password = userData['password']

        if username == "" or password == "":
            return {"message": "Invalid format."}, 400

        try:
            if 'email' in userData:
                email = userData['email']
                query = "select password from users where email='{}'". format(
                    email)
                cursor.execute(query)
                user = cursor.fetchone()
            else:
                query = "select password from users where username='{}'". format(
                    username)
                cursor.execute(query)
                user = cursor.fetchone()

            if check_password_hash(user[0], password):
                token = create_access_token(identity=username)
                return {'message': 'logged in.', 'token': token}, 201
            else:
                return {'message': 'Invalid crententials.'}, 401
        except Exception as e:
            return {'message': 'User not found.'}, 404

api.add_resource(UserSignUp, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
