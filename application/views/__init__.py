blacklist = set()
from application import jwt
from flask_jwt_extended.default_callbacks import default_expired_token_callback

# @jwt.expired_token_loader
# def expired_token:
#     return {'message': 'Token expired'}