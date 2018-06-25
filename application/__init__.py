from flask import Flask, Blueprint
from flask_restplus import Api
from instance.config import configuration


def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(configuration[config])
    app.url_map.strict_slashes = False

    # Enable swagger editor
    app.config['SWAGGE_UI_JSNEDITOR'] = True
    # initialize api
    api = Api(app=app,
              title='Ride My Way',
              doc='/api/v1/documentation')

    from application.views.ride_views import api as rides
    # Blueprints to be registered here
    api.add_namespace(rides, path='/api/v1')
    return app
