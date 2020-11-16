from Route import Route
from dijkstrawrap import *
import random


class RouteManager:
    def __init__(self, stations : list):
        self.stations = stations
        self.graph = build_dijkstra_graph(self.stations)        


    def get_fixed_length_route(self) -> Route:
        # Always gets a route of fixed length of #total stations, but definitely has a lot of duplicate
        #   stations en-route. On avg gives wtt=3000, but it is the best option for crossover methods
        r = Route(self)

        mixed_stops = list(range(1, len(self.stations) + 1))
        random.shuffle(mixed_stops)

        r.route_stops = [ self.stations[x - 1] for x in mixed_stops ]
        r.build_spf()

        return r


    def get_variable_length_route(self) -> Route:
        # Generates a route between random stations, but keeps track of sations inbetween, so that we attempt
        #   to avoid duplicated stations. On avg gives wtt=1000, but the length of the route varies - no idea
        #   how to work with that
        r = Route(self)
        unused_stations = set(list(range(1, len(self.stations) + 1)))

        def _take_one_from_unused(remove=True) -> int:
            elem = random.choice(tuple(unused_stations)) 
            if remove:
                unused_stations.remove(elem)

            return elem

        stops = [ self.stations[_take_one_from_unused() - 1] ]

        while len(unused_stations) != 0:
            st_from = stops[-1]
            st_to = self.stations[_take_one_from_unused(False) - 1]

            info = get_path_info(self.graph, self.stations, st_from, st_to)
            for s in info["stations"]:
                unused_stations.discard(s.id)
                stops.append(s)


        r.route_stops = stops
        r.build_spf()

        return r
