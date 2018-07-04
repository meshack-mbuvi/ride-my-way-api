from flask import Flask, Blueprint
from flask_restplus import Api
from flask_jwt_extended import JWTManager

from instance.config import configuration
from application.manage import Database

db = Database()
def create_app(config, database=None):
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(configuration[config])
    app.url_map.strict_slashes = False

    # Enable swagger editor
    app.config['SWAGGE_UI_JSNEDITOR'] = True

    # initialize api
    api = Api(app=app,
              title='Ride My Way',
              doc='/api/v1/documentation',
              description='Ride-my-way App is a carpooling application \
              that provides drivers with the ability to create ride offers \
              and passengers to join the ride offers.')
    doc = ('/api/v1/documentation')

    jwt = JWTManager(app)
    from application.views import blacklist

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    from application.views.ride_views import api as rides
    from application.views.user_views import api as user
    api.add_namespace(rides, path='/api/v1')
    api.add_namespace(user, path='/api/v1')
    from application.docs.views import docs
    app.register_blueprint(docs)

    return app
