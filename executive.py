from schedule import Schedule
from acm import ACM
from alc import ALC
from tabulate import tabulate

class Executive:
    def __init__(self):
        self.classes_list = []
        self.acm_dict = dict()
        self.alc_dict = dict()

    def password_manager(self):
        i = 0
        try:
            #if you've already used this program, you'll have a passwords file already
            with open("tutoring_passwords.txt", "r") as file:
                for line in file:
                    i += 1
                    if i == 1:
                        self.user_id = line.strip()   
                    else:
                        self.user_pass = line.strip()                 
        except:
            #otherwise, it'll make you a passwords file
            self.user_id = input("Txt file doesn't exist. Please input your KU username: ")
            self.user_pass = input("Please input your KU password: ")
            with open("tutoring_passwords.txt", "w") as file:
                file.write(self.user_id + "\n")
                file.write(self.user_pass)

    def run(self):
        #runs each function
        tutoring_owl = ["          ^...^   ", "         / o,o \  ", "         |):::(|  ",   "       ====w=w=== "   , "------TUTORING_OWL------"]
        for owl in tutoring_owl:
            print(owl)
        self.password_manager()
        #gets student's desired classes
        temp = input("What classes do you need tutoring for?\nInput in format EECS 140,EECS 268,PHXS 212 starting with highest priority: ")
        self.classes_list = temp.split(",")
        #gets student's schedule
        mySchedule = Schedule(self.user_id, self.user_pass)
        mySchedule.run()
        #runs each class through ACM tutoring site and ALC
        for i in self.classes_list:
            try:
                myACM = ACM(i)
                myACM.run()
                self.acm_dict[i] = self.comparison(mySchedule.schedule_list, myACM.options_list)
            except:
                #if the class isn't available, a ValueError will be raised
                myACM.close()
                print(f"ACM Tutoring doesn't offer tutoring for {i} :(")
            myALC = ALC(i, self.user_id, self.user_pass)
            myALC.run()
            if len(myALC.optionsList) > 100:
                #if the class isn't available, program defaults to printing all possible tutoring times
                print(f"ALC Tutoring doesn't offer tutoring for {i} :(")
            else:
                self.alc_dict[i] = self.comparison(mySchedule.schedule_list, myALC.optionsList)   
        #prints ACM and ALC outputs 
        self.table_maker("ACM", self.acm_dict)
        self.table_maker("ALC", self.alc_dict)
        answer = ""
        while answer.lower() != "quit":
            answer = input("Type 'quit' to quit Tutoring_Owl: ")

    def comparison(self, schedule_list, tutoring_list):
        #returns a list with all valid times
        valid_list = []
        #iterates through tutoring_list
        for i in tutoring_list:
            tutoring_time = int(i.times[0:i.times.find(":")] + i.times[i.times.find(":")+1:])
            counter = 0
        #if time is invalid (make sure days match), break
            while counter == 0:
                for j in schedule_list:
                    #if the weekdays match, will compare both times as integers
                    #if tutoring time doesn't overlap with class times, adds it to the valid_list
                    if i.weekday == j.weekday:
                        class_times = j.times.split("-")
                        for k in range(0, len(class_times)):
                            class_times[k] = int(class_times[k][0:class_times[k].find(":")] + class_times[k][class_times[k].find(":")+1:])
                        if class_times[1] > tutoring_time and class_times[0] <= tutoring_time:
                            counter += 1
                            break
                break
            if counter == 0:
                if [i.weekday, i.times] not in valid_list:
                    valid_list.append([i.weekday, i.times])
        #else keep iterating through
        #if time was never marked invalid, add it to the list
        return valid_list

    def table_maker(self, tutoring_type, dict_type):
        #initializes all the rows
        l_row = [tutoring_type]
        m_row = ["Monday"]
        t_row = ["Tuesday"]
        w_row = ["Wednesday"]
        r_row = ["Thursday"]
        f_row = ["Friday"]
        table = [l_row, m_row, t_row, w_row, r_row, f_row]
        #adds each value to the table based on class
        for key in dict_type.keys():
            l_row.append(key)
            for item in dict_type[key]:
                if item[0] == "M":
                    m_row.append(item[1])
                if item[0] == "T":
                    t_row.append(item[1])
                if item[0] == "W":
                    w_row.append(item[1])
                if item[0] == "R":
                    r_row.append(item[1])
                if item[0] == "F":
                    f_row.append(item[1])
            #adds spaces to each row so they are symmetrical
            res = max(table, key = len)
            for i in table:
                if i == res:
                    pass
                else:
                    while len(i) != len(res):
                        i.append(" ")
        #prints the table nicely
        print(tabulate(table, tablefmt="rounded_grid"))
