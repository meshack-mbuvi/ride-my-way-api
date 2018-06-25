from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime

from application.models.ride_models import RideOffer

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

    @api.doc(responses={'message': 'ride offer added successfully.',
                        201: 'Created', 400: 'BAD FORMAT'})
    @api.expect(ride)
    def post(self):
        data = request.get_json()
        # Check whether there is data
        if any(data):
            # save ride to data structure
            if not isinstance(data['available space'], int):
                return {'message': 'available space can only be numbers.'}, 400
            try:
                # set id for the ride offer
                ride_offer = RideOffer(data)
                offer_id = len(rides) + 1
                rides[offer_id] = ride_offer.getDict()
                response = {'message': 'ride offer added successfully.',
                            'offer id': offer_id}
                return response, 201
            except Exception as e:
                return {'message': 'use correct format for date and time.'}, 400
        else:
            return {'message': 'make sure you provide all required fields.'}, 400


api.add_resource(Rides, '/rides')
