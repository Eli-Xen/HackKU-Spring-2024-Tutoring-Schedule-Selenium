class Option:
    def __init__(self, weekday, times, tutor_name="", date=None):
        self.weekday = weekday
        self.times = times
        self.tutor_name = tutor_name
        self.date = date

    def __str__(self):
        return f"{self.weekday}, {self.times}"