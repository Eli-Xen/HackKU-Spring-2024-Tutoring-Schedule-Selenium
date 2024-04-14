from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import time
from option import Option

class Schedule:
    def __init__(self, user_id, user_pass):
        self.driver = " "
        self.schedule_list = []
        self.table_list = []
        self.user_pass = user_pass
        self.user_id = user_id
        

    def set_up(self):
        #makes a Firefox webdriver and looks up the KU Portal website
        self.driver = webdriver.Firefox()
        self.driver.get("https://my.ku.edu/uPortal/f/welcome/normal/render.uP")

    def wait(self,time,types,string): 
        time=int(time)
        string=string.strip() 
        if types=="ID": 
            types=By.ID
        elif types=="class": 
            types=By.CLASS_NAME
        elif types=="link": 
            types=By.PARTIAL_LINK_TEXT
        elif types=="xpath": 
            types=By.XPATH
        WebDriverWait(self.driver,time).until(EC.presence_of_all_elements_located((types,string)))

    def search_in_site(self):
        #Logs in to the KU portal using username and password
        login_link = self.driver.find_element(By.ID, "portalCASLoginLink")
        login_link.click()
        id_form = self.driver.find_element(By.ID, "username")
        id_form.send_keys(self.user_id)
        pass_form = self.driver.find_element(By.ID, "password")
        pass_form.send_keys(self.user_pass + Keys.ENTER)
        self.wait(30,"ID","dont-trust-browser-button")
        self.driver.find_element(By.ID,"dont-trust-browser-button").click()
        #waits for website to load... and clicks on the Schedule button
        time.sleep(5)
        self.driver.find_element(By.ID, "u23l1n230").click()
        time.sleep(10)
        #need to reload page if the schedule doesnt load
        loaded = 0
        while loaded != 1:
            try:
                table = self.driver.find_element(By.CLASS_NAME, "schedule")
                loaded += 1
            except:
                self.driver.refresh()
                time.sleep(10)
        #makes a list from the elements in the table
        self.table_list = table.find_elements(By.TAG_NAME, "tr")


    def process_data(self):
        #skips i[0] because it's titling
        for i in range(1, len(self.table_list)):
            #finds columns in the table
            cols = self.table_list[i].find_elements(By.TAG_NAME, "td")
            #only need [2] and [4]- [2] is times, [4] is days
            cols[4] = cols[4].text.split(",")
            for j in range(0, len(cols[4])):
                self.schedule_list.append(Option(cols[4][j].strip(), cols[2].text))
        #if classes don't have set times, they get kicked out
        for i in range(len(self.schedule_list)-1, -1, -1):
            if self.schedule_list[i].weekday == "":
                self.schedule_list.pop(i) 
        #Converts the times into military time
        for i in range(len(self.schedule_list)):
            temp = self.schedule_list[i].times
            temp = temp.split("-")
            temp[0] = self.convert24(temp[0].strip())
            temp[1] = self.convert24(temp[1].strip())
            self.schedule_list[i].times = temp[0].strip() + " - " + temp[1].strip()

            
    def convert24(self, time):
        #converts to military time so it's easier to compare schedules mathmatically
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
        #the sleep avoids a WinError
        time.sleep(1)

    def run(self):
        #does everything!
        self.set_up()
        self.search_in_site()
        self.process_data()
        self.close()
       

