from tkinter import *
import windows#Import windows.py
import windowsFunctionality#Import windowsFunctionality.py
import threading

loginInfoFile='pacemakerLogins.txt'#Create a variable to store the pacemakerLogins file, containing the login credentials
#of each pacemaker user.
inputSettingsFile='inputModeSettings.txt'#File storing the past input mode settings

global root
root=Tk()#Create the root window that will be used

def main():
    start = windows.windowsStart()
    start.welcomeWindow(root)
    thread = threading.Thread(target=windowsFunctionality.transmitSerial, args=())
    thread.daemon = True
    thread.start()
    root.mainloop()

if __name__=="__main__":
   main()
