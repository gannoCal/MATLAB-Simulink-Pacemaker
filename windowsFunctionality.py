#A file filled with classes relating to the functionality needed for each of the windows in the windows file. This
#includes any functionality related to pressing a button or needed other functionality like text boxes.

from tkinter import *
import windows#Import the windows.py file
import threading
import time
import struct
import serial

currentMode = ''
rMode=False#Boolean for if we are using r-mode
portOpen = False
#lowerRateLimitInput,upperRateLimitInput,atrialAmplitudeInput,atrialPulseWidthInput,ventricularAmplitudeInput,ventricularPulseWidthInput,VRPInput,ARPInput
AOOData = [60, 120, 3.5, 0.4, -1, -1, -1, 250]
VOOData = [60, 120, -1, -1, 3.5, 0.4, 320, -1]
AAIData = [60, 120, 3.5, 0.4, -1, -1, -1, 250]
VVIData = [60, 120, -1, -1, 3.5, 0.4, 320, -1]
DOOData = [60, 120, 3.5, 0.4, 3.5, 0.4, 320, 250]

def transmitSerial():
    global portOpen
    global AOOData
    global VOOData
    global AAIData
    global VVIData
    global DOOData
    global currentMode
    global rMode

    while True:
        print('R-mode?: '+str(rMode))
        #print(str(AOOData),str(VOOData),str(AAIData),str(VVIData),str(DOOData))
        if (portOpen == False):
            try:
                s1 = serial.Serial('/dev/tty.usbmodem1412', 115200)
                failed = False
                portOpen = True
            except:
                #print('Port 1 did not open.')
                try:
                    s1 = serial.Serial('/dev/tty.usbmodem1422', 115200)
                    failed = False
                    portOpen = True
                except:
                    failed = True
                    #print('Port 2 did not open.')

        if (failed == False):
            if (currentMode == 'AOO'):
                value = struct.pack(('f'*10), AOOData[0], AOOData[1], AOOData[2], AOOData[3], AOOData[7], 1, 0, 0, 0, rMode)
            elif (currentMode == 'VOO'):
                value = struct.pack(('f'*10)+'B', VOOData[0], VOOData[1], VOOData[4], VOOData[5], VOOData[6], 2, 0, 0, 0, rMode)
            elif (currentMode == 'AAI'):
                value = struct.pack(('f'*10)+'B', AAIData[0], AAIData[1], AAIData[2], AAIData[3], AAIData[7], 3, 0, 0, 0, rMode)
            elif (currentMode == 'VOO'):
                value = struct.pack(('f'*10)+'B', VVIData[0], VVIData[1], VVIData[4], VVIData[5], VVIData[6], 4, 0, 0, 0, rMode)
            elif (currentMode == 'DOO'):
                value=struct.pack(('f'*10)+'B', DOOData[0], DOOData[1], DOOData[2], DOOData[3], DOOData[4], DOOData[5], DOOOata[6], DOOData[7], 5, rMode)
            try:
                s1.write(value)
                portOpen = True
            except:
                portOpen = False


        time.sleep(0.1)


class loginAndRegistrationWindowsFunctionality:#A parent class to hold the functionality that is necessary to both the
    #login and registration functionalities, along with the login and registration classes themselves.

    #Class variables
    username=''#To store the username and password currently on screen. Updated when the user attempts to login or register.
    password=''
    thread=''#Initialize the thread that we will be using to constantly check what the user has inputted for login/registration
    #credentials on the screen.
    n=1

    # Attain data from the login info sheet. This data is relevant to all login and registration-related methods.
    loginInfoFile = 'pacemakerLogins.txt'
    with open(loginInfoFile) as f:  # Open the loginInfoFile to read from
        fileData = f.readlines()  # Read datasheet
        numLines = len(fileData)  # Calculate the number of lines in the sheet
        usernamesFromSheet = []  # Starting list of all usernames in the sheet
        passwordsFromSheet = []  # Starting list of all passwords in the sheet
        for index in range((int)(numLines / 2)):  # Index ranging up to half of the number of lines (as we will be
            # observing both the usernames and passwords and considering them to be one pairing, even though they
            # take up 2 lines)
            usernamesFromSheet.append(fileData[index * 2].rstrip())  # Append the usernames from the sheet to usernamesFromSheet list.
            # NOTE: This is helpful because now we have two seperate lists containing the usernames and passwords, respectively.
            # This means that we can now compare usernames and passwords at the same index (meaning that they are pertaining
            # to the same user)
            passwordsFromSheet.append(fileData[(index * 2) + 1].rstrip())  # Append the usernames from the sheet to passwordsFromSheet list

    #Class methods for all login and registry-related functionalities
    def createThread(self,usernameEntry,passwordEntry):
        thread = threading.Thread(target=loginAndRegistrationWindowsFunctionality.updateUsernameAndPassword,args=(self, usernameEntry, passwordEntry))
        thread.daemon = True  # Make thread a daemon (runs in background)
        return thread
    def setCurrentUsername(self,username):#To set the username for the whole class to the one that is currently on-screen
        #incase it needs to be used again.
        loginAndRegistrationWindowsFunctionality.username=username
    def setCurrentPassword(self,password):
        loginAndRegistrationWindowsFunctionality.password=password
    def updateUsernameAndPassword(self,usernameEntry,passwordEntry):
        print('Updating username&password')
        loginAndRegistrationWindowsFunctionality.n = 1
        while (loginAndRegistrationWindowsFunctionality.n > 0):
            #print('Updating username & password')
            #if (is_exe(usernameEntry) and is_exe(passwordEntry)):
            try:
                loginAndRegistrationWindowsFunctionality.username = usernameEntry.get()
                loginAndRegistrationWindowsFunctionality.password = passwordEntry.get()
            except:
                print('DNE')
            time.sleep(0.1)#0.01 second delay between username and password updates
            # if (loginAndRegistrationWindowsFunctionality.n == 1):
            #     break
        # if (loginAndRegistrationWindowsFunctionality.n==1):
        #     return
        print('Joining!')
        loginAndRegistrationWindowsFunctionality.thread.join()
    def usernameAndPasswordEntries(self,root):
        usernameLabel = Label(root, text='Username: ')  # Username text
        usernameLabel.grid(row=1, column=1, sticky=W)  # Username text organization
        usernameEntry = Entry(root)  # Username entry text
        usernameEntry.grid(row=1, column=2, sticky=E)  # Username entry text organization
        passwordLabel = Label(root, text='Password: ')  # Password text
        passwordLabel.grid(row=2, column=1, sticky=W)  # Password text organization
        passwordEntry = Entry(root, show='*')  # Password entry text
        passwordEntry.grid(row=2, column=2, sticky=E)  # Password entry text organization
        loginAndRegistrationWindowsFunctionality.thread=loginAndRegistrationWindowsFunctionality.createThread(self,usernameEntry,passwordEntry)
        loginAndRegistrationWindowsFunctionality.thread.start()
    class loginWindowsFunctionality:
        def fillLoginWindow(self, lWindow):#Fills the login window with necessary pieces (e.g. text, buttons, etc.)
            print('Filling login window')#For debugging
            loginAndRegistrationWindowsFunctionality.usernameAndPasswordEntries(self,lWindow)
            loginButton=Button(lWindow, text='Login', fg='Black', command=lambda: loginAndRegistrationWindowsFunctionality.loginWindowsFunctionality.login(self,lWindow))
            loginButton.grid(row=3, column=1, columnspan=2, sticky=S)
            registrationLabel=Label(lWindow, text="Don't have a login? Register here-->")
            registrationLabel.grid(row=4, column=1, sticky=W)
            registrationButton=Button(lWindow, text='Register', fg='Black', command=lambda: windows.windowsRegister.registerWindow(self, lWindow))
            registrationButton.grid(row=4, column=2, sticky=E)
        def matchingUsernameAndPassword(self, currentUsername,currentPassword):  # To check if there exists a user who has the combination of username
            # and password that the user has entered.
            for j in range(len(loginAndRegistrationWindowsFunctionality.usernamesFromSheet)):  # Check all usernames for login equality
                if (str(loginAndRegistrationWindowsFunctionality.usernamesFromSheet[j]) == str(currentUsername)):  # If username at the current index matches the username
                    # entered by the user
                    if (str(loginAndRegistrationWindowsFunctionality.passwordsFromSheet[j]) == str(currentPassword)):  # Only accepts login if username and password come
                        # from same index. This stops someone else's password from being used with a given username
                        return TRUE
            return FALSE  # If the end of this function is reached, it means that there is no user with the login credentials
            # entered by the user (meaning that we can go ahead and return a false value)
        def login(self, lWindow):#Method used to check if we will log the user in given the information that they have entered.
            print('Login attempt made')
            print('Username: '+loginAndRegistrationWindowsFunctionality.username+'Password: '+loginAndRegistrationWindowsFunctionality.password)
            if(loginAndRegistrationWindowsFunctionality.loginWindowsFunctionality.matchingUsernameAndPassword(self,loginAndRegistrationWindowsFunctionality.username,loginAndRegistrationWindowsFunctionality.password)):
                windows.windowsDCM.DCMWindow(self,lWindow)
            else:
                errorWindow=Tk()
                errorWindow.title('Error!')
                errorWindowLabel=Label(errorWindow, text='You entered invalid login credentials!')
                errorWindowLabel.grid(row=1, column=1)
                errorWindow.mainloop()

    class registrationWindowsFunctionality:
        def fillRegistrationWindow(self, rWindow):
            print('Filling registration window')
            loginAndRegistrationWindowsFunctionality.n=0
            #loginAndRegistrationWindowsFunctionality.thread.join()
            loginAndRegistrationWindowsFunctionality.usernameAndPasswordEntries(self,rWindow)
            backButton = Button(rWindow, text='Go Back', fg='Black', command=lambda: [windows.windowsLogin.loginWindow(self,rWindow)])
            backButton.grid(row=3, column=1, columnspan=2, sticky=W)
            registrationButton = Button(rWindow, text='Register', fg='Black', command=lambda: loginAndRegistrationWindowsFunctionality.registrationWindowsFunctionality.register(self, rWindow))
            registrationButton.grid(row=3, column=1, columnspan=2, sticky=E)

        def validLogin(usernameOrPassword):
            for index in range(len(usernameOrPassword)):
                if (ord(usernameOrPassword[index]) < 48 or (
                        ord(usernameOrPassword[index]) > 57 and ord(usernameOrPassword[index]) < 65) or (
                        ord(usernameOrPassword[index]) > 90 and ord(usernameOrPassword[index]) < 97) or ord(
                        usernameOrPassword[index]) > 122):
                    return False
            return True

        def userAlreadyExists(self):
            usernameExists = False
            loginInfoFile='pacemakerLogins.txt'
            readFile = open(loginInfoFile, 'r')
            numLines = len(readFile.readlines())

            with open(loginInfoFile) as f:  # Open the loginInfoFile to read from
                fileData = f.readlines()  # Read datasheet
                # usernamesFromSheet = []  # Starting list of all usernames in the sheet
                for index in range(
                        (int)(numLines / 2)):  # Index ranging up to half of the number of lines (as we will be
                    # observing both the usernames and passwords and considering them to be one pairing, even though they
                    # take up 2 lines)
                    # usernamesFromSheet.append(fileData[index * 2].rstrip())  # Append the usernames from the sheet to usernamesFromSheet list.
                    if (loginAndRegistrationWindowsFunctionality.username == fileData[index * 2].rstrip()):
                        usernameExists = True

            return usernameExists

        def writeToSheet(self,rWindow):
            loginInfoFile = 'pacemakerLogins.txt'
            file = open(loginInfoFile, 'a')
            if (loginAndRegistrationWindowsFunctionality.username == '' and loginAndRegistrationWindowsFunctionality.password == ''):
                failWindow = Tk()
                failWindow.title('Failed to register')
                failMessage = Label(failWindow, text='Can not create a user with no credentials.')
                failMessage.grid(row=1, sticky=W)
                return  # Escape the function so that the remaining parts do not happen
            elif (loginAndRegistrationWindowsFunctionality.username == ''):
                failWindow = Tk()
                failWindow.title('Failed to register')
                failMessage = Label(failWindow, text='Can not create a user with no username.')
                failMessage.grid(row=1, sticky=W)
                return  # Escape the function so that the remaining parts do not happen
            elif (loginAndRegistrationWindowsFunctionality.password == ''):
                failWindow = Tk()
                failWindow.title('Failed to register')
                failMessage = Label(failWindow, text='Can not create a user with no password.')
                failMessage.grid(row=1, sticky=W)
                return  # Escape the function so that the remaining parts do not happen
            elif (loginAndRegistrationWindowsFunctionality.registrationWindowsFunctionality.userAlreadyExists(self)):
                failWindow = Tk()
                failWindow.title('Failed to register')
                failMessage = Label(failWindow, text='A user with this username already exists.')
                failMessage.grid(row=1, sticky=W)
            elif (loginAndRegistrationWindowsFunctionality.registrationWindowsFunctionality.validLogin(loginAndRegistrationWindowsFunctionality.username) != True or loginAndRegistrationWindowsFunctionality.registrationWindowsFunctionality.validLogin(
                    loginAndRegistrationWindowsFunctionality.password) != True):
                failWindow = Tk()
                failWindow.title('Failed to register')
                failMessage = Label(failWindow,
                                    text='An invalid character was found within the username and/or password that you entered.')
                failMessage.grid(row=1, sticky=W)
            elif(len(loginAndRegistrationWindowsFunctionality.password)<6):
                failWindow = Tk()
                failWindow.title('Failed to register')
                failMessage = Label(failWindow,
                                    text='The password you entered was too short')
                failMessage.grid(row=1, sticky=W)
            else:
                successWindow = Tk()
                successWindow.title('Registered!')
                successMessage = Label(successWindow, text='Congratulations. Registration successful')
                successMessage.grid(row=1, sticky=W)
                file.write('\n' + loginAndRegistrationWindowsFunctionality.username + '\n' + loginAndRegistrationWindowsFunctionality.password)
                file.close()
                rWindow.destroy()
                # loginAndRegistrationWindowsFunctionality.registrationWindowsFunctionality.writeToSheet(self, rWindow)
                windows.windowsDCM.DCMWindow(self, rWindow)
        def register(self, rWindow):
            print('Registration attempt made')
            print('Username: '+loginAndRegistrationWindowsFunctionality.username+'Password: '+loginAndRegistrationWindowsFunctionality.password)
            loginAndRegistrationWindowsFunctionality.registrationWindowsFunctionality.writeToSheet(self,rWindow)
            #windows.windowsDCM.DCMWindow(self, rWindow)

class DCMWindowsFunctionality:
    #Class Variables
    currentData = [0,0,0,0,0,0,0,0]
    ###Data for each of the pacing modes###
    # NOTE: These must be stored globally so that they may be accessed between windows
    # NOTE: -1 denotes an area that will not be editable, as it is not associated with said mode.
    # As a result of this, it will be greyed out and not have the ability to be edited when shown
    # on the DCM.
    # Data order:


    #Class Methods
    def importSettings(self,windowName,lowerRateLimitInput,upperRateLimitInput,atrialAmplitudeInput,atrialPulseWidthInput,ventricularAmplitudeInput,ventricularPulseWidthInput,VRPInput,ARPInput):
        # Get the global arrays of input info
        global AOOData
        global VOOData
        global AAIData
        global VVIData
        global DOOData

        inputModeSettingsSheet = 'inputModeSettings.txt'
        with open(inputModeSettingsSheet) as settingsData:
            settings = settingsData.readlines()
            # previousData=[]
            importData = ''

            def parseToInt(data):  # Convert parsed data from individual char values to ints
                for i in range(len(data)):
                    data[i] = float(data[i])
                return data

            if (windowName == 'AOO'):
                # previousData=AOOData[:]#Stores a copy of the previous AOOData list incase the user wants to revert when prompted
                importData = settings[0].split(',')
                # importData=parseToInt(importData)
                # AOOData = importData[:]
            elif (windowName == 'VOO'):
                # previousData=VOOData[:]
                importData = settings[1].split(',')
                # importData=parseToInt(importData)
                # VOOData=importData[:]
            elif (windowName == 'AAI'):
                # previousData = AAIData[:]
                importData = settings[2].split(',')
                # importData=parseToInt(importData)
                # AAIData=importData[:]
            elif (windowName == 'VVI'):
                # previousData=VVIData[:]
                importData = settings[3].split(',')
                # importData=parseToInt(importData)
                # VVIData=importData[:]
            elif (windowName == 'DOO'):
                importData = settings[4].split(',')
            # print(AOOData, importData, type(importData[0]), type(1))

            importData = parseToInt(importData)

            lowerRateLimitInput.delete(0, END)
            lowerRateLimitInput.insert(END, importData[0])
            upperRateLimitInput.delete(0, END)
            upperRateLimitInput.insert(END, importData[1])
            atrialAmplitudeInput.delete(0, END)
            atrialAmplitudeInput.insert(END, importData[2])
            atrialPulseWidthInput.delete(0, END)
            atrialPulseWidthInput.insert(END, importData[3])
            ventricularAmplitudeInput.delete(0, END)
            ventricularAmplitudeInput.insert(END, importData[4])
            ventricularPulseWidthInput.delete(0, END)
            ventricularPulseWidthInput.insert(END, importData[5])
            VRPInput.delete(0, END)
            VRPInput.insert(END, importData[6])
            ARPInput.delete(0, END)
            ARPInput.insert(END, importData[7])

    def updateInputModeInfo(self,windowName,lowerRateLimitInput,upperRateLimitInput,atrialAmplitudeInput,atrialPulseWidthInput,ventricularAmplitudeInput,ventricularPulseWidthInput,VRPInput,ARPInput):
        #print('Current data list: ' + str(DCMWindowsFunctionality.currentData[0]) + ' ' + str(
        #    DCMWindowsFunctionality.currentData[1]) + ' ' + str(DCMWindowsFunctionality.currentData[2]) + ' ' + str(
        #    DCMWindowsFunctionality.currentData[3]) + ' ' + str(DCMWindowsFunctionality.currentData[4]) + ' ' + str(
        #    DCMWindowsFunctionality.currentData[5]) + ' ' + str(DCMWindowsFunctionality.currentData[6]) + ' ' + str(
        #    DCMWindowsFunctionality.currentData[7]))
        DCMWindowsFunctionality.currentData[0]=lowerRateLimitInput
        DCMWindowsFunctionality.currentData[1]=upperRateLimitInput
        DCMWindowsFunctionality.currentData[2]=atrialAmplitudeInput
        DCMWindowsFunctionality.currentData[3]=atrialPulseWidthInput
        DCMWindowsFunctionality.currentData[4]=ventricularAmplitudeInput
        DCMWindowsFunctionality.currentData[5]=ventricularPulseWidthInput
        DCMWindowsFunctionality.currentData[6]=VRPInput
        DCMWindowsFunctionality.currentData[7]=ARPInput
        newInputModeInfo = DCMWindowsFunctionality.currentData
        # The information applied to the selected input mode once the update button is pressed

        # Get the global arrays of input info
        global AOOData
        global VOOData
        global AAIData
        global VVIData
        global DOOData

        def valueRangeCheck(newInputModeInfo):#Returns true if all values are in proper range
            #For lower rate  limit
            print(newInputModeInfo)
            for index in range(8):  # Loop to convert empty values to '-1' for the next time the program is run (will not work
            # without doing this)
                if(newInputModeInfo[index]==''):
                    newInputModeInfo[index]='-1'
            if((float(newInputModeInfo[0])<-1) or ((float(newInputModeInfo[0])>=0) and (float(newInputModeInfo[0])<30)) or (float(newInputModeInfo[0])>175)):
                return False
            elif((float(newInputModeInfo[1])<-1) or ((float(newInputModeInfo[1])>=0) and (float(newInputModeInfo[1])<50)) or (float(newInputModeInfo[1])>175)):
                return False
            elif((float(newInputModeInfo[2])<-1) or ((float(newInputModeInfo[2])>=0) and (float(newInputModeInfo[2])<0.5)) or ((float(newInputModeInfo[2])>=3.2) and (float(newInputModeInfo[2])<3.5)) or (float(newInputModeInfo[2])>7)):
                return False
            elif((float(newInputModeInfo[3])<-1) or ((float(newInputModeInfo[3])>=0) and (float(newInputModeInfo[3])<0.05)) or ((float(newInputModeInfo[3])>=0.06) and (float(newInputModeInfo[3])<0.1)) or (float(newInputModeInfo[3])>1.9)):
                return False
            elif ((float(newInputModeInfo[4]) < -1) or (
                    (float(newInputModeInfo[4]) >= 0) and (float(newInputModeInfo[4]) < 0.5)) or (
                          (float(newInputModeInfo[4]) >= 3.2) and (float(newInputModeInfo[4]) < 3.5)) or (
                          float(newInputModeInfo[4]) > 7)):
                return False
            elif ((float(newInputModeInfo[5]) < -1) or (
                    (float(newInputModeInfo[5]) >= 0) and (float(newInputModeInfo[5]) < 0.05)) or (
                          (float(newInputModeInfo[5]) >= 0.06) and (float(newInputModeInfo[5]) < 0.1)) or (
                          float(newInputModeInfo[5]) > 1.9)):
                return False
            elif ((float(newInputModeInfo[6]) < -1) or (
                    (float(newInputModeInfo[6]) >= 0) and (float(newInputModeInfo[6]) < 150)) or (
                    float(newInputModeInfo[6]) > 500)):
                return False
            elif ((float(newInputModeInfo[7]) < -1) or (
                    (float(newInputModeInfo[7]) >= 0) and (float(newInputModeInfo[7]) < 150)) or (
                    float(newInputModeInfo[7]) > 500)):
                return False
            return True

        if (valueRangeCheck(newInputModeInfo)):
            if (windowName == 'AOO'):
                AOOData = newInputModeInfo
            elif (windowName == 'VOO'):
                VOOData = newInputModeInfo
            elif (windowName == 'AAI'):
                AAIData = newInputModeInfo
            elif (windowName == 'VVI'):
                VVIData = newInputModeInfo
            elif (windowName == 'DOO'):
                DOOData = newInputModeInfo
        else:
            errorWindow=Tk()
            errorWindow.title('Error!')
            errorText=Label(errorWindow, text='One of the values that you tried to give was not in the proper range!')
            errorText.grid(row=1, column=1)
            errorWindow.mainloop()
        settingsData = open('inputModeSettings.txt', 'w')
        for index in range (8):#Loop to convert empty values to '-1' for the next time the program is run (will not work
             #without doing this)
             if(AOOData[index]==''):
                 AOOData[index]='-1'
             if (VOOData[index] == ''):
                 VOOData[index] = '-1'
             if (AAIData[index] == ''):
                 AAIData[index] = '-1'
             if (VVIData[index] == ''):
                 VVIData[index] = '-1'
             if (DOOData[index] == ''):
                 DOOData[index] = '-1'

        #print('\n\n\n\n\n\n\n\n\n\n\n'+newInputModeInfo+'\n\n\n\n\n\n\n\n\n\n\n')

        settingsData.write(str(AOOData[0])+','+str(AOOData[1])+','+str(AOOData[2])+','+str(AOOData[3])+','+str(AOOData[4])+','+str(AOOData[5])+','
                           +str(AOOData[6])+','+str(AOOData[7])+'\n'+str(VOOData[0])+','+str(VOOData[1])+','+str(VOOData[2])+','+str(VOOData[3])+','
                           +str(VOOData[4])+','+str(VOOData[5])+','+str(VOOData[6])+','+str(VOOData[7])+'\n'+str(AAIData[0])+','+str(AAIData[1])+','
                           +str(AAIData[2])+','+str(AAIData[3])+','+str(AAIData[4])+','+str(AAIData[5])+','+str(AAIData[6])+','+str(AAIData[7])+'\n'
                           +str(VVIData[0])+','+str(VVIData[1])+','+str(VVIData[2])+','+str(VVIData[3])+','+str(VVIData[4])+','+str(VVIData[5])+','
                           +str(VVIData[6])+','+str(VVIData[7])+'\n'+str(DOOData[0])+','+str(DOOData[1])+','+str(DOOData[2])+','+str(DOOData[3])+','
                           +str(DOOData[4])+','+str(DOOData[5])+','+str(DOOData[6])+','+str(DOOData[7]))

    def parameterInputData(self,windowName):
        global AOOData
        global VOOData
        global AAIData
        global VVIData
        global DOOData

        parameterInputDataInterface = Tk()
        parameterInputDataInterface.title(windowName)
        parameterInputDataInterface.geometry('1920x1080')
        localInputData = []
        if (windowName == 'AOO'):
            localInputData = AOOData
        elif (windowName == 'VOO'):
            localInputData = VOOData
        elif (windowName == 'AAI'):
            localInputData = AAIData
        elif (windowName == 'VVI'):
            localInputData = VVIData
        elif (windowName == 'DOO'):
            localInputData = DOOData
        ###Input adjustments###
        # Lower Rate Limit
        lowerRateLimitInputLabel = Label(parameterInputDataInterface, text='Lower Rate Limit')
        lowerRateLimitInputLabel.grid(row=4, column=1)
        lowerRateLimitInput = Entry(parameterInputDataInterface)
        lowerRateLimitInput.grid(row=5, column=1)
        if (localInputData[0] == (-1)):
            lowerRateLimitInput.configure(state='disabled')
        else:
            lowerRateLimitInput.insert(END, localInputData[0])
        # Upper Rate Limit
        upperRateLimitInputLabel = Label(parameterInputDataInterface, text='Upper Rate Limit')
        upperRateLimitInputLabel.grid(row=4, column=2)
        upperRateLimitInput = Entry(parameterInputDataInterface)
        upperRateLimitInput.grid(row=5, column=2)
        if (localInputData[1] == (-1)):
            upperRateLimitInput.configure(state='disabled')
        else:
            upperRateLimitInput.insert(END, localInputData[1])
        # Atrial Amplitude
        atrialAmplitudeInputLabel = Label(parameterInputDataInterface, text='Atrial Amplitude')
        atrialAmplitudeInputLabel.grid(row=4, column=3)
        atrialAmplitudeInput = Entry(parameterInputDataInterface)
        atrialAmplitudeInput.grid(row=5, column=3)
        if (localInputData[2] == (-1)):
            atrialAmplitudeInput.configure(state='disabled')
        else:
            atrialAmplitudeInput.insert(END, localInputData[2])
        # Atrial Pulse Width
        atrialPulseWidthInputLabel = Label(parameterInputDataInterface, text='Atrial Pulse Width')
        atrialPulseWidthInputLabel.grid(row=4, column=4)
        atrialPulseWidthInput = Entry(parameterInputDataInterface)
        atrialPulseWidthInput.grid(row=5, column=4)
        if (localInputData[3] == (-1)):
            atrialPulseWidthInput.configure(state='disabled')
        else:
            atrialPulseWidthInput.insert(END, localInputData[3])
        # Ventricular Amplitude
        ventricularAmplitudeInputLabel = Label(parameterInputDataInterface, text='Ventricular Amplitude')
        ventricularAmplitudeInputLabel.grid(row=6, column=1)
        ventricularAmplitudeInput = Entry(parameterInputDataInterface)
        ventricularAmplitudeInput.grid(row=7, column=1)
        if (localInputData[4] == (-1)):
            ventricularAmplitudeInput.configure(state='disabled')
        else:
            ventricularAmplitudeInput.insert(END, localInputData[4])
        # Ventricular Pulse Width
        ventricularPulseWidthInputLabel = Label(parameterInputDataInterface, text='Ventricular Pulse Width')
        ventricularPulseWidthInputLabel.grid(row=6, column=2)
        ventricularPulseWidthInput = Entry(parameterInputDataInterface)
        ventricularPulseWidthInput.grid(row=7, column=2)
        if (localInputData[5] == (-1)):
            ventricularPulseWidthInput.configure(state='disabled')
        else:
            ventricularPulseWidthInput.insert(END, localInputData[5])
        # VRP
        VRPInputLabel = Label(parameterInputDataInterface, text='VRP')
        VRPInputLabel.grid(row=6, column=3)
        VRPInput = Entry(parameterInputDataInterface)
        VRPInput.grid(row=7, column=3)
        if (localInputData[6] == (-1)):
            VRPInput.configure(state='disabled')
        else:
            VRPInput.insert(END, localInputData[6])
        # ARP
        ARPInputLabel = Label(parameterInputDataInterface, text='ARP')
        ARPInputLabel.grid(row=6, column=4)
        ARPInput = Entry(parameterInputDataInterface)
        ARPInput.grid(row=7, column=4)
        if (localInputData[7] == (-1)):
            ARPInput.configure(state='disabled')
        else:
            ARPInput.insert(END, localInputData[7])

        #def getCurrentInputs():#Sets the current value of the currentData list equal to all of the current entries in the entry boxes
        #    print('Current Parameters: '+DCMWindowsFunctionality.parameterInputData().lowerRateLimitInput.get()+' '+upperRateLimitInput.get()+' '+atrialAmplitudeInput.get()+' '+atrialPulseWidthInput.get()+' '+ventricularAmplitudeInput.get()+' '+ventricularPulseWidthInput.get()+' '+VRPInput.get(),ARPInput.get())
        #    DCMWindowsFunctionality.currentData = [lowerRateLimitInput.get(),upperRateLimitInput.get(),atrialAmplitudeInput.get(),atrialPulseWidthInput.get(),ventricularAmplitudeInput.get(),ventricularPulseWidthInput.get(),VRPInput.get(),ARPInput.get()]
        #    time.sleep(0.01)#Sleep for 0.01 seconds before updating again.

        def printLists():
            global AOOData
            global VOOData
            global AAIData
            global VVIData
            global DOOData
            print(str(AOOData),str(VOOData),str(AAIData),str(VVIData),str(DOOData))

        #thread = threading.Thread(target=printLists,args=())
        #thread.daemon = True  # Make thread a daemon (runs in background)
        #thread.start()

        #DCMWindowsFunctionality.updateInputModeInfo(self)

        #DCMWindowsFunctionality.importSettings(self)

        updateButton = Button(parameterInputDataInterface, text='Update Info', fg='Black',command=lambda: [DCMWindowsFunctionality.updateInputModeInfo(self,windowName,lowerRateLimitInput.get(),upperRateLimitInput.get(),atrialAmplitudeInput.get(),atrialPulseWidthInput.get(),ventricularAmplitudeInput.get(),ventricularPulseWidthInput.get(),VRPInput.get(),ARPInput.get()),printLists()])  # Also need to add command so that it actually updates this info
        updateButton.grid(row=8, column=1)

        importButton = Button(parameterInputDataInterface, text='Import Settings', fg='Black', command=lambda: DCMWindowsFunctionality.importSettings(self,windowName,lowerRateLimitInput,upperRateLimitInput,atrialAmplitudeInput,atrialPulseWidthInput,ventricularAmplitudeInput,ventricularPulseWidthInput,VRPInput,ARPInput))
        importButton.grid(row=8, column=2)

    def fillDCMWindow(self,interface):
        ###Pacing mode interface selection###

        pacingModesLabel = Label(interface, text='Pacing Mode Selection')
        pacingModesLabel.grid(row=1, column=1, columnspan=2)
        def AOOWindow():
            global currentMode
            DCMWindowsFunctionality.parameterInputData(self,'AOO')
            currentMode='AOO'
        def VOOWindow():
            global currentMode
            DCMWindowsFunctionality.parameterInputData(self,'VOO')
            currentMode='VOO'
        def AAIWindow():
            global currentMode
            DCMWindowsFunctionality.parameterInputData(self,'AAI')
            currentMode='AAI'
        def VVIWindow():
            global currentMode
            DCMWindowsFunctionality.parameterInputData(self,'VVI')
            currentMode='VVI'
        def DOOWindow():
            global currentMode
            DCMWindowsFunctionality.parameterInputData(self,'DOO')
            currentMode='DOO'
        AOOButton = Button(interface, text='AOO', command=AOOWindow)
        AOOButton.grid(row=2, column=1)
        VOOButton = Button(interface, text='VOO', command=VOOWindow)
        VOOButton.grid(row=2, column=2)
        AAIButton = Button(interface, text='AAI', command=AAIWindow)
        AAIButton.grid(row=3, column=1)
        VVIButton = Button(interface, text='VVI', command=VVIWindow)
        VVIButton.grid(row=3, column=2)
        DOOButton = Button(interface, text='DOO', command=DOOWindow)
        DOOButton.grid(row=4, column=1, columnspan=2)
        rModeCheckboxBool = BooleanVar()  # Create a variable of type BooleanVar to be updated from the checkbox
        def updateRModeVar(rModeCheckboxBool):
            global rMode  # Boolean to represent if we have r-mode enabled or disabled.
            rMode=rModeCheckboxBool.get()
        rModeCheckbox=Checkbutton(interface, text='R-Mode', variable=rModeCheckboxBool, command=lambda: updateRModeVar(rModeCheckboxBool))
        rModeCheckbox.grid(row=5, column=1, columnspan=2)
        ###Communication Status between DCM and Device (board)###
        DCMCommunicationStatusTitleLabel = Label(interface, text='DCM Comms w/ Device')
        DCMCommunicationStatusTitleLabel.grid(row=1, column=3)
        DCMCommunicationStatusLabel = Label(interface, text='OFF')
        DCMCommunicationStatusLabel.grid(row=2, column=3)
        ###Identifier for whether new pacemaker is plugged in###
        def newPacemaker():
            newPacemakerBool = FALSE  # Will actually be whatever the status of whether there is a new pacemaker or not is
            if (newPacemakerBool == TRUE):
                return 'YES'
            else:
                return 'NO'
        newPacemakerTitleLabel = Label(interface, text='Different Pacemaker')
        newPacemakerTitleLabel.grid(row=1, column=4)
        newPacemakerLabel = Label(interface, text=newPacemaker())
        newPacemakerLabel.grid(row=2, column=4)
