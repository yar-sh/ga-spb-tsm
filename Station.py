from Neighbour import Neighbour

# For now we are assuming operating times 7:00-24:00

class Station:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.name_eng = ""
        self.line = -1
        self.neighbours = []
        #self.time_open = None
        #self.time_close = None

    def flat_str(self) -> str:
        return  f"""id={self.id}, line={self.line}, name={self.name_eng}"""

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "name_eng": self.name_eng,
            "line": self.line,
            "neighbours": [{
                "station" : n.station.id,
                "travel_time" : n.travel_time,
                "travel_interval": n.travel_interval,
                "travel_method": n.travel_method,
            } for n in self.neighbours],
            #"time_open" : self.time_open.to_format(),
            #"time_close" : self.time_close.to_format(),
        }

    def from_dict(data:dict):
        s = Station()
        s.id = data["id"]
        s.name = data["name"]
        s.name_eng = data["name_eng"]
        s.line = data["line"]
        s.neighbours = []

        for n in data["neighbours"]:
            nn = Neighbour()
            nn.station = n["station"]
            nn.travel_interval = n["travel_interval"]
            nn.travel_time = n["travel_time"]
            nn.travel_method = n["travel_method"] if "travel_method" in n else "subway"

            s.neighbours.append(nn)

        return s

    def __str__(self) -> str:
        s = self.flat_str()

        if len(self.neighbours) > 0:
            s += ", neighbours:\n"

        for n in self.neighbours:
            s += f"\tinterval={n.travel_interval}, time={n.travel_time}, method={n.travel_method}, station ==> {n.station.flat_str()}\n"

        return s

