import kivy #Importing Kivy which does all the GUI
from kivy.app import App  # Import main app class - does All graphics .. Run method in class
from kivy.uix.label import Label #Importing the Label for the GUI
from kivy.uix.floatlayout import FloatLayout #Importing the floatlayout used for the GUI
from kivy.uix.textinput import TextInput #Importing the Text Input feature for the GUI
from kivy.uix.button import Button # Importing the Button Feature for the GUI
from kivy.uix.widget import Widget #Importing the Widget Feature for the GUI
from kivy.properties import ObjectProperty, NumericProperty, StringProperty #Importing the Different Properties to assign the Label and Buttons as
from kivy.lang import Builder #Importing the Builder to Build the KV file
from kivy.uix.screenmanager import ScreenManager, Screen #Importing the Screen manager to build and manage the screens
from kivy.uix.popup import Popup #Importing the Popup feature for the GUI
from kivy.clock import Clock #Importing the clock function
from functools import partial #Importing the partial function
from kivy.uix.image import Image #Importing the image function to set the background of the windows
from kivy.core.window import Window #Importing the ability to add windows
from database import DataBase #Importing another python code which handles the database
from datetime import datetime, timedelta #Importing the date time feature
from threading import Timer #Importing the Timer for the Reset Students Function
import fileinput #Importing Fileinput to handle replaceing lines in files
import sys #Importing sys for various tasks
from time import time
import time, threading
import schedule

#Divide RGB / 255 to get RGBA decimal

def Reset_Students(): #This function replaces the current students file with a fresh file every day at 15:05
    with open('Students/Students_Reset.txt') as num1, open('Students/Students.txt', 'w') as num2: #Opens both files - The current file is open as Write
        for row in num1: #For all Lines in the original
            num2.write(row) #Replace all lines in original with Current file
    return

schedule.every().day.at("16:00").do(Reset_Students) #Code Below sets a timer - Every day at 16:00 the students details are reset

def Refresh(): #Refresh function
    db.load() #Calls the database function Load - This reloads the database


class ScanWindow(Screen): #This class is the first Window where user scans barcode
    studentid = ObjectProperty(None) #This calls the User input from the kivy file


    def fix(self): #This is the function that is run when the scan barcode button is pressed
        self.studentid.focus = True #On the button release the Text Input focus is set to True

    def nextStep(self): #This function is run when the text from the user input [in kivy file] is entered
        if db.validate(self.studentid.text): #This open the Database and runs the Validate function with the users Lanyard Code
            LateWindow.CurrentUser = self.studentid.text #Setting a variable in the Late window Which holds the curernt users Lanyard code
            MainWindow.CurrentUser = self.studentid.text #Setting a variable in the Main window Which holds the curernt users Lanyard code
            self.reset() #Runs the Reset function - Resets all user inputs
            sm.current = "main" #If the user is int he data base take the user to the main window

        elif self.studentid.text == "090909111":
            self.reset()
            sm.current = "admin"

        else: #IF USER NOT IN DATABASE
            self.reset() #Run Reset function and reset all inputs
            #self.studentid.focus = True
            sm.current = "scan" #Put user back in scan menu
            invalidID() #Runs Invalid ID function with popup menu - Tells user that barcode is invalid

    def reset(self):
        self.studentid.text = "" #Reset function - resets all user inputs on barcode scan

def invalidID(): #Invalid Barcode function
    pop = Popup(title="Barcode Not Recognised", #Sets title of popup menu
                    content = Label(text="Invalid Barcode."
                                         "\n"
                                         "\n"
                                         "Scan Again"), #Validation message - Tells user to scan barcode again
                    size_hint=(None, None), size=(400,400)) #Sets size of popup box - position is set to none
    pop.open() #This opens the variable pop which contains the popup menu

class MainWindow(Screen): #Main window Class - opens when user scanned barcode
    n = ObjectProperty(None) #Label from Kivy file that displays users name
    status = ObjectProperty(None) #Status ID taken from the label in Kivy file
    CurrentUser = "" #Empty variable - Takes value from Scan window [Users Barcode stored here]


    def late(self): #Late function - Late Button
        sm.current = "late" #Takes the user to the Late window

    def signIn(self):#Sign in function - Sign in Button
        file = "Students/Students.txt" #Sets the file to be called
        searchExp = "Off Site" #Sets the file to be called
        replaceExp = "On Site" #Word that will be replacing the current word
        lanyard = self.CurrentUser #Storing the current users lanyard code in this variable
        for line in fileinput.input(file, inplace=1): #For a line in the file
            if str(lanyard) in line: #If the lanyard ID is in the line
                line = line.replace(searchExp,replaceExp) #Replace the line with the 2 Variables set above
            sys.stdout.write(line) #Write the line to the file
            sm.current = "scan" #Set the current window back to scan
            Refresh() #Run the Refresh function that reloads the database

    def signOut(self):#Sign in function - Sign in Button
        file = "Students/Students.txt" #Sets the file to be called
        searchExp = "On Site" #Word to be replaced Set in this variable
        replaceExp = "Off Site" #Word that will be replacing the current word
        lanyard = self.CurrentUser #Storing the current users lanyard code in this variable
        for line in fileinput.input(file, inplace=1): #For a line in the file
            if str(lanyard) in line: #If the lanyard ID is in the line
                line = line.replace(searchExp,replaceExp) #Replace the line with the 2 Variables set above
            sys.stdout.write(line) #Write the line to the file
            sm.current = "scan" #Set the current window back to scan
            Refresh() #Run the Refresh function that reloads the database

    def on_enter(self, *args): #When Menu opened ...
        name, status, late, time = db.get_user(self.CurrentUser) #Get Name and Status from the database using the CurrentUser varaible - Holds the current signed in user

        self.status.text = "You are Currently: " + str(status) #Sets the current Label [Status] as Whatever the users value is from the database
        self.n.text = "Name: " + str(name) #Gets the users name from the database and displays on the Late menu


    def Back(self): #This is the back button in case a User Wants to return to the scan menu
        sm.current = "scan" #Opens Scan menu

class LateWindow(Screen): #Late window class
    CurrentUser = "" #Empty variable - Takes value from Scan window [Users Barcode stored here]

    def Transport(self):#Late function - Transport Button
        file = "Students/Students.txt" #Sets the file to be called
        searchExp = "No" #Word to be searched
        replaceExp = "Transport" #Word that will be replacing the current word
        nowTime = "Time"
        Time = str(datetime.now().time()) #TEST
        lanyard = self.CurrentUser #Storing the current users lanyard code in this variable
        for line in fileinput.input(file, inplace=1): #For a line in the file
            if str(lanyard) in line: #If the lanyard ID is in the line
                line = line.replace(searchExp,replaceExp) #Replace the line with the 2 Variables set above
                line = line.replace(nowTime, str(datetime.now().time()))
            sys.stdout.write(line)#Write the line to the file
            sm.current = "scan" #Set the current window back to scan
            Refresh() #Run the Refresh function that reloads the database

    def Overslept(self):#Late function - Overslept Button
        file = "Students/Students.txt" #Sets the file to be called
        searchExp = "No" #Word to be searched
        replaceExp = "Overslept" #Word that will be replacing the current word
        nowTime = "Time"
        Time = str(datetime.now().time()) #TEST
        lanyard = self.CurrentUser #Storing the current users lanyard code in this variable
        for line in fileinput.input(file, inplace=1): #For a line in the file
            if str(lanyard) in line: #If the lanyard ID is in the line
                line = line.replace(searchExp,replaceExp) #Replace the line with the 2 Variables set above
                line = line.replace(nowTime, str(datetime.now().time()))
            sys.stdout.write(line)#Write the line to the file
            sm.current = "scan" #Set the current window back to scan
            Refresh() #Run the Refresh function that reloads the database

    def Sick(self):#Late function - Sick Button
        file = "Students/Students.txt" #Sets the file to be called
        searchExp = "No" #Word to be searched
        replaceExp = "Sick" #Word that will be replacing the current word
        nowTime = "Time"
        Time = str(datetime.now().time()) #TEST
        lanyard = self.CurrentUser #Storing the current users lanyard code in this variable
        for line in fileinput.input(file, inplace=1): #For a line in the file
            if str(lanyard) in line: #If the lanyard ID is in the line
                line = line.replace(searchExp,replaceExp) #Replace the line with the 2 Variables set above
                line = line.replace(nowTime, str(datetime.now().time()))
            sys.stdout.write(line)#Write the line to the file
            sm.current = "scan" #Set the current window back to scan
            Refresh() #Run the Refresh function that reloads the database

    def Accident(self):#Late function - Accident Button
        file = "Students/Students.txt" #Sets the file to be called
        searchExp = "No" #Word to be searched
        replaceExp = "Accident" #Word that will be replacing the current word
        nowTime = "Time"
        Time = str(datetime.now().time()) #TEST
        lanyard = self.CurrentUser #Storing the current users lanyard code in this variable
        for line in fileinput.input(file, inplace=1): #For a line in the file
            if str(lanyard) in line: #If the lanyard ID is in the line
                line = line.replace(searchExp,replaceExp) #Replace the line with the 2 Variables set above
                line = line.replace(nowTime, str(datetime.now().time()))
            sys.stdout.write(line)#Write the line to the file
            sm.current = "scan" #Set the current window back to scan
            Refresh() #Run the Refresh function that reloads the database

    def Medical(self):#Late function - Medical Button
        file = "Students/Students.txt" #Sets the file to be called
        searchExp = "No" #Word to be searched
        replaceExp = "Medical" #Word that will be replacing the current word
        nowTime = "Time"
        Time = str(datetime.now().time()) #TEST
        lanyard = self.CurrentUser #Storing the current users lanyard code in this variable
        for line in fileinput.input(file, inplace=1): #For a line in the file
            if str(lanyard) in line: #If the lanyard ID is in the line
                line = line.replace(searchExp,replaceExp) #Replace the line with the 2 Variables set above
                line = line.replace(nowTime, str(datetime.now().time()))
            sys.stdout.write(line)#Write the line to the file
            sm.current = "scan" #Set the current window back to scan
            Refresh() #Run the Refresh function that reloads the database

    def Other(self):#Late function - Other Button
        file = "Students/Students.txt" #Sets the file to be called
        searchExp = "No" #Word to be searched
        replaceExp = "Other" #Word that will be replacing the current word
        nowTime = "Time"
        Time = str(datetime.now().time()) #TEST
        lanyard = self.CurrentUser #Storing the current users lanyard code in this variable
        for line in fileinput.input(file, inplace=1): #For a line in the file
            if str(lanyard) in line: #If the lanyard ID is in the line
                line = line.replace(searchExp,replaceExp) #Replace the line with the 2 Variables set above
                line = line.replace(nowTime, str(datetime.now().time()))
            sys.stdout.write(line)#Write the line to the file
            sm.current = "scan" #Set the current window back to scan
            Refresh() #Run the Refresh function that reloads the database



    def Back(self): #Back function linked to back button
        sm.current = "main" #Takes user back to menu if mistake opening

class AdminWindow(Screen):

    def ResetStudent(self):
        Reset_Students()
        sm.current = "scan"

    def Back(self): #Back function linked to back button
        sm.current = "scan" #Takes user back to menu if mistake opening#




class WindowManager(ScreenManager): #This class hold all the windows in
    pass #When script run and class is open pass to next line


kv = Builder.load_file("my.kv")  # Load up the kivy style sheet file

sm = WindowManager() #Store the Window manager in a variable called sm
db = DataBase("Students/Students.txt") #Store the python file holding the database in a variable called db

screens = [ScanWindow(name="scan"), MainWindow(name="main"),LateWindow(name="late"),AdminWindow(name="admin")] #List of all the current windows and there names they are assigned to
for screen in screens: #Kivy uses widgets to write screens - For the current screen in the list of screens ...
    sm.add_widget(screen) #Write all screens [Create each screen as a widget]

sm.current = "scan" #When the script is run the current window displayed is the scan window



class MyMainApp(App): #This class hold the entire aplication - the class named "MyMainApp" holds the APP [Whole script]
    def build(self): #This procedure builds the entire app
        return sm # Return the file when building the app

Window.fullscreen = 'auto' #Adjusts the window size to the screen

if __name__ == "__main__":
    MyMainApp().run() #Runs the app

while True: #While the code is running
    schedule.run_pending() #Run the pending Schdeule
    time.sleep(1) #Run the schedule every second until it is met

#Certain admin barcode opens settings
#Add validation on late - Take picture
#Add inbetween screen - ADD Padding + Make Buttons rounded - Add border maybe
