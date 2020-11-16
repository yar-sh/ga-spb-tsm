from helpers import *
from RouteManager import RouteManager


if __name__ == "__main__":
    stations = load_stations_from_file()
    rm = RouteManager(stations)

    r1 = rm.get_fixed_length_route()
    r2 = rm.get_variable_length_route()

    print(f"Fixed-length route: wtt={r1.get_wtt()}")
    sanity_check_r1 = [ False for s in stations ]
    for s in r1.route_stops:
        print(s.flat_str())
        sanity_check_r1[s.id-1] = True
    print("BAD" if False in sanity_check_r1 else "GOOD")

    #print(f"Variable-length route: wtt={r2.get_wtt()}")
    #sanity_check_r2 = [ False for s in stations ]
    #for s in r2.route_stops:
    #    print(s.flat_str())
    #    sanity_check_r2[s.id-1] = True
    #print("BAD" if False in sanity_check_r2 else "GOOD")


