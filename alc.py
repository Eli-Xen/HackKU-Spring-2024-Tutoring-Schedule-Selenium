'''
Author: Eliza Malyshev 
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
        self.login()
        self.duo()
        time.sleep(30)

    '''waits for elements to appear'''
    def wait(self,time,types,string): 
        time=int(time)
        string=string.strip() 
        if types=="ID": 
            types=By.ID
        elif types=="class": 
            types=By.CLASS_NAME
        elif types=="link": 
            types=By.PARTIAL_LINK_TEXT
        WebDriverWait(self.driver,time).until(EC.presence_of_all_elements_located((types,string)))
        
    '''opens ALC website and clicks schedule an appointmnet button'''
    def openALC(self): 
        self.driver.get("https://learningandwriting.ku.edu/individual-tutoring")
        self.wait(5,"ID","section342")
        #WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.ID,"section342")))  
        self.driver.find_element(By.ID,"section342").click()
        #scheduleAppointmentButton.click() 
        
    '''logs into ALC tutoring'''
    def login(self): 
        #_username=input("KU username: ")
        #_password=input("KU password: ")
        #username.strip() 
        #password.strip() 
        #WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.ID,"username")))  
        self.wait(5,"ID","username")
        _enterUser=self.driver.find_element(By.ID,"username")
        _enterUser.send_keys("e602m203")
        _pass=self.driver.find_element(By.ID,"password")
        _pass.send_keys("EliXen!1"+Keys.ENTER)
        
    '''DUO dont trust computer'''
    def duo(self): 
        self.wait(30,"ID","dont-trust-browser-button")
        self.driver.find_element(By.ID,"dont-trust-browser-button").click()
    
    