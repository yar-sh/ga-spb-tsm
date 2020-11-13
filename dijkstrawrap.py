from Station import Station
from dijkstra import Graph, DijkstraSPF


def build_dijkstra_graph(stations: list) -> Graph:
    g = Graph()

    # Build the graph edges
    for s in stations:
        for n in s.neighbours:
            g.add_edge(s.id, n.station.id, n.get_wtt())

    return g


def get_path_info(g: Graph, stations:list, st_from : Station, st_to : Station, existing_spf=None) -> dict:
    d = DijkstraSPF(g, st_from.id) if existing_spf == None else existing_spf

    return {
        "time" : d.get_distance(st_to.id),
        "stations" :  [ stations[id - 1] for id in d.get_path(st_to.id)],
        "spf" : d,
    }
