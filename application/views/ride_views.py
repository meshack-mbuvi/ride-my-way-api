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


class SingleRide(Resource):

    @api.doc('Get single ride offer',
             params={'ride_id': 'Id for a single ride offer'},
             responses={200: 'OK', 404: 'NOT FOUND'})
    def get(self, ride_id):
        """Retrieves a single ride offer."""
        try:
            ride = rides[int(ride_id)]
            ride['id'] = int(ride_id)
            return jsonify(ride)
        except Exception as e:
            return {'message': 'Ride does not exist'}, 404


api.add_resource(SingleRide, '/rides/<string:ride_id>')
