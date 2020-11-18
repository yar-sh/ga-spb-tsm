from static_data import *


class Neighbour:
    def __init__(self):
        self.station = None # Station we want to get to
        self.travel_interval = 0 # How often a method of transportation from current station is available, in minutes
        self.travel_time = 0 # How long it takes to get to the station from the current one, in minuts
        self.travel_method = "subway" # can be "walk" or "taxi"

    def get_wtt(self) -> float:
        if self.travel_method == "subway":
            return TRAVEL_TIME_SUBWAY_X * self.travel_time + TRAVEL_INTERVAL_SUBWAY_X * self.travel_interval
        elif self.travel_method == "walk":
            return TRAVEL_TIME_WALK_X * self.travel_time + TRAVEL_INTERVAL_WALK_X * self.travel_interval
        elif self.travel_method == "taxi":
            return TRAVEL_TIME_TAXI_X * self.travel_time + TRAVEL_INTERVAL_TAXI_X * self.travel_interval
        else:
            raise Exception("Aaaaaa panic")

    def get_travel_time(self) -> float:
        if self.travel_method == "subway":
            return TRAVEL_TIME_SUBWAY_X * self.travel_time
        elif self.travel_method == "walk":
            return TRAVEL_TIME_WALK_X * self.travel_time
        elif self.travel_method == "taxi":
            return TRAVEL_TIME_TAXI_X * self.travel_time
        else:
            raise Exception("Aaaaaa panic")
