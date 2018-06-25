from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime


api = Namespace('Ride offers', Description='Operations on Rides')

# data structure to store ride offers

rides = {}

ride = api.model('Ride offer', {
    'start point': fields.String(description='location of the driver'),
    'destination': fields.String(description='end-point of the journey'),
    'route': fields.String(description='ordered roads driver is going \
         to use'),
    'start time': fields.Date(description='Format:(Month Day Year Hr:MinAM/PM). time \
     driver starts the ride.'),
    'available space': fields.Integer(
        description='available space for passengers')
})


class Rides(Resource):

    @api.doc('list of rides', responses={200: 'OK'})
    def get(self):
        """Retrieves all available rides"""
        available_rides = {}
        for key, value in rides.items():
            if value['start_time'] >= datetime.now():
                # convert to date to string
                value['start_time'] = datetime.strftime(
                    value['start_time'], '%B %d %Y %I:%M%p')
                available_rides[key] = value
        return (available_rides)

api.add_resource(Rides, '/rides')
