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
    'driver': fields.Boolean(description='True if driver, False otherwise')
})


con = connect(database=dbname, user=user, host=host, password=password)
con.autocommit = True
cur = con.cursor()


class UserSignUp(Resource):

    @api.doc('user accounts', responses={201: 'CREATED', 400: 'BAD FORMAT', 409: 'CONFLICT'})
    @api.expect(usermodel)
    def post(self):
        """User sign up"""
        data = request.get_json()

        username = data['username']
        confirm_password = data['confirm password']
        phone = data['phone']
        email = data['email']
        password = data["password"]

        if username == "" or email == "" or phone == "" or confirm_password == "" or password == "":
            return {"message": "All fields are required."}, 400

        if len(password) < 6:
            return {'message': 'password should be 6 characters or more.'}, 400

        if not validate_email(email):
            return {"message": "Email is invalid"}, 400

        if not password == confirm_password:
            return {'message': 'Passwords do not match'}, 400

        user = None
        try:
            query = "select username from users where username='%s'" % username
            cur.execute(query)
            user = cur.fetchone()
            if user is None:
                data = request.get_json()
                user_object = User(data)
                user_object.save()
                return {'message': 'Account created.'}, 201
            return {'message': 'User exists.'}, 409
        except Exception as e:
            return {'message': 'We are unable to create your account at the moment.'}, 404

api.add_resource(UserSignUp, '/auth/signup')
