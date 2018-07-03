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


def past_date(date_string):
    """checks whether date given is a past date
    :returns True for past date, False otherwise."""
    try:
        str_to_date = datetime.strptime(date_string, "%B %m %Y %I:%M%p").date()
        if str_to_date > datetime.now().date():
            return False
        return True
    except Exception as e:
        # catch invalid date format
        return False


def convert_date(date_string):
    try:
        date = datetime.strptime(date_string, '%B %d %Y %I:%M%p')
        startTime = datetime.strftime(date, '%B %d %Y %I:%M%p')
        return startTime
    except Exception as e:
        return None


def str_to_date(date_string):
    try:
        date = datetime.strptime(date_string, '%B %d %Y %I:%M%p')
        return date
    except Exception as e:
        return None


class Rides(Resource):

    @api.doc(responses={'message': 'ride offer added successfully.',
                        201: 'Created', 400: 'BAD FORMAT',
                        401: 'UNAUTHORIZED'})
    @api.expect(ride)
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
            if past_date(data['start time']):
                return {'message': 'Cannot create an expired ride'}, 403

            query = "SELECT driver from users where username='{}'"\
                .format(current_user)
            cursor.execute(query)
            row = cursor.fetchone()
            if row[0] is False:
                return "Only a driver can create a ride offer.", 401

            try:
                # set id for the ride offer

                start_time = convert_date(data['start time'])
                if start_time is not None:
                    query = "SELECT * from rides where start_point='{}'\
                     and destination = '{}' and start_time='{}' \
                     and owner_id=(SELECT user_id from users \
                     where username='{}')" . format(data['start point'],
                                                    data['destination'],
                                                    start_time, current_user)

                    cursor.execute(query)
                    row = cursor.fetchone()
                    if row is None:
                        data['start time'] = start_time
                        ride_offer = RideOffer(data)
                        # save data here
                        ride_offer.save(current_user)
                        return {'message':
                                'ride offer added successfully.'}, 201
                    return {'message': 'offer exists.'}, 409
                return {'message':
                        'use correct format for date and time.'}, 400
            except Exception as e:
                return {'message': 'Request not successful'}, 500
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
            return {'message': 'Request not successful'}, 500


class SingleRide(Resource):

    @api.doc('Get Available rides',
             params={'ride_id': 'Id for a single ride offer'},
             responses={200: 'OK', 404: 'NOT FOUND'})
    @jwt_required
    def get(self, ride_id):
        """Retrieves a single ride offer"""
        try:
            query = "SELECT * from rides where ride_id = {}"\
                . format(ride_id)
            cursor.execute(query)
            rows = cursor.fetchall()

            if len(rows) > 0:
                return jsonify([
                    {'id': row[0], 'start point': row[2],
                     'destination': row[3], 'start_time': row[4],
                     'route': row[5],
                     'available space': row[6]}
                    for row in rows])
            return {'message': 'Offer not found'}, 404
        except Exception as e:
            {'message': 'Request not successful.'}, 500


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
            # Get user ID
            query = "SELECT users.user_id \
                            from users where username='{}'"\
                            . format(current_user)
            cursor.execute(query)
            user_row = cursor.fetchone()
            user_id = user_row[0]
            # check whether ride offer is expired
            query = "SELECT * from rides where ride_id = '{}'" . format(
                ride_id)
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                return {'message': 'That ride does not exist'}, 404
            time = (row[4])
            if user_id == row[1]:
                return {'message':
                        'You cannot request to join your own offer'}, 403
            if time > datetime.now():
                # check whether users has alread requested given ride offer
                query = "SELECT * from requests where user_id = (SELECT users.user_id \
                            from users where username='{}') and ride_id = {}"\
                    . format(current_user, ride_id)
                cursor.execute(query)
                result = cursor.fetchone()
                if result is None:
                    # save user requests now
                    query = "INSERT INTO requests (date_created, ride_id, user_id, status)\
                                values('{}', '{}', '{}', '{}')"\
                                 . format(datetime.now(), ride_id,
                                          user_id, False)
                    cursor.execute(query)
                    return {'message': 'Your request has been send.'}, 201
                # user has already requested to join this ride offer
                return{'message': 'You already requested this ride.'}, 403
            else:
                return {'message':
                        'The ride requested has already expired'}, 403
        except Exception as e:
            return {'message': 'Request not successful.'}, 500


class Requests(Resource):

    @api.doc('view user requests to a given ride offer',
             responses={200: 'OK', 404: 'NOT FOUND', 401: 'UNAUTHORIZED'},
             params={'ride_id': 'Id for ride user wants to view'})
    @jwt_required
    def get(self, ride_id):
        """Retrieves all requests to a given ride"""
        try:
            # get owner id
            query = "SELECT user_id from users where username='{}'"\
                .format(get_jwt_identity()
                        )
            cursor.execute(query)
            row = cursor.fetchone()
            user_id = row[0]

            query = "SELECT username,phone,start_point,destination,\
            start_time,status from users INNER JOIN requests \
                    ON requests.user_id = users.user_id INNER JOIN \
                    rides on rides.ride_id = '{}'" \
                    . format(ride_id)
            cursor.execute(query)
            rows = cursor.fetchall()
            if len(rows) > 0:
                return jsonify([{'name of user': row[0], 'user phone': row[1],
                                 'pick up point': row[2],
                                 'Destination': row[3],
                                 'start time': row[4],
                                 'status': 'Accepted' if row[5] is True
                                 else 'Pending'} for row in rows])
            return {'message': 'Ride does not exist'}, 404
        except Exception as e:
            return {'message': 'Request not successful.'}, 500


class RequestActions(Resource):

    @api.doc('view user requests to a given ride offer',
             responses={200: 'OK', 404: 'NOT FOUND', 401: 'UNAUTHORIZED'},
             params={'rideId': 'Id for ride user wants to view',
                     'requestId': 'Id identifying the request'})
    @jwt_required
    def put(self, rideId, requestId):
        """Driver can accept or reject the ride offer."""
        try:
            data = request.get_json()
            act = True
            response = ''
            if data['action'].lower() == 'accept':
                act = True
                response = {'message': 'Request accept'}
            else:
                act = False
                response = {'message': 'Request rejected'}
            query = "UPDATE requests SET status = '{}'\
             where requests.req_id = '{}' and requests.ride_id = '{}'" \
             . format(act, int(requestId), int(rideId))
            cursor.execute(query)
            return response

        except Exception as e:
            print(e)
            return {'message': 'Request not successful.'}, 500


api.add_resource(Rides, '/users/rides')
api.add_resource(AllRides, '/rides')
api.add_resource(SingleRide, '/rides/<string:ride_id>')
api.add_resource(JoinRide, '/rides/<ride_id>/requests')
api.add_resource(Requests, '/users/rides/<ride_id>/requests')
api.add_resource(RequestActions, '/users/rides/<rideId>/requests/<requestId>')
