#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#The main for Assignment 1 of Laboratory protection
#@Author:  Alexey Titov
#@Version: 1.0
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#libraries
import os
import time
import re
from datetime import datetime
from sys import platform
from subprocess import Popen, PIPE, check_output
from classes.process import Process
if platform == "linux" or platform == "linux2":
    import psutil

#the function returns number
def getNumeric(message):
    while True:
        response=input(message)
        try:
            if (int(response)>0):
                return int(response)
            else:
                print("Please enter a number >0")
        except ValueError:
            print("Please enter a number")
            
#the function gives the running processes
def get_processes_running():
    """
    Takes tasklist output and parses the table into a dict
    """
    p = []              #array of processes
    if platform == "linux" or platform == "linux2":
        for proc in psutil.process_iter():
            try:
                tmp=Process(proc.name(),int(proc.pid),proc.username(),int(0),int(0))
                p.append(tmp)
            except:
                continue
        return (p)
			
    tasks = check_output(['tasklist']).decode('cp866', 'ignore').split("\r\n")
    for task in tasks:
        m = re.match(b'(.*?)\\s+(\\d+)\\s+(\\w+)\\s+(\\w+)\\s+(.*?)\\s.*', task.encode())
        if m is not None:
            tmp=Process(m.group(1).decode(),int(m.group(2).decode()),m.group(3).decode(),int(m.group(4).decode()),int(m.group(5).decode('ascii', 'ignore')))
            p.append(tmp)
            #m.group(1).decode()                               image name
            #m.group(2).decode()                               process id
            #m.group(3).decode()                               session_name
            #m.group(4).decode()                               session_num
            #m.group(5).decode('ascii', 'ignore')              memory usage
    return(p)

#the function creates new files and rename old files
def RemCreFiles():
    old_file1 = os.path.join("Scanner","processList.txt")
    old_file2 = os.path.join("Scanner","Status_Log.txt")
    prefix=datetime.strftime(datetime.now(), "%Y_%m_%d %H_%M_%S")
    new_file1 = os.path.join("Scanner",prefix+"_processList.txt")
    new_file2 = os.path.join("Scanner",prefix+"_Status_Log.txt")
    folder="Scanner"
    #if file is exist
    try:
        os.stat(folder)
    except:
        os.mkdir(folder)
    #rename old files
    try:
        os.rename(old_file1,new_file1)
        os.rename(old_file2,new_file2)
    except:
        return

#the function writes processes to processList.txt
def WriteToProcessList(lst):
    try:
        fileProcessList="Scanner//processList.txt"
        my_file = open(fileProcessList, "a")
        my_file.write("------------------------------------------------------------------------------------------------------\n")
        my_file.write("Time:                               %r                               \n" %datetime.strftime(datetime.now(),"%Y.%m.%d %H:%M:%S"))
        my_file.write("------------------------------------------------------------------------------------------------------\n")
        for p in lst:
            my_file.write("%r\n" %p.toString())
        my_file.close() 
        return
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        my_file.close()
        exit()

#the function return proccesses running now    
def GetSetList():
    #call the function get_processes_running()
    lstp = get_processes_running()
    WriteToProcessList(lstp)
    return(lstp)

#the function monitors old and new processes
def SetStatus(old,new,run,flag):
    try:
        fileStatus_Log="Scanner//Status_Log.txt"
        my_file = open(fileStatus_Log, "a")
        my_file.write("------------------------------------------------------------------------------------------------------\n")
        my_file.write("Time:                                            %r                                              \n" %run)
        my_file.write("------------------------------------------------------------------------------------------------------\n")
        #someone changed Status_Log.txt file
        if (flag==1):
            my_file.write("DANGER! someone could change or delete Status_Log.txt\n")
            print("----------------------------\nDANGER! someone could change or delete Status_Log.txt\n-------------------------------\n")
	#someone changed processList.txt file
        if (flag==2):
            my_file.write("DANGER! someone could change or delete processList.txt\n")
            print("----------------------------\nDANGER! someone could change or delete processList.txt\n-------------------------------\n")
        #someone changed processList.txt and Status_Log.txt files
        if (flag==3):
            my_file.write("DANGER! someone could change or delete processList.txt\n")
            my_file.write("DANGER! someone could change or delete Status_Log.txt\n")
            print("----------------------------\nDANGER! someone could change or delete Status_Log.txt\n-------------------------------\n")
            print("----------------------------\nDANGER! someone could change or delete processList.txt\n-------------------------------\n")
	#killed processes
        for p1 in old:
            flag=0
            for p2 in new:
                if (p1.compareProc(p2)):
                    flag=1
                    break
            if (flag==0):
                my_file.write("Killed process: %r\n" %p1.toString())
                print("Killed process: %r\n" %p1.toString())
        #new processes
        for p1 in new:
            flag=0
            for p2 in old:
                if (p1.compareProc(p2)):
                    flag=1
                    break
            if (flag==0):
                my_file.write("New process: %r\n" %p1.toString())
                print("New process: %r\n" %p1.toString())        
        my_file.close()
        return(new)
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        my_file.close()
        exit()

#the function checks if someone has changed files
def HackerModFile(last_modifications):
    flag=0;
    try:
        Lmod0=os.path.getmtime("Scanner//processList.txt")
    except: #file is deleted
        Lmod0=-1
    try:
        Lmod1=os.path.getmtime("Scanner//Status_Log.txt")
    except: #file is deleted
        Lmod1=-1
    #someone changed Status_Log.txt file
    if (last_modifications[1]!=-1 and last_modifications[1]!=Lmod1):
        #someone changed processList.txt file
        if (last_modifications[0]!=-1 and last_modifications[0]!=Lmod0):
            flag=3
        else:
            flag=1
    elif (last_modifications[0]!=-1 and last_modifications[0]!=Lmod0):
        flag=2
    return flag
    
if __name__ == '__main__':
    try:
        run=1
        RemCreFiles()
        X=getNumeric("Hello user, enter X time: ")
        old=[]
        new=[]
        old=GetSetList()
        last_modifications=[-1,-1]
        while True:
            time.sleep(X)
            flag=HackerModFile(last_modifications)
            new=GetSetList()
            old=SetStatus(old,new,run,flag)
            run+=1
            last_modifications[0]=os.path.getmtime("Scanner//processList.txt")
            last_modifications[1]=os.path.getmtime("Scanner//Status_Log.txt")
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()
