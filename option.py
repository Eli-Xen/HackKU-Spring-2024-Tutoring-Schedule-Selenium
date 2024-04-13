'''
Author: Lily Brooks-Kanost
Date:4/13/2024 
HackKU Spring 2024 Tutoring Project; ALC Tutoring webscrapping 
Purpose: class instance of the tutoring time information
''' 

class Option:
    def __init__(self, weekday, times, tutorName="", date=None):
        self.weekday = weekday
        self.times = times
        self.tutorName = tutorName
        self.date = date

    def __str__(self):
        return f"{self.weekday}, {self.times}"
