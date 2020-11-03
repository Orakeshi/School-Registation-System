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
import fileinput #Importing Fileinput to handle replaceing lines in files
import sys #Importing sys for various tasks

from kivy.uix.recycleview import RecycleView

def Refresh(): #Refresh function
    db.load() #Calls the database function Load - This reloads the database


class MainWindow(Screen): #Main window Class - opens when user scanned barcode
    studentid = ObjectProperty(None) #Status ID taken from the label in Kivy file
    CurrentUser = "" #Empty variable - Takes value from Scan window [Users Barcode stored here]

    def searchStudent(self):
        if db.validate(self.studentid.text):
            StudentWindow.CurrentStudent = self.studentid.text
            self.reset()
            sm.current = "studentwindow"

        else:
            self.reset()
            sm.current="main"
            invalidID()

    def onsite(self):
        sm.current = "onsite"

    def offsite(self):
        sm.current = "offsite"

    def lateall(self):
        sm.current = "all"

    def latetransport(self):
        sm.current = "transport"

    def lateoverslept(self):
        sm.current = "overslept"

    def latesick(self):
        sm.current = "sick"

    def lateaccident(self):
        sm.current = "accident"

    def latemedical(self):
        sm.current = "medical"

    def lateother(self):
        sm.current = "other"

    def searchcodes(self):
        sm.current = "list"

    def reset(self):
        self.studentid.text = ""

def invalidID(): #Invalid Barcode function
    pop = Popup(title="Barcode Not Recognised", #Sets title of popup menu
                    content = Label(text="Invalid Student ID."
                                         "\n"
                                         "\n"
                                         "Search Again"), #Validation message - Tells user to scan barcode again
                    size_hint=(None, None), size=(400,400)) #Sets size of popup box - position is set to none
    pop.open() #This opens the variable pop which contains the popup menu

class StudentWindow(Screen):
    studname = ObjectProperty(None)
    studstatus = ObjectProperty(None)
    studlate = ObjectProperty(None)
    studtime = ObjectProperty(None)
    CurrentStudent = ""

    def back(self):
        sm.current = "main"

    def on_enter(self, *args):
        name, status, late, time = db.get_user(self.CurrentStudent)

        self.studname.text = str(name)
        self.studstatus.text = str(status)
        self.studlate.text = str(late)

        if time == "Time":
            self.studtime.text = "Not Late"

        else:
            self.studtime.text = str(time)

class OnSiteWindow(Screen):
    status = ObjectProperty(None)
    onsite = ObjectProperty(None)
    CurrentStatus = "On Site"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[2])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.onsite.text = str(contents)

    def back(self):
        sm.current = "main"

class OffSiteWindow(Screen):
    status = ObjectProperty(None)
    offsite = ObjectProperty(None)
    CurrentStatus = "Off Site"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[2])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.offsite.text = str(contents)

    def back(self):
        sm.current = "main"

class AllWindow(Screen):
    lateall = ObjectProperty(None)
    CurrentStatus = "No"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus not in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[3] + ": " + values[4])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.lateall.text = str(contents)

    def back(self):
        sm.current = "main"

class TransportWindow(Screen):
    latetransport = ObjectProperty(None)
    CurrentStatus = "Transport"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[3] + ": " + values[4])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.latetransport.text = str(contents)

    def back(self):
        sm.current = "main"

class OversleptWindow(Screen):
    lateoverslept = ObjectProperty(None)
    CurrentStatus = "Overslept"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[3] + ": " + values[4])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.lateoverslept.text = str(contents)

    def back(self):
        sm.current = "main"

class SickWindow(Screen):
    latesick = ObjectProperty(None)
    CurrentStatus = "Sick"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[3] + ": " + values[4])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.latesick.text = str(contents)

    def back(self):
        sm.current = "main"

class AccidentWindow(Screen):
    lateaccident = ObjectProperty(None)
    CurrentStatus = "Accident"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[3] + ": " + values[4])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.lateaccident.text = str(contents)

    def back(self):
        sm.current = "main"

class MedicalWindow(Screen):
    latemedical = ObjectProperty(None)
    CurrentStatus = "Medical"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[3] + ": " + values[4])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.latemedical.text = str(contents)

    def back(self):
        sm.current = "main"

class OtherWindow(Screen):
    lateother = ObjectProperty(None)
    CurrentStatus = "Other"

    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            if self.CurrentStatus in line:
                values = line.strip().split(";", 4)
                new = str(values[1] + ": " + values[3] + ": " + values[4])
                file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.lateother.text = str(contents)

    def back(self):
        sm.current = "main"

class ListStudentCode(Screen):
    liststudent = ObjectProperty(None)
    def on_enter(self, *args):
        newfile = open("Students/Students.txt", "r")
        file = open("Students/PlaceHolder.txt", "w")
        for line in newfile:
            values = line.strip().split(";", 4)
            new = str(values[0] + ": " + values[1])
            file.writelines(new+"\n")
        file.close()
        self.work()

    def work(self):
        file = open("Students/PlaceHolder.txt", "r")
        contents = file.read()
        self.liststudent.text = str(contents)

    def back(self):
        sm.current = "main"

class WindowManager(ScreenManager): #This class hold all the windows in
    pass #When script run and class is open pass to next line


kv = Builder.load_file("teacher.kv")  # Load up the kivy style sheet file

sm = WindowManager() #Store the Window manager in a variable called sm
db = DataBase("Students/Students.txt") #Store the python file holding the database in a variable called db

screens = [MainWindow(name="main"), StudentWindow(name="studentwindow"), OnSiteWindow(name="onsite"), OffSiteWindow(name="offsite")
           , AllWindow(name="all"), TransportWindow(name="transport"), OversleptWindow(name="overslept"), SickWindow(name="sick")
           , AccidentWindow(name="accident"), MedicalWindow(name="medical"), OtherWindow(name="other"), ListStudentCode(name="list")] #List of all the current windows and there names they are assigned to
for screen in screens: #Kivy uses widgets to write screens - For the current screen in the list of screens ...
    sm.add_widget(screen) #Write all screens [Create each screen as a widget]

sm.current = "main" #When the script is run the current window displayed is the scan window



class TeacherMainApp(App): #This class hold the entire aplication - the class named "MyMainApp" holds the APP [Whole script]
    def build(self): #This procedure builds the entire app
        return sm # Return the file when building the app

Window.fullscreen = 'auto' #Adjusts the window size to the screen

if __name__ == "__main__":
    TeacherMainApp().run() #Runs the app

