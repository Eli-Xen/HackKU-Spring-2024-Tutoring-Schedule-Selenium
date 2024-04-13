'''
Author: Eliza Malyshev 
Date:4/13/2024 
HackKU Spring 2024 Tutoring Porject; ALC Tutoring webscrapping 
Purpose: directs and gets information from ALC website 
''' 

class Option:
    def __init__(self, weekday, times, name, date=None):
        self.weekday = weekday
        self.times = times
        self.name = name
        self.date = date

    def __str__(self):
        return f"{self.weekday}, {self.times}, {self.name}"
