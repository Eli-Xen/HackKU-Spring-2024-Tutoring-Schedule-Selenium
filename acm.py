from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from option import Option

class ACM:
    def __init__(self, help_class):
        self.driver = " "
        self.table_list = []
        self.options_list = []
        self.help_class = help_class

    def set_up(self):
        #asks user which class they wanna look up
        #makes a firefox (best) webdriver
        self.driver = webdriver.Chrome()
        #looks up website
        self.driver.get("https://kuacm.club/tutoring/")

    def search_in_site(self):
        #goes to the dropdown menu n clicks it
        self.driver.find_element(By.ID, "classSelect").click()
        select = Select(self.driver.find_element(By.ID, "classSelect"))
        #selects the user inputted class in the dropdown menu
        #note- dropdown menu contains items like "PHSX 110/111". code won't work
        #for that
        try:
            select.select_by_visible_text(self.help_class)
        except:
            raise ValueError("ACM tutoring doesn't offer this class")
        #finds the schedule table and puts all the info into a list
        table = self.driver.find_element(By.ID, "schedule")
        self.table_list = table.find_elements(By.TAG_NAME, "tr")
        
    def process_data(self):
        for i in self.table_list:
            #finds columns in the table
            cols = i.find_elements(By.TAG_NAME, "td")
            for j in range(0, len(cols)): 
                try:
                    #if the value starts with a number (this would be times),
                    int(cols[j].text[0])
                    #makes a list with time, days of the week, and names/blank spaces
                    temp_list = [cols[j].text, "M", cols[j+1].text, "T", cols[j+2].text, "W", cols[j+3].text, "R", cols[j+4].text, "F", cols[j+5].text]
                    temp_list[0] = self.convert24(temp_list[0])
                    for k in range(1, len(temp_list)):
                        #if a day of the week, or if it's an empty str, do nothing
                        if  len(temp_list[k]) <= 1:
                            pass
                        else:
                            #otherwise, make an object Option with the info,
                            #and append it to the options_list
                            self.options_list.append(Option(temp_list[k-1], temp_list[0], temp_list[k]))
                except:
                    pass
        return self.options_list

    def convert24(self, time):
        if time[-2].upper() == "A":
            pass
        else:
            temp = time[0:time.find(":")]
            temp = int(temp)
            if temp == 12:
                pass
            else:
                temp += 12
                time = str(temp) + time[time.find(":"):-1]
        return time[0:-2]

    def close(self):
        self.driver.close()
        time.sleep(1)

    def run(self):
        self.set_up()
        self.search_in_site()
        self.process_data()
        self.close()

