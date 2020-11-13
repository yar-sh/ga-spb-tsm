from Station import Station
import json


def dump_stations_to_file(stations:list):
    stations_json = [s.as_dict() for s in stations]

    with open("stations.json", "w") as f:
        json.dump(stations_json, f, indent=4, sort_keys=True)


def load_stations_from_file() -> list:
    with open("stations.json", "r") as f:
        stations = json.load(f)
        stations = [Station.from_dict(s) for s in stations]

        # Correctly link neighboring stations
        for s in stations:
            for n in s.neighbours:
                n.station = stations[n.station - 1]

        return stations
