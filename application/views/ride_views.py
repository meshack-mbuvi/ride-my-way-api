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


class JoinRide(Resource):

    @api.doc('Request to join a ride offer',
             params={'ride_id': 'Id for offer user is requesting to join'},
             responses={201: 'CREATED', 404: 'NOT FOUND', 403: 'FORBIDEN'})
    def post(self, ride_id):
        """Sends user request to join a ride offer"""
        try:
            # sample user
            username = 'Meshack Mbuvi'
            # check whether ride offer is expired
            ride = rides[int(ride_id)]
            if ride['start_time'] >= datetime.now():
                ride['requests'].append(username)
                return {'message': 'Your request has been send.'}, 201
            else:
                return {'message':
                        'The ride requested has already expired'}, 403
        except Exception as e:
            return {'message': 'That ride does not exist'}, 404


api.add_resource(JoinRide, '/rides/<string:ride_id>/requests')
