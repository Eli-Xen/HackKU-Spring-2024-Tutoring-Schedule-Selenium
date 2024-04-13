from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import time
from option import Option
from datetime import datetime

class Schedule:
    def __init__(self):
        self.driver = " "
        self.schedule_list = []
        self.table_list = []
        self.user_pass = ""
        self.user_id = ""

    def set_up(self):
        #makes a firefox (best) webdriver
        self.driver = webdriver.Firefox()
        #looks up website
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
        login_link = self.driver.find_element(By.ID, "portalCASLoginLink")
        login_link.click()
        with open("pass.txt", "r") as file:
            i = 0
            for line in file:
                i += 1
                if i == 1:
                    self.user_id = line.strip()
                else:
                    self.user_pass = line.strip()
        id_form = self.driver.find_element(By.ID, "username")
        id_form.send_keys(self.user_id)
        pass_form = self.driver.find_element(By.ID, "password")
        pass_form.send_keys(self.user_pass + Keys.ENTER)
        self.wait(30,"ID","dont-trust-browser-button")
        self.driver.find_element(By.ID,"dont-trust-browser-button").click()
        #wait for website to load...
        time.sleep(5)
        self.driver.find_element(By.ID, "u23l1n230").click()
        time.sleep(5)
        table = self.driver.find_element(By.CLASS_NAME, "schedule")
        self.table_list = table.find_elements(By.TAG_NAME, "tr")


    def process_data(self):
        #skips 0 because it's titling
        for i in range(1, len(self.table_list)):
            #finds columns in the table
            cols = self.table_list[i].find_elements(By.TAG_NAME, "td")
            #only need [2] and [4]- [2] is times, [4] is days
            cols[4] = cols[4].text.split(",")
            cols[2] = cols[2].text.split("-")
            cols[2][0] = self.convert24(cols[2][0].strip())
            cols[2][1] = self.convert24(cols[2][1].strip())
            cols[2] = cols[2][0] + " - " + cols[2][1]
            for j in range(0, len(cols[4])):
                self.schedule_list.append(Option(cols[4][j].strip(), cols[2]))
        for i in range(len(self.schedule_list)-1, -1, -1):
            if self.schedule_list[i].weekday == "":
                self.schedule_list.pop(i) 
            
    def convert24(self, time):
        # Parse the time string into a datetime object
        t = datetime.strptime(time, '%I:%M:%S %p')
        # Format the datetime object into a 24-hour time string
        return t.strftime('%H:%M:%S')[0:-2]
 

    def close(self):
        self.driver.close()
        time.sleep(1)

def main():
    driver = Schedule()
    driver.set_up()
    driver.search_in_site()
    driver.process_data()
    for i in driver.schedule_list:
        print(str(i))
    driver.close()

if __name__ == "__main__":
    main()