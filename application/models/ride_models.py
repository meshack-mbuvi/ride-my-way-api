from datetime import datetime
from application import db


class RideOffer():
    """Model of a ride offer
    start point: String location of the driver,
    destination: String end-point of the journey,
    route: String ordered roads driver is going to use,
    start time: Datetime time driver starts the ride.,
    available space: Int available space for passengers
    requests : List holding users who request to join the ride
    """
    def __init__(self, ridedata):
        self.start_point = ridedata['start point']
        self.destination = ridedata['destination']
        date = datetime.strptime(ridedata['start time'], '%Y-%m-%d %H:%M')
        self.start_time = datetime.strftime(date, '%Y-%m-%d %H:%M')
        self.route = ridedata['route']
        self.available_space = ridedata['available space']

    def save(self, current_user_email):
        # insert new record
        query = "INSERT INTO rides (owner_id,start_point,destination,start_time,\
        route,available_space) \
                VALUES ((SELECT user_id from users where email ='{}'), '{}',\
                        '{}','{}','{}', '{}')" . format(current_user_email,
                                                        self.start_point,
                                                        self.destination,
                                                        self.start_time,
                                                        self.route,
                                                        self.available_space)
        db.execute(query)        
