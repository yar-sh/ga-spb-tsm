class Neighbour:
    def __init__(self):
        self.station = None # Station we want to get to
        self.travel_interval = 0 # How often a method of transportation from current station is available, in minutes
        self.travel_time = 0 # How long it takes to get to the station from the current one, in minuts
        self.travel_method = "subway" # can be "walk" or "taxi"
