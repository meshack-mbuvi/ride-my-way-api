from flask_jwt_extended import jwt_required, get_jwt_identity
from psycopg2 import connect
from application.models.ride_models import RideOffer
from datetime import datetime

from . import *
dbname = 'ridemyway'
user = 'ridemyway'
host = 'localhost'
password = 'ridemyway'

connection = connect(database=dbname, user=user, host=host, password=password)
connection.autocommit = True
cursor = connection.cursor()

api = Namespace('Ride offers', Description='Operations on Rides')

# data structure to store ride offers

rides = {}

ride = api.model('Ride offer', {
    'start point': fields.String(description='location of the driver'),
    'destination': fields.String(description='end-point of the journey'),
    'route': fields.String(description='ordered roads driver is going \
         to use'),
    'start time': fields.DateTime(dt_format='iso8601',
                                  description='Format:(Year Month Day Hr:MinAM/PM). time \
     driver starts the ride.'),
    'available space': fields.Integer(
        description='available space for passengers')
})


class Rides(Resource):

    @api.doc(responses={'message': 'ride offer added successfully.',
                        201: 'Created', 400: 'BAD FORMAT',
                        401: 'UNAUTHORIZED'})
    @api.expect(ride)
    @api.header('Authorization', 'Some expected header', required=True)
    @jwt_required
    def post(self):
        """Creates a new ride offer"""
        data = request.get_json()
        current_user = get_jwt_identity()
        # Check whether there is data
        if any(data):
            # save ride to data structure
            if not isinstance(data['available space'], int):
                return {'message': 'available space can only be numbers.'}, 400
            try:
                # set id for the ride offer
                ride_offer = RideOffer(data)
                # save data here
                ride_offer.save(current_user)
                response = {'message': 'ride offer added successfully.',
                            }
                return response, 201
            except Exception as e:
                return {'message':
                        'use correct format for date and time.'}, 400
        else:
            return {'message':
                    'make sure you provide all required fields.'}, 400


class AllRides(Resource):

    @api.doc('Get Available rides',
             params={'ride_id': 'Id for a single ride offer'},
             responses={200: 'OK', 404: 'NOT FOUND'})
    @jwt_required
    def get(self):
        """Retrieves all available rides"""
        try:
            query = "SELECT * from rides"
            cursor.execute(query)
            rows = cursor.fetchall()
            return jsonify([
                {'id': row[0], 'start point': row[2],
                 'destination': row[3], 'start_time': row[4], 'route': row[5],
                 'available space': row[6]}
                for row in rows])
        except Exception as e:
            raise e


class JoinRide(Resource):

    @api.doc('Request to join a ride offer',
             params={'ride_id': 'Id for offer to join'},
             responses={201: 'Created', 404: 'NOT FOUND', 403: 'EXPIRED'})
    @jwt_required
    def post(self, ride_id):
        """Sends user request to join a ride offer"""
        try:
            # sample user
            current_user = get_jwt_identity()
            # check whether ride offer is expired
            query = "SELECT * from rides where ride_id = '{}'" . format(
                ride_id)
            cursor.execute(query)
            row = cursor.fetchone()
            time = datetime.strptime(row[4], '%B %d %Y %I:%M%p')
            if time > datetime.now():
                # save user requests now
                query = "INSERT INTO requests (date_created, owner_id, user_id, status)\
                            values('{}', '{}', (SELECT users.user_id \
                            from users where username='{}'), '{}')"\
                             . format(datetime.now(), row[1],
                                      current_user, False)
                cursor.execute(query)
                return {'message': 'Your request has been send.'}, 201
            else:
                return {'message':
                        'The ride requested has already expired'}, 403
        except Exception as e:
            return {'message': 'That ride does not exist'}, 404


api.add_resource(Rides, '/users/rides')
api.add_resource(AllRides, '/rides')
api.add_resource(JoinRide, '/rides/<ride_id>/requests')
