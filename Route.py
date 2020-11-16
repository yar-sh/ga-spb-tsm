from dijkstra import Graph, DijkstraSPF
from dijkstrawrap import *

class Route:
    def __init__(self, rm):
        self.rm = rm
        self.route_stops = []
        self.spf = None
        self._wtt = 0

    def build_spf(self) -> None:
        self.spf = DijkstraSPF(self.rm.graph, self.route_stops[0].id)


    def get_wtt(self) -> float:
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
