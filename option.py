class Option:
    def __init__(self, weekday, times, tutor_name="", date=None, prof_name = ""):
        self.weekday = weekday
        self.times = times
        self.tutor_name = tutor_name
        self.date = date
        self.prof_name = prof_name

    def __str__(self):
        return f"{self.weekday}, {self.times}"