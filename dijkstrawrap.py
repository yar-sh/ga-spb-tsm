from Station import Station
from dijkstra import Graph, DijkstraSPF


def build_dijkstra_graph(stations: list) -> Graph:
    g = Graph()

    # Build the graph edges
    for s in stations:
        for n in s.neighbours:
            g.add_edge(s.id, n.station.id, n.get_wtt())

    return g


PATH_CACHE = {}
def get_path_info(g: Graph, stations:list, st_from : Station, st_to : Station, existing_spf=None) -> dict:
    # We are using caching of results to speed up the generations of spf trees and dijkstra path length calculations

    cache_key = f"{st_from.id}:{st_to.id}"
    if cache_key not in PATH_CACHE:
        d = DijkstraSPF(g, st_from.id) if existing_spf == None else existing_spf

        stops = [ stations[id - 1] for id in d.get_path(st_to.id)]
        time = 0
        stop_times = [0]

        # We must adjust the time in the path between two explicit stations, since we do not need to account
        #   for travel_interval in transit for subway neighbors (though, we do for taxi transit)
        for i in range(len(stops) - 1):
            st_1 = stops[i]
            st_2 = stops[i+1]

            for n in st_1.neighbours:
                if n.station.id == st_2.id:
                    if i == 0 or n.travel_method == "taxi":
                        time += n.get_wtt()
                    else:
                        time += n.get_travel_time()

            stop_times.append(time)

        PATH_CACHE[cache_key] = {
            "time" : time,
            "stations" :  stops,
            "stop_times": stop_times,
            "spf" : d,
        }

    return PATH_CACHE[cache_key]
