'''
Author: Eliza Malyshev 
Date:4/13/2024 
HackKU Spring 2024 Tutoring Project; ALC Tutoring webscrapping 
Purpose: directs and gets information from ALC website 
''' 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
import time 

from option import Option 

class ALC: 
    def __init__(self,helpClass,username,password): 
        self.optionsList=[] #dlist of tutoring times
        self.help=helpClass #must by tuple/list/dictionary of EECS,# string, format to be with space 
        self.driver=webdriver.Chrome() #ask for input of which browser, for now just chrome 
        self.openALC()
        self.login()
        self.duo()
        #self.selectClass()
        #self.timeSlot()
        self.findTimes()
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
        elif types=="xpath": 
            types=By.XPATH
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
        
    '''clicks "dont trust computer" button on DUO to avoid security issues'''
    def duo(self): 
        self.wait(30,"ID","dont-trust-browser-button")
        self.driver.find_element(By.ID,"dont-trust-browser-button").click()
    
    '''iterates through every row tr and looks for araia-label="Open/Available..." and selects it'''
    def selectClass(self): 
        self.wait(10,"ID","limfoc")
        classInput=self.driver.find_element(By.ID,"limfoc") #instead of EECS 268 or whatever put self.help
        classInput.send_keys("EECS 168"+Keys.ENTER)
    
    def findTimes(self):
        self.wait(7,"ID", "sch-table")
        allTables=self.driver.find_elements(By.ID,"sch-table")
        for i in allTables: #get it to iterate over all 6 tables 
            #table = self.driver.find_element(By.ID, "sch-table")
            ALCtimes = i.find_elements(By.TAG_NAME, "tr")
            for row in ALCtimes:
                cols = row.find_elements(By.TAG_NAME, "td")
                for col in cols:
                    tooltip_content = col.get_attribute('data-bs-original-title')
                    if tooltip_content:
                        # Extracting the desired information from the tooltip content
                        appointment_info = tooltip_content.split('<strong>')
                        time = appointment_info[1].split('</strong>')[0]
                        date = appointment_info[2].split('</strong>')[0]
                        person = appointment_info[3].split('</strong>')[0]
            
                        print(f"Time:{time}\tDate:{date}\tPerson:{person}")    
    
    '''this actually clicks on the time slot to reserve the appointmnet'''
    '''called from executive only if any times match with the users schedule, let user select which appointment'''
    def timeSlot(self): 
        self.wait(10,"xpath",'//*[@aria-label="Open/Available Appointment Slot"]')
        openSlot = self.driver.find_element(By.CSS_SELECTOR, "td[aria-label='Open/Available Appointment Slot']") #goes into td and looks for aria label specified 
        ActionChains(self.driver).move_to_element(openSlot).click(openSlot).perform() #scrolls/moves to element and clicks it 
        