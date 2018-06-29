from datetime import datetime
from . import *


class RideOffer(object):
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
        date = datetime.strptime(ridedata['start time'], '%B %d %Y %I:%M%p')
        self.start_time = datetime.strftime(date, '%B %d %Y %I:%M%p')
        self.route = ridedata['route']
        self.available_space = ridedata['available space']

    def save(self, current_user):
        # insert new record
        query = "INSERT INTO rides (owner_id,start_point,destination,start_time,route,available_space) \
                VALUES ((SELECT user_id from users where username ='{}'), '{}',\
                        '{}','{}','{}', '{}')" . format(current_user,
                                                  self.start_point,
                                                  self.destination,
                                                  self.start_time,
                                                  self.route,
                                                  self.available_space)
        cursor.execute(query)
        connection.commit()

    def fetch_all(self):
        pass
