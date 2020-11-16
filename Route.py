from dijkstra import Graph, DijkstraSPF
from dijkstrawrap import *

class Route:
    _counter = 0

    def __init__(self, rm):
        self.rm = rm
        self.route_stops = []
        self.spf = None
        self._wtt = 0

        Route._counter += 1
        self.id = Route._counter


    def build_spf(self) -> None:
        self.spf = DijkstraSPF(self.rm.graph, self.route_stops[0].id)


    def get_wtt(self) -> float:
        # Lesser wtt <=> lesser distance <=> better

        # Doing some small value caching in here to avoid building a lot of graphs for re-calculating
        #   route's wtt
        if self._wtt != 0:
            return self._wtt

        wtt = 0

        for s in range(len(self.route_stops) - 1):
            st_from = self.route_stops[s]
            st_to = self.route_stops[s + 1]

            wtt += get_path_info(self.rm.graph, self.rm.stations, st_from, st_to)["time"]

        self._wtt = wtt
        return wtt

    
    def get_fitness(self) -> float:
        # Fitness is the inverse of wtt <=> inverse of distance => greater fitness <=> better
        return 1.0 / self.get_wtt()
