from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
from datetime import datetime

from application.models.ride_models import RideOffer
from application import db

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
        return {'message':
                        'use correct format for date and time.'}, 400


def convert_date(date_string):
    """:Returns
        : start_time(str) a string representation for time is successful"""
    try:
        date = datetime.strptime(date_string, '%B %d %Y %I:%M%p')
        startTime = datetime.strftime(date, '%B %d %Y %I:%M%p')
        return startTime
    except Exception as e:
        return {'message':
                        'use correct format for date and time.'}, 400


class Rides(Resource):

    @api.doc(responses={'message': 'ride offer added successfully.',
                        201: 'Created', 400: 'BAD FORMAT',
                        401: 'UNAUTHORIZED'})
    @api.expect(ride)
    @jwt_required
    def post(self):
        """Creates a new ride offer"""
        data = request.get_json()
        current_user_email = get_jwt_identity()
        # Check whether there is data
        if any(data):
            # save ride to data structure
            if not isinstance(data['available space'], int):
                return {'message': 'available space can only be numbers.'}, 400
            if past_date(data['start time']) == True:
                return {'message': 'Cannot create an expired ride'}, 400

            query = "SELECT user_type from users where email='{}'"\
                .format(current_user_email)
            result = db.execute(query)
            row = result.fetchone()
            if row[0] == 'passenger':
                return "Please upgrade your account to be a driver to access this service", 401

            try:
                start_time = convert_date(data['start time'])
                if type(start_time) == type(str("")):
                    query = "SELECT * from rides where start_point='{}'\
                     and destination = '{}' and start_time='{}' \
                     and owner_id=(SELECT user_id from users \
                     where email='{}')" . format(data['start point'],
                                                    data['destination'],
                                                    start_time, current_user_email)

                    result = db.execute(query)
                    row = result.fetchone()
                    if row is None:
                        data['start time'] = start_time
                        ride_offer = RideOffer(data)
                        # save data here
                        ride_offer.save(current_user_email)
                        return {'message':
                                'ride offer added successfully.'}, 201
                    return {'message': 'offer exists.'}, 409

                # return the error caught on datetime conversion since it is saved on variable start_time
                return start_time
                
            except Exception as e:
                print(e)
                return {'message': 'Request not successful'}, 500
        else:
            return {'message':
                    'make sure you provide all required fields.'}, 400

    @jwt_required
    def put(self,ride_id):
        query = "select * from rides where ride_id='{}'".format(ride_id)
        result = db.execute(query)
        ride = result.fetchone()
        if ride is None:
            return {'message': 'Offer with given id does not exist'}, 404
        current_user_email = get_jwt_identity()
        query =  "select user_id from users where email='{}'"\
                    . format(current_user_email)
        result = db.execute(query)
        user_id = result.fetchone()
        if not ride[1] == user_id[0]:
            return {'message': 'You cannot change \
                        details of ride offer you do not own'}, 401
        
        data = request.get_json()
        if not isinstance(data['available space'], int):
                return {'message': 'available space can only be numbers.'}, 400

        start_time=convert_date(data['start time'])
        if type(start_time) != type(str("")):
            """time is not in the correct format"""
            return start_time

        if past_date(start_time) == True:
            return {'message': 'Cannot create an expired ride'}, 400

        query = "update rides set start_point='{}',destination='{}', start_time='{}',\
                 route='{}', available_space='{}' where ride_id='{}'"\
                 . format(data['start point'], data['destination'], data['start time'],\
                  data['route'], data['available space'] ,int(ride_id))
        db.execute(query)
        
        query = "select * from rides where ride_id='{}'".format(ride_id)
        result = db.execute(query)
        ride = result.fetchone()
        return jsonify({'id': ride[0],'start point': ride[2], 'destination': ride[3],\
         'start time': ride[4], 'route': ride[5], 'available seats': ride[6]})

    @jwt_required
    def delete(self,ride_id):        
        query = "select user_id from users where email='{}'".format(get_jwt_identity())
        result = db.execute(query)
        user_id = result.fetchone()

        query = "select * from rides where ride_id='{}' and owner_id='{}'"\
                .format(ride_id, user_id[0])
        result = db.execute(query)
        if len(result.fetchall()) > 0:
            query = "delete from rides where ride_id='{}' and owner_id='{}'"\
                .format(ride_id, user_id[0])
            result = db.execute(query)
            return {'message': 'Ride offer deleted successfully'}
        else:    
            return {'message': 'Ride offer not found.'}, 404


class AllRides(Resource):

    @api.doc('Get Available rides',
             params={'ride_id': 'Id for a single ride offer'},
             responses={200: 'OK', 404: 'NOT FOUND'})
    def get(self, ride_id=None):
        
        query = ''
        if ride_id is None:
            query = "SELECT * from rides"
        
        else:
            query = "SELECT * from rides where ride_id = {}"\
                . format(ride_id)

        offer_filter = request.args
        if len(offer_filter) > 0:
            search_key = offer_filter['key']
            search_value = offer_filter['{}'.format(search_key)]
            query = "SELECT * from rides where {}='{}'".format(search_key, search_value)
        
        try:            
            result = db.execute(query)
            rows = result.fetchall()
            if (len(rows) == 0) and (ride_id is not None):
                # This works when user retrieves a single ride offer
                return {'message': 'Offer not found'}, 404
            return jsonify([
                {'id': row[0], 'start point': row[2],
                    'destination': row[3], 'start_time': row[4],
                    'route': row[5],
                    'available space': row[6]}
                for row in rows])
            
        except Exception as e:
            return {'message': 'Request not successful'}, 500


class JoinRide(Resource):

    @api.doc('Request to join a ride offer',
             params={'ride_id': 'Id for offer to join'},
             responses={201: 'Created', 404: 'NOT FOUND', 403: 'EXPIRED'})
    @jwt_required
    def post(self, ride_id):
        """Sends user request to join a ride offer"""
        try:
            # sample user
            current_user_email = get_jwt_identity()
            # Get user ID
            query = "SELECT users.user_id \
                            from users where email='{}'"\
                            . format(current_user_email)
            result = db.execute(query)
            user_row = result.fetchone()
            if user_row is None:
                return {'message': 'User not found'}, 404
            user_id = user_row[0]
            # Find the particular ride offer to check its availability
            query = "SELECT * from rides where ride_id = '{}'" . format(
                ride_id)
            result = db.execute(query)
            row = result.fetchone()
            if row is None:
                return {'message': 'That ride does not exist'}, 404
            # check whether this ride offer belongs to the user
            if user_id == row[1]:
                return {'message':
                        'You cannot request to join your own offer'}, 403
            request_data = request.get_json()
            if 'pick-up point' not in request_data or 'drop-off point' not in request_data or\
                   'seats_booked' not in request_data:
                   return {'message': 'provide pick-up and drop-off points, and number of seats you want to book. '}, 400
            
            pick_up = request_data['pick-up point']
            drop_off = request_data['drop-off point']
            seats_booked = request_data['seats_booked']
            status = 'pending'
            # # check whether ride offer has any remaining space
            if row[6] < seats_booked:
                return {'message': 'No available space for you.'}, 403

            # check whether ride offer is expired
            time = (row[4])
            if time > datetime.now():
                # check whether users has alread requested given ride offer
                query = "SELECT * from requests where user_id = (SELECT users.user_id \
                            from users where email='{}') and ride_id = {}"\
                    . format(current_user_email, ride_id)
                result = db.execute(query)
                result = result.fetchone()
                if result is None:                    
                    # save user requests now
                    query = "INSERT INTO requests (date_created, ride_id, user_id, pick_up_point,\
                    drop_off_point, seats_booked, status)\
                                values('{}', '{}', '{}', '{}', '{}', '{}', '{}')"\
                                 . format(datetime.now(), ride_id, user_id, pick_up, drop_off, \
                                  seats_booked, status)
                    db.execute(query)
                    return {'message': 'Your request has been send.'}, 201
                # user has already requested to join this ride offer
                return{'message': 'You already requested this ride.'}, 403
            else:
                return {'message':
                        'The ride requested has already expired'}, 403
        except Exception as e:
            print(e)
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
            query = "SELECT user_id from users where email='{}'"\
                .format(get_jwt_identity()
                        )
            result = db.execute(query)
            row = result.fetchone()
            owner_id = row[0]

            query = "SELECT firstname,phone,pick_up_point,drop_off_point, seats_booked, \
            start_time,status, req_id from users INNER JOIN requests \
                    ON requests.user_id = users.user_id INNER JOIN \
                    rides on rides.ride_id = '{}' where rides.owner_id = '{}'" \
                    . format(ride_id, owner_id)
            result = db.execute(query)
            rows = result.fetchall()
            if len(rows) > 0:
                return jsonify([{'Request Id':row[7],'name of user': row[0], 'user phone contact': row[1],
                                 'pick up point': row[2],
                                 'drop-off point': row[3],
                                 'seats booked': row[4],
                                 'start time': row[5],
                                 'status': row[6]} for row in rows])
            return {'message': "You do not have any ride offer."}, 404
        except Exception as e:  return e, 500

    @jwt_required
    def put(self, request_id):
        """Driver can accept or reject the ride offer."""
        try:
            action = request.args['action']
            response = ''
            # check whether driver already accepted the offer.
            query = "select status,seats_booked,ride_id from requests where\
                     req_id='{}'".format(request_id)
            result = db.execute(query)
            result_rows = result.fetchone()

            query = "select available_space from rides where ride_id='{}'"\
                        .format((result_rows[2]))
            result = db.execute(query)
            seats = result.fetchone()
            available_seats = seats[0]            

            # check for action to take
            if action.lower() == 'accept':
                if result_rows[0] == 'accepted':
                    return {'message': 'You already accepted this user request'},403
                action = 'accepted'                
                # Decrement the available seats by one
                available_seats -= result_rows[1]
                
                # set message to be returned to user after request update cycle
                response = {'message': 'Request accepted'}
            else:
                # Reject an already accepted request; this means available seats should be incremented
                if result_rows[0] == 'accepted' :
                    available_seats += result_rows[1]
                    response = {'message': 'Request canceled'}
                    action = 'canceled'
                elif result_rows[0] == 'rejected':
                    return {'message': 'Request already rejected'}
                else:
                    action = 'rejected'
                    response = {'message': 'Request rejected'}   
            query = "update requests set status='{}' where requests.req_id='{}'" \
             . format(action, int(request_id))
            db.execute(query)

            query = "update rides set available_space='{}' where ride_id='{}'"\
                        .format(int(available_seats), result_rows[2])
            db.execute(query)
            return response

        except Exception as e: return e, 500


api.add_resource(Rides, '/users/rides', '/users/rides/<ride_id>')
api.add_resource(AllRides, '/rides', '/rides/<string:ride_id>')
api.add_resource(JoinRide, '/rides/<ride_id>/requests')
api.add_resource(Requests, '/users/rides/<ride_id>/requests', '/users/rides/requests/<request_id>')
