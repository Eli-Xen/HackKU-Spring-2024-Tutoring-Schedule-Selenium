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
import calendar

from selenium.common.exceptions import TimeoutException


from option import Option 

class ALC: 
    def __init__(self,helpClass=None,username=None,password=None): 
        self.optionsList=[] #dlist of tutoring times
        self.help=helpClass #must by tuple/list/dictionary of EECS,# string, format to be with space 
        self.driver=webdriver.Chrome() #ask for input of which browser, for now just chrome 
        #self.openALC()
        #self.login()
        #self.duo()
        #self.selectClass()
        #self.timeSlot()
        #self.findTimes()
        self.run()
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
        self.driver.find_element(By.ID,"section342").click()
        
    '''logs into ALC tutoring'''
    def login(self,username=None,password=None): 
        self.wait(5,"ID","username")
        _enterUser=self.driver.find_element(By.ID,"username")
        _enterUser.send_keys("e602m203")
        #_enterUser.send_keys(username)
        _pass=self.driver.find_element(By.ID,"password")
        _pass.send_keys("EliXen!1"+Keys.ENTER)
        #_pass.send_keys(password+Keys.ENTER)
        
    '''clicks "dont trust computer" button on DUO to avoid security issues'''
    def duo(self): 
        self.wait(30,"ID","dont-trust-browser-button")
        self.driver.find_element(By.ID,"dont-trust-browser-button").click()
    
    '''iterates through every row tr and looks for araia-label="Open/Available..." and selects it'''
    def selectClass(self): 
        self.wait(10,"ID","limfoc")
        classInput=self.driver.find_element(By.ID,"limfoc") #instead of EECS 268 or whatever put self.help
        classInput.send_keys(self.help+Keys.ENTER)
    
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
                        #print(appointment_info)
                        time = appointment_info[1].split('</strong>')[0]
                        date = appointment_info[2].split('</strong>')[0]
                        person = appointment_info[3].split('</strong>')[0]
                        
                        weekdate=date.split(" ")
                        month=self._month(weekdate[0])
                        weekdayNum=calendar.weekday(2024,month, int(weekdate[1]))
                        weekday=self._weekday(weekdayNum)
                        option=Option(weekday,time,person,date)
                        self.optionsList.append(option)
    
    def _month(self,month): 
        if month=="January": 
            return 1
        elif month=="February": 
            return 2 
        elif month=="March": 
            return 3 
        elif month=="April": 
            return 4
        elif month=="May": 
            return 5
        elif month=="June": 
            return 6
        elif month=="July": 
            return 7
        elif month=="August": 
            return 8
        elif month=="September": 
            return 9
        elif month=="October": 
            return 10
        elif month=="November": 
            return 11
        elif month=="December": 
            return 12
    def _weekday(self,num): 
        if num==0: 
            return "M" 
        elif num==1: 
            return "T"
        elif num==2: 
            return "W" 
        elif num==3: 
            return "R"
        elif num==4: 
            return "F"
        elif num==5: 
            return "Saturday" 
        elif num==6: 
            return "Sunday"
        
    '''if executive finds there are no matching tutors between this and tutoring schedule it will open another instance and immidietley go to next week and scan that'''
    def nextWeek(self): 
        #here insert rerun of everything till adter duo 
        self.wait(10,"link", "Next Week")
        nextWeek=self.driver.find_element(By.PARTIAL_LINK_TEXT,"Next Week")
        nextWeek.click() 
        self.findTimes()
        return self.optionsList
    
    '''this actually clicks on the time slot to reserve the appointmnet'''
    '''called from executive only if any times match with the users schedule, let user select which appointment'''
    def timeSlot(self,time="1:00 pm",date="April 15",person="Apoorva",instructor="John Gibbons"): 
        #iterates over every table and every row and col in table and tries to find matching tooltip content 
        self.wait(7,"ID", "sch-table")
        allTables=self.driver.find_elements(By.ID,"sch-table")
        for i in allTables: #get it to iterate over all 6 tables 
            #table = self.driver.find_element(By.ID, "sch-table")
            ALCtimes = i.find_elements(By.TAG_NAME, "tr")
            for row in ALCtimes:
                cols = row.find_elements(By.TAG_NAME, "td")
                for col in cols:
                    tooltip_content = col.get_attribute('data-bs-original-title')
                    if tooltip_content: #if tooltip context exists 
                        # Extracting the desired information from the tooltip content
                        appointment_info = tooltip_content.split('<strong>')
                        #print(appointment_info)
                        tool_time = appointment_info[1].split('</strong>')[0]
                        tool_date = appointment_info[2].split('</strong>')[0]
                        tool_person = appointment_info[3].split('</strong>')[0]
                    else: 
                        tool_time = ''
                        tool_date = ''
                        tool_person = ''
                    match=0
                    if time==tool_time: 
                      match+=1 
                    if date==tool_date: 
                        match+=1 
                    if person==tool_person: 
                        match+=1 
                    if match==3: 
                        openSlot = self.driver.find_element(By.CSS_SELECTOR, "td[aria-label='Open/Available Appointment Slot']") #goes into td and looks for aria label specified 
                        ActionChains(self.driver).move_to_element(openSlot).click(openSlot).perform() #scrolls/moves to element and clicks it'''
                        '''works up till here'''
                        
                        
                        try:
                            # Switch frame by id
                            self.driver.switch_to.frame('dynamicIframe')
                            
                                # Now, Click on the button
                            self.driver.find_element(By.ID, 'q2').send_keys(instructor)
  
                            self.time.sleep(10)
                        except TimeoutException:
                            print("Timed out waiting for inputInstructor element to be clickable.")
                            self.time.sleep(10)
                        return 
        
        
    def run(self): 
        self.openALC() #opens website and clicks button 
        self.login() #login
        self.duo() #go through duo 
        #self.selectClass() #this will type class into drop down 
        #self.nextWeek()
        self.findTimes() #this will find all avialable times in the week and put into optionsList as Option instance 
        self.timeSlot() #this will schedule an appointmnet, handled by executive and will be called there, this will be an optional call after every week
        return self.optionsList