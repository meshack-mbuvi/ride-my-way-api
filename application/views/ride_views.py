from flask_jwt_extended import jwt_required, get_jwt_identity
from psycopg2 import connect

from . import *
dbname = 'ridemyway'
user = 'ridemyway'
host = 'localhost'
password = 'ridemyway'

connection = connect(database=dbname, user=user, host=host, password=password)
connection.autocommit = True
cursor = connection.cursor()

from application.models.ride_models import RideOffer

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

    def isdriver(self, user):
        """checks whether user with provided username is a driver.
        :arg
            username (str): parameter to be considered.
        :returns
            True for driver, False for non-drivers.
        """
        # if user.admin:
        #     return True
        # else:
        #     return False
        pass

    @api.doc(responses={'message': 'ride offer added successfully.',
                        201: 'Created', 400: 'BAD FORMAT', 401: 'UNAUTHORIZED'})
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
                offer_id = ride_offer.save(current_user)
                response = {'message': 'ride offer added successfully.',
                            'offer id': offer_id}
                return response, 201
            except Exception as e:
                return {'message': 'use correct format for date and time.'}, 400
        else:
            return {'message': 'make sure you provide all required fields.'}, 400


class AllRides(Resource):

    @api.doc('Get Available rides',
             params={'ride_id': 'Id for a single ride offer'},
             responses={200: 'OK', 404: 'NOT FOUND'})
    @jwt_required
    def get(self):
        """Retrieves all available rides"""
        query = "SELECT * from rides"
        cursor.execute(query)
        return jsonify([{'id': i[0], 'start point': i[2], 'destination':
                         i[3], 'start_time': i[4], 'route': i[5], 'available space': i[6]} for i in cursor.fetchall()])


api.add_resource(Rides, '/users/rides')
api.add_resource(AllRides, '/rides')
