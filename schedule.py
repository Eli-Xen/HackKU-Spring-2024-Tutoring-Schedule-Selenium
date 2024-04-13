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
            for j in range(0, len(cols[4])):
                self.schedule_list.append(Option(cols[4][j].strip(), cols[2].text))
                
        for i in range(len(self.schedule_list)-1, -1, -1):
            if self.schedule_list[i].weekday == "":
                self.schedule_list.pop(i) 
        for i in range(len(self.schedule_list)):
            temp = self.schedule_list[i].times
            temp = temp.split("-")
            temp[0] = self.convert24(temp[0].strip())
            temp[1] = self.convert24(temp[1].strip())
            self.schedule_list[i].times = temp[0].strip() + " - " + temp[1].strip()
            
    def convert24(self, time):
        if time[-2] == "A":
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