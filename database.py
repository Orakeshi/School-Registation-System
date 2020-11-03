class DataBase:
    def __init__(self, filename):
        self.filename = filename #Knowing what file to work with
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {} #Loads al data in dictionary which is stored in users

        for line in self.file:
            lanyard, name, status, late, time = line.strip().split(";", 4)
            self.users[lanyard] = (name, status, late, time)
            self.users[status] = (name, status)

        self.file.close()

    def get_user(self, lanyard):
        if lanyard in self.users: #check if lanyward key is in users
            return self.users[lanyard] #If yes return the key
        else:
            return -1 #if not return negative 1 meaning no key


    def validate(self, lanyard):
        if self.get_user(lanyard) != -1: #Check lanyward id exists if not you get -1 meaning no user
            return self.users[lanyard]
            new = self.users[lanyard]

        else:
            return False

    #def save(self):
        #with open(self.filename, "w") as f:
            #for user in self.users:
                #f.write(user + "," + self.users[user][0] + "," + self.users[user][1] + "," + self.users[user][2] + "\n")

