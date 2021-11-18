import pyodbc
import os
import hashlib
from prettytable import PrettyTable

#User class to save details of the current User
class User:
    def __init__(self, name, email, privilegeLvl):
        self.name = name
        self.email = email
        self.privilegeLvl = privilegeLvl


#login function   
def login(email, pwd):

    #file read function
    configFile = open('config.txt', 'r')
    lines = configFile.readlines()
    configFile.close()
    count = 0
    login = False
    for line in lines:
        count += 1
        #seperate each data in a row
        data = line.strip().split(",")
        if(data[1] == email and data[2] == pwd.hexdigest()):
            login = True
            print("Login Successful")
            user = User(data[0], data[1], data[3])
            return user
    if(not login):
        print("Invalid email/password")
        return False


#--------------Database Dccess functions--------------

#Patient Database Access functions

def registerPatientDb(firstName, lastName, email, address, phoneNum):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        myUser = (
            (firstName, lastName, email, address, phoneNum),
        )
        cursor.executemany('INSERT INTO Patient ([First Name], [Last Name], [Email Address], [Address], [Phone Number]) VALUES (?,?,?,?,?)', myUser)
        conn.commit()
        print('Data Inserted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def deletePatientDb(patientId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('DELETE FROM Patient WHERE Patient.[Patient ID] = ?', (patientId))
        conn.commit()
        print('Data Deleted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def viewAllPatientsDb():
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Patient')

        patients = []
        for row in cursor.fetchall():
            patients.append(row)
        return patients

    except pyodbc.Error as e:
        print("Error in connection", e)

def viewPatientDb(patientId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Patient  WHERE [Patient].[Patient ID] = ?', (patientId))

        patients = []
        for row in cursor.fetchall():
            patients.append(row)
        return patients

    except pyodbc.Error as e:
        print("Error in connection", e)

def getMyIdDb(email):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT [Patient].[Patient ID] FROM Patient  WHERE [Patient].[Email Address] = ?', (email))

        myId = []
        for row in cursor.fetchall():
            myId.append(row)
        return myId

    except pyodbc.Error as e:
        print("Error in connection", e)


#Drug Prescription Database Access functions

def addDrugPrescriptionDb(patientId, drug, dose):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        drugPrescriptionRecord = (
            (patientId, drug, dose, 'Prescribed'),
        )
        cursor.executemany('INSERT INTO [Drug Prescription] ([Patient ID], [Drug], [Dose], [Status]) VALUES (?,?,?,?)', drugPrescriptionRecord)
        conn.commit()
        print('Data Inserted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def removeDrugPrescriptionDb(drugPrescriptionId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('DELETE FROM [Drug Prescription] WHERE [Drug Prescription].[Drug Prescription ID] = ?', (drugPrescriptionId))
        conn.commit()
        print('Data Deleted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def viewAllDrugPrescriptionsDb():
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT Patient.[Patient ID], Patient.[First Name], Patient.[Last Name], Patient.[Email Address], [Drug Prescription].[Drug Prescription ID], [Drug Prescription].Drug, [Drug Prescription].Dose, [Drug Prescription].Status FROM Patient INNER JOIN [Drug Prescription] ON Patient.[Patient ID] = [Drug Prescription].[Patient ID];')

        drugPrescriptions = []
        for row in cursor.fetchall():
            drugPrescriptions.append(row)
        return drugPrescriptions

    except pyodbc.Error as e:
        print("Error in connection", e)

def viewPatientDrugPrescriptionsDb(patientId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT Patient.[Patient ID], Patient.[First Name], Patient.[Last Name], Patient.[Email Address], [Drug Prescription].[Drug Prescription ID], [Drug Prescription].Drug, [Drug Prescription].Dose, [Drug Prescription].Status FROM Patient INNER JOIN [Drug Prescription] ON Patient.[Patient ID] = [Drug Prescription].[Patient ID] WHERE Patient.[Patient ID] = ?;', (patientId))

        drugPrescriptions = []
        for row in cursor.fetchall():
            drugPrescriptions.append(row)
        return drugPrescriptions

    except pyodbc.Error as e:
        print("Error in connection", e)

def isseDrugPrescriptionDb(drugPrescriptionId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        newStatus = 'Issued'
        cursor.execute('UPDATE [Drug Prescription]  SET [Drug Prescription].[Status] = ? WHERE [Drug Prescription].[Drug Prescription ID] = ?', (newStatus, drugPrescriptionId))
        conn.commit()
        print('Data Inserted')

    except pyodbc.Error as e:
        print("Error in connection", e)


#Lab Test Prescription Database Access functions

def addLabTestPrescriptionDb(patientId, test):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        labTestPrescriptionRecord = (
            (patientId, test, 'Pending'),
        )
        cursor.executemany('INSERT INTO [Lab Test Prescription] ([Patient ID], [Test], [Status]) VALUES (?,?,?)', labTestPrescriptionRecord)
        conn.commit()
        print('Data Inserted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def removeLabTestPrescriptionDb(labTestPrescriptionId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('DELETE FROM [Lab Test Prescription] WHERE [Lab Test Prescription].[Lab Test Prescription ID] = ?', (labTestPrescriptionId))
        conn.commit()
        print('Data Deleted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def viewAllLabTestPrescriptionsDb():
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT Patient.[Patient ID], Patient.[First Name], Patient.[Last Name], Patient.[Email Address], [Lab Test Prescription].[Lab Test Prescription ID], [Lab Test Prescription].Test, [Lab Test Prescription].Status, [Lab Test Prescription].Result FROM Patient INNER JOIN [Lab Test Prescription] ON Patient.[Patient ID] = [Lab Test Prescription].[Patient ID];')

        labTestPrescriptions = []
        for row in cursor.fetchall():
            labTestPrescriptions.append(row)
        return labTestPrescriptions

    except pyodbc.Error as e:
        print("Error in connection", e)

def viewPatientLabTestPrescriptionsDb(patientId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT Patient.[Patient ID], Patient.[First Name], Patient.[Last Name], Patient.[Email Address], [Lab Test Prescription].[Lab Test Prescription ID], [Lab Test Prescription].Test, [Lab Test Prescription].Status, [Lab Test Prescription].Result FROM Patient INNER JOIN [Lab Test Prescription] ON Patient.[Patient ID] = [Lab Test Prescription].[Patient ID] WHERE Patient.[Patient ID] = ?;', (patientId))

        labTestPrescriptions = []
        for row in cursor.fetchall():
            labTestPrescriptions.append(row)
        return labTestPrescriptions

    except pyodbc.Error as e:
        print("Error in connection", e)

def labTestPrescriptionMarkDoneDb(labTestPrescriptionId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        newStatus = 'Done'
        cursor.execute('UPDATE [Lab Test Prescription]  SET [Lab Test Prescription].[Status] = ? WHERE [Lab Test Prescription].[Lab Test Prescription ID] = ?', (newStatus, labTestPrescriptionId))
        conn.commit()
        print('Data Inserted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def addLabTestPrescriptionResultDb(labTestPrescriptionId, result):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('UPDATE [Lab Test Prescription]  SET [Lab Test Prescription].[Result] = ? WHERE [Lab Test Prescription].[Lab Test Prescription ID] = ?', (result, labTestPrescriptionId))
        conn.commit()
        print('Data Inserted')

    except pyodbc.Error as e:
        print("Error in connection", e)


#Sickness Detail Database Access functions

def addSicknessDetailDb(patientId, sickness, description):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        sicknessDetailRecord = (
            (patientId, sickness, description),
        )
        cursor.executemany('INSERT INTO [Sickness Detail] ([Patient ID], [Sickness], [Description]) VALUES (?,?,?)', sicknessDetailRecord)
        conn.commit()
        print('Data Inserted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def removeSicknessDetailDb(sicknessDetailId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('DELETE FROM [Sickness Detail] WHERE [Sickness Detail].[Sickness Detail ID] = ?', (sicknessDetailId))
        conn.commit()
        print('Data Deleted')

    except pyodbc.Error as e:
        print("Error in connection", e)

def viewAllSicknessDetailsDb():
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT Patient.[Patient ID], Patient.[First Name], Patient.[Last Name], Patient.[Email Address], [Sickness Detail].[Sickness Detail ID], [Sickness Detail].Sickness, [Sickness Detail].Description FROM Patient INNER JOIN [Sickness Detail] ON Patient.[Patient ID] = [Sickness Detail].[Patient ID];')

        sicknessDetails = []
        for row in cursor.fetchall():
            sicknessDetails.append(row)
        return sicknessDetails

    except pyodbc.Error as e:
        print("Error in connection", e)

def viewPatientSicknessDetailsDb(patientId):
    try:
        con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.path.dirname(os.path.abspath(__file__))+'\db\MedicalDataProcessingSystemDB.accdb;'
        conn = pyodbc.connect(con_str)

        cursor = conn.cursor()
        cursor.execute('SELECT Patient.[Patient ID], Patient.[First Name], Patient.[Last Name], Patient.[Email Address], [Sickness Detail].[Sickness Detail ID], [Sickness Detail].Sickness, [Sickness Detail].Description FROM Patient INNER JOIN [Sickness Detail] ON Patient.[Patient ID] = [Sickness Detail].[Patient ID] WHERE Patient.[Patient ID] = ?;', (patientId))

        sicknessDetails = []
        for row in cursor.fetchall():
            sicknessDetails.append(row)
        return sicknessDetails

    except pyodbc.Error as e:
        print("Error in connection", e)


#--------------Data Functions--------------

#Patient Data functions

#function to register a patient
def registerPatient(firstName, lastName, email, address, phoneNum):
    registerPatientDb(firstName, lastName, email, address, phoneNum)

#function to delete a patient
def deletePatient(patientId):
    deletePatientDb(patientId)

#function to view all patients
def viewAllPatients():
    rows = viewAllPatientsDb()
    table = PrettyTable(["Patient ID", "First Name", "Last Name", "Email Address", "Address", "Phone Number"])
    for row in rows:           
              table.add_row([row[0],row[1],row[2],row[3],row[4],row[5]]) 
    print(table)

#function to a single patient
def viewPatient(patientId):
    rows = viewPatientDb(patientId)
    table = PrettyTable(["Patient ID", "First Name", "Last Name", "Email Address", "Address", "Phone Number"])
    for row in rows:           
              table.add_row([row[0],row[1],row[2],row[3],row[4],row[5]]) 
    print(table)

#get the patient id for an email
def getMyId(email):
    myId = getMyIdDb(email)
    try:
        return myId[0][0]
    except:
        return None


#Drug Prescription Data functions

#function to add a drug presciption
def addDrugPrescription(patientId, drug, dose):
    addDrugPrescriptionDb(patientId, drug, dose)

#function to remove a drug presciption
def removeDrugPrescription(drugPrescriptionId):
    removeDrugPrescriptionDb(drugPrescriptionId)

#function to view all drug presciptions
def viewAllDrugPrescriptions():
    rows = viewAllDrugPrescriptionsDb()
    table = PrettyTable(["Patient ID", "First Name", "Last Name", "Email Address", "Drug Prescription ID", "Drug", "Dose", "Status"])
    for row in rows:          
              table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]) 
    print(table)

#function to view all drug presciptions of a patient
def viewPatientDrugPrescriptions(patientId):
    rows = viewPatientDrugPrescriptionsDb(patientId)
    table = PrettyTable(["Patient ID", "First Name", "Last Name", "Email Address", "Drug Prescription ID", "Drug", "Dose", "Status"])
    for row in rows:          
              table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]) 
    print(table)

#function to change the state of a drug presciption record from Prescribed to Issued
def isseDrugPrescription(drugPrescriptionId):
    isseDrugPrescriptionDb(drugPrescriptionId)


#Lab Test Prescription Data functions

#function to add a lab test presciption
def addLabTestPrescription(patientId, test):
    addLabTestPrescriptionDb(patientId, test)

#function to remove a lab test presciption
def removeLabTestPrescription(labTestPrescriptionId):
    removeLabTestPrescriptionDb(labTestPrescriptionId)

#function to view all lab test presciptions
def viewAllLabTestPrescriptions():
    rows = viewAllLabTestPrescriptionsDb()
    table = PrettyTable(["Patient ID", "First Name", "Last Name", "Email Address", "Lab Test Prescription ID", "Test", "Status", "Result"])
    for row in rows:          
              table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]) 
    print(table)

#function to view all lab test presciptions of a patient
def viewPatientLabTestPrescriptions(patientId):
    rows = viewPatientLabTestPrescriptionsDb(patientId)
    table = PrettyTable(["Patient ID", "First Name", "Last Name", "Email Address", "Lab Test Prescription ID", "Test", "Status", "Result"])
    for row in rows:          
              table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]) 
    print(table)

#function to change the state of a lab test presciption record from Pending to Done
def labTestPrescriptionMarkDone(labTestPrescriptionId):
    labTestPrescriptionMarkDoneDb(labTestPrescriptionId)

#function to add the result of a lab test presciption
def addLabTestPrescriptionResult(labTestPrescriptionId, result):
    addLabTestPrescriptionResultDb(labTestPrescriptionId, result)


#Sickness Detail Data functions

#function to add a sickness detail
def addSicknessDetail(patientId, sickness, description):
    addSicknessDetailDb(patientId, sickness, description)

#function to remove a sickness detail
def removeSicknessDetail(sicknessDetailId):
    removeSicknessDetailDb(sicknessDetailId)

#function to view all sickness details
def viewAllSicknessDetails():
    rows = viewAllSicknessDetailsDb()
    table = PrettyTable(["Patient ID", "First Name", "Last Name", "Email Address", "Sickness Detail ID", "Sickness", "Description"])
    for row in rows:          
              table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]]) 
    print(table)

#function to view all sickness details of a patient
def viewPatientSicknessDetails(patientId):
    rows = viewPatientSicknessDetailsDb(patientId)
    table = PrettyTable(["Patient ID", "First Name", "Last Name", "Email Address", "Sickness Detail ID", "Sickness", "Description"])
    for row in rows:          
              table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]]) 
    print(table)


#--------------Program--------------

while(True):
    #Log-in interface
    print("--------------Log-in Menu--------------")
    print("0 - Exit")
    print("1 - Log in")
    print("2 - Sign up")
    select = input("Select : ")
    if(select == "0"):
        break
    
    #Log in as an existing user
    elif(select == "1"):
        print("--------------Enter your credentials--------------")
        email = input("Email: ")
        password = input("Password: ")
        #   hash the password with md5
        hashed_pw = hashlib.md5(password.encode())
        user = login(email,hashed_pw)
        
        if(user): # check whether the login is success
            print('Your privilage level :',user.privilegeLvl)
            loggedIn = True
            

            while(loggedIn):

                #--------------if the user is a Doctor--------------
                if (user.privilegeLvl == '4'):
                    #Doctor Main Menu
                    print("--------------Doctor Main Menu--------------")
                    print("0 - Log out")
                    print("1 - View all Patients")
                    print("2 - View a patient")
                    print("3 - Register a Patient")
                    print("4 - Delete a Patient")
                    print("5 - View all Sickness Details")
                    print("6 - View  Sickness Details of a Patient")
                    print("7 - Add Sickness Detail")
                    print("8 - Remove Sickness Detail")
                    print("9 - View all Drug Prescriptions")
                    print("10 - View Drug Prescriptions of a Patient")
                    print("11 - Add Drug Prescription")
                    print("12 - Remove Drug Prescription")
                    print("13 - View all Lab Test Prescriptions")
                    print("14 - View Lab Test Prescriptions of a Patient")
                    print("15 - Add Lab Test Prescription")
                    print("16 - Remove Lab Test Prescription")
                    select2 = input("Select : ")

                    if(select2 == "0"):
                        loggedIn = False
                        continue
                    
                    elif(select2 == "1"):
                        viewAllPatients()
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "2"):
                        patientId = int(input("Enter patient Id : "))
                        viewPatient(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "3"):
                        firstName = input("Enter patient First Name : ")
                        lastName = input("Enter patient Last Name : ")
                        email = input("Enter patient Email : ")
                        address = input("Enter patient Address : ")
                        phoneNum = int(input("Enter patient Phone Number : "))
                        registerPatient(firstName, lastName, email, address, phoneNum)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "4"):
                        viewAllPatients()
                        patientId = int(input("Enter Patient ID to delete : "))
                        deletePatient(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "5"):
                        viewAllSicknessDetails()
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "6"):
                        patientId = int(input("Enter patient Id : "))
                        viewPatientSicknessDetails(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "7"):
                        patientId = int(input("Enter Patient ID : "))
                        sickness = input("Enter Sickess : ")
                        description = input("Enter description : ")
                        addSicknessDetail(patientId, sickness, description)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "8"):
                        viewAllSicknessDetails()
                        sicknessDetailId = int(input("Enter Sickness Detail ID to delete : "))
                        removeSicknessDetail(sicknessDetailId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "9"):
                        viewAllDrugPrescriptions()
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "10"):
                        patientId = int(input("Enter patient Id : "))
                        viewPatientDrugPrescriptions(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "11"):
                        patientId = int(input("Enter Patient ID : "))
                        drug = input("Enter Drug : ")
                        dose = input("Enter Dosage : ")
                        addDrugPrescription(patientId, drug, dose)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "12"):
                        viewAllDrugPrescriptions()
                        drugPrescriptionId = int(input("Enter Drug Prescription ID to delete : "))
                        removeDrugPrescription(drugPrescriptionId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "13"):
                        viewAllLabTestPrescriptions()
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "14"):
                        patientId = int(input("Enter patient Id : "))
                        viewPatientLabTestPrescriptions(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "15"):
                        patientId = int(input("Enter Patient ID : "))
                        test = input("Enter Test : ")
                        addLabTestPrescription(patientId, test)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "16"):
                        viewAllLabTestPrescriptions()
                        labTestPrescriptionId = int(input("Enter Lab Test Prescription ID to delete : "))
                        removeLabTestPrescription(labTestPrescriptionId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                

                #--------------if the user is a Pharmacist--------------
                elif (user.privilegeLvl == '3'):
                    #Pharmacist Main Menu
                    print("--------------Pharmacist Main Menu--------------")
                    print("0 - Log out")
                    print("1 - View all Patients")
                    print("2 - View a patient")
                    print("3 - View all Drug Prescriptions")
                    print("4 - View Drug Prescriptions of a Patient")
                    print("5 - Update Drug Prescription as issued")
                    select2 = input("Select : ")

                    if(select2 == "0"):
                        loggedIn = False
                        continue
                    
                    elif(select2 == "1"):
                        viewAllPatients()
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "2"):
                        patientId = int(input("Enter patient Id : "))
                        viewPatient(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "3"):
                        viewAllDrugPrescriptions()
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "4"):
                        patientId = int(input("Enter patient Id : "))
                        viewPatientDrugPrescriptions(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "5"):
                        viewAllDrugPrescriptions()
                        drugPrescriptionId = int(input("Enter Drug Prescription Id : "))
                        isseDrugPrescription(drugPrescriptionId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                

                #--------------if the user is a Lab Technician--------------
                elif (user.privilegeLvl == '2'):
                    #Lab Technician Main Menu
                    print("--------------Lab Technician Main Menu--------------")
                    print("0 - Log out")
                    print("1 - View all Patients")
                    print("2 - View a patient")
                    print("3 - View all Lab Test Prescriptions")
                    print("4 - View Lab Test Prescriptions of a Patient")
                    print("5 - Mark Lab Test as Done")
                    print("6 - Enter Lab Test Result")
                    select2 = input("Select : ")

                    if(select2 == "0"):
                        loggedIn = False
                        continue
                    
                    elif(select2 == "1"):
                        viewAllPatients()
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "2"):
                        patientId = int(input("Enter patient Id : "))
                        viewPatient(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "3"):
                        viewAllLabTestPrescriptions()
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "4"):
                        patientId = int(input("Enter patient Id : "))
                        viewPatientLabTestPrescriptions(patientId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "5"):
                        viewAllLabTestPrescriptions()
                        labTestPrescriptionId = int(input("Enter Lab Test Prescription Id : "))
                        labTestPrescriptionMarkDone(labTestPrescriptionId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "6"):
                        viewAllLabTestPrescriptions()
                        labTestPrescriptionId = int(input("Enter Lab Test Prescription Id : "))
                        result = input("Enter Lab Test Result : ")
                        addLabTestPrescriptionResult(labTestPrescriptionId, result)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                
                #--------------if the user is a Patient--------------
                elif (user.privilegeLvl == '1'):
                    myId = getMyId(user.email)
                    if myId == None:
                        print("Couldn't find any patient records for the email", user.email)
                        break
                    #Patient Main Menu
                    print("--------------Patient Main Menu--------------")
                    print("0 - Log out")
                    print("1 - View my Details")
                    print("2 - View my Sickness Details")
                    print("3 - View my Drug Prescriptions")
                    print("4 - View my Lab Test Prescriptions")
                    select2 = input("Select : ")

                    if(select2 == "0"):
                        loggedIn = False
                        continue
                    
                    elif(select2 == "1"):
                        viewPatient(myId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "2"):
                        viewPatientSicknessDetails(myId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "3"):
                        viewPatientDrugPrescriptions(myId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
                    
                    elif(select2 == "4"):
                        viewPatientLabTestPrescriptions(myId)
                        print("Enter any key to View Main Menu")
                        select3 = input("Select : ")
                        continue
    
    #Register a new User
    elif(select == "2"):
        #User Sign-up interface
        print("--------------New User Sign-up--------------")
        print("1 - Patient Sign-up")
        print("2 - Lab Technician Sign-up")
        print("3 - Pharmacist Sign-up")
        print("4 - Doctor Sign-up")
        #select the type of user
        select2 = input("Select : ")
        if (select2 == '1'):
            privilegeLvl = 1
        elif (select2 == '2'):
            privilegeLvl = 2
        elif (select2 == '3'):
            privilegeLvl = 3
        elif (select2 == '4'):
            privilegeLvl = 4
        name = input("Enter Name : ")
        email = input("Enter Email : ")
        password = input("Enter Password : ")
        hashed_password = hashlib.md5(password.encode())

        #write the user credentials into the config.txt file
        f = open("config.txt", "a")
        userRecord = name + "," + email + "," + hashed_password.hexdigest() +"," + str(privilegeLvl)
        f.write(userRecord)
        f.write("\n")
        f.close()
        print("User Registered")
        print("Now you can log in using the credentials")