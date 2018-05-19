#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#The main for Assignment 2 of Laboratory protection
#@Author:  Alexey Titov
#@Version: 4.0
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#libraries
import os
import re
import time
from datetime import datetime
from sys import platform
from subprocess import Popen, PIPE, check_output
from classes.process import Process
if platform == "linux" or platform == "linux2":
    import psutil

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#First laboratory
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#Second laboratory
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#the function returns datetime
def getDateTime(message):
    while True:
        response=raw_input(message)
        #response=input(message)
        try:
            date_time=datetime.strptime(response, "%Y-%m-%d %H:%M:%S")
            return date_time
        except ValueError:
            print("Please enter a datetime")

#the function compares strings
def CompareStrings(a,b):
    try:
        if (a[1]==b[1] and a[2]==b[2] and a[3]==b[3]):
            return True
        return False
    except:
        print("The data in the processList.txt file is not correct")
        os._exit(0)

#the function demonstrates the difference between samples
def Different(first,second):
    #old
    for item_i in first:
        flag=0
        for item_j in second:
            if (CompareStrings(item_i.split(":"),item_j.split(":"))):
                flag=1
        if (flag==0):
            item_i= re.sub("['\n]",'',item_i)
            print("Killed process: %r" %item_i)
    #new
    for item_i in second:
        flag=0
        for item_j in first:
            if(CompareStrings(item_i.split(":"),item_j.split(":"))):
                flag=1
        if (flag==0):
            item_i= re.sub("['\n]",'',item_i)
            print("New process: %r" %item_i)

#the function checks which file exists
def CheckExist():
    file_1_path = "Scanner//processList.txt"
    file_2_path = "processList.txt"
    if os.access(file_1_path, os.F_OK) == True:
        return file_1_path
    elif os.access(file_2_path, os.F_OK) == True:
        return file_2_path
    else:
        print("The processList.txt file does not exist or is not in the correct directory")
        os._exit(0)

#the function read file
def ReadFile(first_time,second_time):
    try:
        boarder="------------------------------------------------------------------------------------------------------\n"
        num_processes=0         #number of check entries
        firsttest=first_time;
        secondtest=second_time;
        list_arr=[]
        first_arr=[]
        second_arr=[]
        first_st=float('inf')   #to store the scan time
        min_first=float('inf')  #variable for storing the value of the minimum difference between tmp_time and first_time
        min_second=float('inf') #variable for storing the value of the minimum difference between tmp_time and second_time
        fileName=CheckExist()
        with open(fileName,"r") as file_handler:
            #for line in file_handler:      #problem for python
            while True:
                line = file_handler.readline()
                if not line:
                    break
                if (line.startswith("Time:")):
                    num_processes+=1
                    tmp=line.split("'")
                    tmp_time=datetime.strptime(tmp[1], "%Y.%m.%d %H:%M:%S")
                    #correct calculation of the difference in seconds for the first input
                    if(tmp_time>=first_time):
                        first_d=(tmp_time-first_time).seconds
                    else:
                        first_d=(first_time-tmp_time).seconds
                    #correct calculation of the difference in seconds for the second input
                    if(tmp_time>=second_time):
                        second_d=(tmp_time-second_time).seconds
                    else:
                        second_d=(second_time-tmp_time).seconds
                    line=file_handler.readline()
                    line=file_handler.readline()
                    #reading processes that ran
                    while(line.startswith("'image:")):
                        list_arr.append(line)
                        if (len(line.split(":"))!=6):
                            print("The data in the processList.txt file is not correct:")
                            print(line)
                            os._exit(0)
                        line=file_handler.readline()
                    if(line!=boarder and line!=''):
                        print("The data in the processList.txt file is not correct:")
                        print(line)
                        os._exit(0)
                    #close to the first input
                    if (min_first>first_d):
                        if(min_second>first_st):
                            secondtest=firsttest
                            second_arr.clear()
                            second_arr=list(first_arr)
                            min_second=first_st
                        firsttest=tmp_time
                        first_arr.clear()
                        first_arr=list(list_arr)
                        min_first=first_d
                        first_st=second_d
                    #close to the first input
                    elif(min_second>second_d):
                        secondtest=tmp_time
                        second_arr.clear()
                        second_arr=list(list_arr)
                        min_second=second_d
                    list_arr.clear()
                elif(line!=boarder and line!=''):
                    print("The data in the processList.txt file is not correct:")
                    print(line)
                    os._exit(0) 
        if (num_processes<=1):
            print("There is only one record or file is empty")
        else:
            if (firsttest<secondtest):
                Different(first_arr,second_arr)
            else:
                Different(second_arr,first_arr)
    except IOError:
        print("An IOError has occurred!")
    finally:
        file_handler.close()
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#main
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#assignment 1
def proc1():
    try:
        run=1
        old=[]
        new=[]
        RemCreFiles()
        X=getNumeric("Hello user, enter X time: ")
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
#assignment 2
def proc2():
    first_time=getDateTime("Please enter first datetime according to the format %Y-%m-%d %H:%M:%S :\n")
    second_time=getDateTime("Please enter second datetime according to the format %Y-%m-%d %H:%M:%S :\n")
    if (first_time!=second_time):
        if (first_time<second_time):
            ReadFile(first_time,second_time)
        else:
            ReadFile(second_time,first_time)
    else:
        print("You entered the same time, so the answer is empty")
        
if __name__ == '__main__':
    try:
        X=getNumeric("User select:\n1-Assignment 1\n2-Assignment 2\nany other-EXIT\n")
        if (X==1):
            proc1()
        elif (X==2):
            proc2()
        else:
            print("Good bye!")
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()
