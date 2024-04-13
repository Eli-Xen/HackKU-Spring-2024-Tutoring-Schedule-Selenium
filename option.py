class Option:
    def __init__(self, weekday, times, name, date=None):
        self.weekday = weekday
        self.times = times
        self.name = name
        self.date = date

    def __str__(self):
        return f"{self.weekday}, {self.times}, {self.name}"