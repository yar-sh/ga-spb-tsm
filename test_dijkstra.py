from helpers import *
from dijkstrawrap import *


if __name__ == "__main__":
    stations = load_stations_from_file()
    g = build_dijkstra_graph(stations)

    st_from = stations[int(input("From station id: "))-1]
    st_to = stations[int(input("To station id: "))-1]

    path_info = get_path_info(g, stations, st_from, st_to)
    print("Wtt: ", path_info["time"])

    print("Path: ")
    t = 0
    for s in path_info["stations"]:
        new_t = path_info["spf"].get_distance(s.id)
        print(f"t={new_t},", s.flat_str())
        t = new_t


