class RideOffer(object):
    """Model of a ride offer
    start point: String location of the driver,
    destination: String end-point of the journey,
    route: String ordered roads driver is going to use,
    start time: Datetime time driver starts the ride.,
    available space: Int available space for passengers
    requests : List holding users who request to join the ride
    """

    def __init__(self, data):
        self.start_point = data['start point']
        self.destination = data['destination']
        self.route = data['route']
        self.start_time = data['start time']
        self.available_space = data['available space']
        self.requests = []

    def getDict(self):
        return self.__dict__
