class Time:
    def __init__(self):
        self.minutes = 0
        self.hours = 0

    def from_format(time:str):
        t = Time()
        tokens = time.split("-")
        t.hour = int(tokens[0])
    
        # A weird thing we do. At 3am the subway is most definitely closed, so we consider 1am to be a 25th hours, ie: it is tomorrow
        if t.hour < 3:
            t + 24

        t.minutes = int(tokens[1])

        return t

    def to_format(self) -> str:
        hours = self.hours
        minutes = str(self.minutes).rjust(2, '0')

        if hours >= 24:
            hours -= 24

        



