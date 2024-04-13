from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from option import Option

class ACM:
    def __init__(self):
        self.driver = " "
        self.search_class = " "
        self.table_list = []
        self.options_list = []

    def set_up(self):
        #asks user which class they wanna look up
        self.search_class = input("class: ")
        #makes a firefox (best) webdriver
        self.driver = webdriver.Firefox()
        #looks up website
        self.driver.get("https://kuacm.club/tutoring/")

    def search_in_site(self):
        #goes to the dropdown menu n clicks it
        self.driver.find_element(By.ID, "classSelect").click()
        select = Select(self.driver.find_element(By.ID, "classSelect"))
        #selects the user inputted class in the dropdown menu
        #note- dropdown menu contains items like "PHSX 110/111". code won't work
        #for that
        select.select_by_visible_text(self.search_class)
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

    def close(self):
        self.driver.close()
        time.sleep(1)


#will modify... just for testing purposes.
def main():
    has_ran = 0
    while has_ran != 1:
        driver = ACM()
        driver.set_up()
        try:
            driver.search_in_site()
            has_ran += 1
        except:
            print("Class could not be found on ACM tutoring")
            driver.close()
    driver.process_data()
    for i in driver.options_list:
        print(i)
    driver.close()

if __name__ == "__main__":
    main()
