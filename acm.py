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
        self.options_list = []

    def set_up(self):
        self.search_class = input("class: ")
        self.driver = webdriver.Firefox()
        self.driver.get("https://kuacm.club/tutoring/")

    def search_in_site(self):
        self.driver.find_element(By.ID, "classSelect").click()
        select = Select(self.driver.find_element(By.ID, "classSelect"))
        select.select_by_visible_text(self.search_class)
        self.driver.find_element(By.ID, "schedule")
        table = self.driver.find_element(By.ID, "schedule");
        table_list = table.find_elements(By.TAG_NAME, "tr")
        for i in table_list:
            cols = i.find_elements(By.TAG_NAME, "td")
            for j in range(0, len(cols)): 
                #print(cols[j].text + "\t")
                try:
                    #this is buggy--- can you convert " " to int?
                    print(cols[j].text[0])
                    int(cols[j].text[0])
                    temp_list = [cols[j].text, "M", cols[j+1].text, "T", cols[j+2].text, "W", cols[j+3].text, "H", cols[j+4].text, "F", cols[j+5].text]
                    for k in range(0, len(temp_list)):
                        if temp_list[k].isspace() or len(temp_list[k]) == 1:
                            pass
                        else:
                            self.options_list.append(Option(temp_list[k-1], temp_list[0], temp_list[k]))
                except:
                    pass

    def close(self):
        self.driver.close()

def main():
    driver = ACM()
    driver.set_up()
    driver.search_in_site()
    for i in driver.options_list:
        print(i)
    driver.close()

if __name__ == "__main__":
    main()
