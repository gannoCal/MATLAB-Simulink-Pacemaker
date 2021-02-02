#A file filled with classes relating to each of the windows that will be needed. The windows themselves, the text and
#the buttons that call the functionality that will be needed. The functionality for each of these windows will be held
#in a seperate file.
from tkinter import *
import windowsFunctionality#To be able to use the methods contained within the windowsFunctionality classes

class windowsStart:
    def welcomeWindow(self,root):
        print('Starting Welcome Window')#Print to bottom for debugging
        root.title('Pacemaker DCM')#Window name
        welcomeLabel = Label(root, text="Welcome to the pacemaker DCM! Please enter your login info!")# Welcome message
        welcomeLabel.grid(row=1,sticky=N)# Assigns label to border
        continueToLoginButton=Button(root, text='Continue to Login', fg='Black', command=lambda: windowsLogin.loginWindow(self,root))
        continueToLoginButton.grid(row=2,sticky=S)

class windowsLogin:
    def loginWindow(self, root):
        print('Opening Login Window')
        lWindow=Tk()#Create a window to hold the login
        lWindow.title('Login')#Window name
        loginWindowsFunctionality=windowsFunctionality.loginAndRegistrationWindowsFunctionality().loginWindowsFunctionality()
        loginWindowsFunctionality.fillLoginWindow(lWindow)#Call the fillLoginWindow method from the loginWindowsFunctionality
        #class.
        root.destroy()  # Destroy the starting window and its mainloop
        lWindow.mainloop()

class windowsRegister:
    def registerWindow(self, root):
        print('Opening Register Window')
        rWindow=Tk()
        rWindow.title('Register')
        registrationWindowsFunctionality = windowsFunctionality.loginAndRegistrationWindowsFunctionality().registrationWindowsFunctionality()
        registrationWindowsFunctionality.fillRegistrationWindow(rWindow)  # Call the fillRegistrationWindow method from the registrationWindowsFunctionality
        root.destroy()
        rWindow.mainloop()

class windowsDCM:
    def DCMWindow(self,root):
        print('Opening DCM Window')
        DCMWindow=Tk()
        DCMWindow.geometry('450x130')
        DCMWindow.title('DCM')
        windowsFunctionality.DCMWindowsFunctionality.fillDCMWindow(self,DCMWindow)
        root.destroy()
        DCMWindow.mainloop()
