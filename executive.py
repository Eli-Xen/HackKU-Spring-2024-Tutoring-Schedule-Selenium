from schedule import Schedule
from acm import ACM
class Executive:
    def __init__(self):
        self.classes_list = []
        self.acm_dict = dict()
        self.alc_dict = dict()

    def password_manager(self):
        i = 0
        try:
            with open("tutoring_passwords.txt", "r") as file:
                for line in file:
                    i += 1
                    if i == 1:
                        self.user_id = line.strip()   
                    else:
                        self.user_pass = line.strip()                 
        except:
            self.user_id = input("Txt file doesn't exist. Please input your KU username: ")
            self.user_pass = input("Please input your KU password: ")
            with open("tutoring_passwords.txt", "w") as file:
                file.write(self.user_id + "\n")
                file.write(self.user_pass)

    def run(self):
        self.password_manager()
        temp = input("What classes do you need tutoring for?\nInput in format EECS 140,EECS 268,PHXS 212 starting with highest priority: ")
        self.classes_list = temp.split(",")
        mySchedule = Schedule(self.user_id, self.user_pass)
        mySchedule.run()
        for i in self.classes_list:
            try:
                myACM = ACM(i)
                myACM.run()
                self.acm_dict[i] = self.comparison(mySchedule.schedule_list, myACM.options_list)
            except:
                myACM.close()
                print(f"ACM Tutoring doesn't offer tutoring for {i} :(") 
        #run alc for each class
        self.pretty_print()   

    def comparison(self, schedule_list, tutoring_list):
        #returns a list with all valid times
        valid_list = []
        #iterate through tutoring_list
        for i in tutoring_list:
            tutoring_time = int(i.times[0:i.times.find(":")] + i.times[i.times.find(":")+1:])
            counter = 0
        #do a counter?
        #if time is invalid (make sure days match), break
            while counter == 0:
                for j in schedule_list:
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

    def pretty_print(self):
        print("Dates/times for ACM Tutoring (held in LEEP2 1328):")
        for key, value in self.acm_dict.items():
            print(f'For {key}:')
            for i in range(0, len(value)):
                if value[i][0] == 'M':
                    print(f'Mondays at {value[i][1]}')
                if value[i][0] == 'T':
                    print(f'Tuesdays at {value[i][1]}')
                if value[i][0] == 'W':
                    print(f'Wednesdays at {value[i][1]}')
                if value[i][0] == 'R':
                    print(f'Thursdays at {value[i][1]}')
                if value[i][0] == 'F':
                    print(f'Fridays at {value[i][1]}')
def main():
    myExec = Executive()
    myExec.run()

main()