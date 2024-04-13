'''
Author: Eliza Malyshev 
KUID: 3122318
Date:4/12/2024 
HackKU Spring 2024 Tutoring Porject; ALC Tutoring webscrapping 
Purpose: directs and gets information from ALC website 
''' 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import time 

class ALC: 
    def __init__(self,studentSchedule=None): 
        self.studentSchedule={}
        self.ALCtimes={} #dictionary f classes to keep day,
        self.driver=webdriver.Chrome() #ask for input of which browser, for now just chrome 
        self.openALC()

        
    '''opens ALC website and clicks schedule an appointmnet button'''
    def openALC(self): 
        self.driver.get("https://learningandwriting.ku.edu/individual-tutoring")
        WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.ID,"section342")))  
        scheduleAppointmentButton=self.driver.find_element(By.ID,"section342") 
        scheduleAppointmentButton.click() 
        time.sleep(30)
    
    