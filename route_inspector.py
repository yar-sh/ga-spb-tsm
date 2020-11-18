from helpers import *
from Route import Route
from RouteManager import RouteManager
from dijkstrawrap import *

def format_minutes(minutes:int) -> str:
    hour = int(minutes / 60)
    minute = minutes % 60

    return f"{hour}:{str(minute).rjust(2,'0')}"


if __name__ == "__main__":
    stations = load_stations_from_file()
    rm = RouteManager(stations)

    # The best route with wtt=522, tournament selection, ordered crossover, simple_inversion mutation
    #   ADJUSTED NOTES: put 10 right after 14, to have less transfers and walking around
    best_route = Route(rm)
    best_route.route_stops = [stations[id - 1] for id in [20,21,22,23,24,25,26,27,29,60,59,57,58,61,62,63,49,28,41,38,39,40,42,47,48,46,45,44,43,52,55,56,54,53,51,50,11,12,70,71,69,68,67,66,65,64,13,31,33,34,37,36,35,32,30,16,19,18,17,15,14,10,9,8,7,6,5,4,3,2,1]]
    best_route.build_spf()

    print(f"Route's wtt={best_route.get_wtt()}, fitness={best_route.get_fitness()}")

    time_offset = 420 # We want to start the route at 7:00am <=> 420 minutes into the day
    t = 0

    for s in range(len(best_route.route_stops)):

        st_from = best_route.route_stops[s]

        print(f"{format_minutes(time_offset + int(t))}, {st_from.line}, {st_from.name}")
        if s+1 < len(best_route.route_stops):
            st_to = best_route.route_stops[s + 1]
            t += get_path_info(rm.graph, rm.stations, st_from, st_to)["time"]



