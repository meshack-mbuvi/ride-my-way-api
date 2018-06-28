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


api.add_resource(JoinRide, '/rides/<ride_id>/requests')


class Rides(Resource):

    @api.doc(responses={'message': 'ride offer added successfully.',
                        201: 'Created', 400: 'BAD FORMAT'})
    @api.expect(ride)
    def post(self):
        """creates a new ride offer."""
        data = request.get_json()
        # Check whether there is data
        if any(data):
            # save ride to data structure
            if not isinstance(data['available space'], int):
                return {'message': 'available space can only be numbers.'}, 400
            try:
                # set id for the ride offer
                rideOffer = RideOffer(data)
                offerId = len(rides) + 1
                rides[offer_id] = ride_offer.getDict()
                response = {'message': 'ride offer added successfully.',
                            'offer id': offer_id}
                return response, 201
            except Exception as e:
                return {'message': 'use correct format for date and time.'}, 400
        else:
            return {'message': 'make sure you provide all required fields.'}, 400

    @api.doc('list of rides', responses={200: 'OK'})
    def get(self):
        """Retrieves all available rides"""
        availableRides = {}
        for key, value in rides.items():
            if value['start_time'] >= datetime.now():
                # convert to date to string
                value['start_time'] = datetime.strftime(
                    value['start_time'], '%B %d %Y %I:%M%p')
                availableRides[key] = value
        return (availableRides)

api.add_resource(Rides, '/rides')


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
