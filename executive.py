from schedule import Schedule
class Executive:
    def __init__(self):
        self.classes_list = []
        self.options_dict = {}

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
        temp = input("What classes do you need tutoring for? Input in format EECS 140,EECS 268,PHXS 212: ")
        self.classes_list = temp.split(",")
        mySchedule = Schedule(self.user_id, self.user_pass)
        mySchedule.run()
        mySchedule.schedule_list
        #run acm for each class
        #run alc for each class
        #run comparison for each class
        pass

    def comparison(self, schedule_list, acm_list, alc_list):
        #returns a list with all valid times
        pass

def main():
    myExec = Executive()
    myExec.run()

main()