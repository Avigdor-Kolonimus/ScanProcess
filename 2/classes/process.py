#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#The my class for Assignment 1 
#@Author:  Alexey Titov
#@Version: 1.0
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#libraries
import sys
import os

#my class
class Process:
    __image=""             #image name
    __pid=0                #process id
    __session_name=""      #session_name
    __session_num=0        #session_num
    __mem_usage=0          #memory usage

    #constructor
    def __init__(self,image,pid,session_name,session_num,mem_usage):
        self.__image=image
        self.__pid=pid
        self.__session_name=session_name
        self.__session_num=session_num
        self.__mem_usage=mem_usage

    #get and set for __image
    def set_image(self,image):
        self.__image=image

    def get_image(self):
        return self.__image

    #get and set for __pid
    def set_pid(self,pid):
        self.__pid=pid

    def get_pid(self):
        return self.__pid

    #get and set for __session_name
    def set_session_name(self,session_name):
        self.__session_name=session_name

    def get_session_name(self):
        return self.__session_name

    #get and set for __session_num
    def set_session_num(self,session_num):
        self.__session_num=session_num

    def get_session_num(self):
        return self.__session_num

    #get and set for __mem_usage
    def set_mem_usage(self,mem_usage):
        self.__mem_usage=mem_usage

    def get_mem_usage(self):
        return self.__mem_usage

    #compare for class Process
    def compareProc(self,other):
        if (self.__image!=other.get_image()):
            return False
        elif (self.__pid!=other.get_pid()):
            return False
        return True
    
    #get type class
    def get_type(self):
        print("Process")

    #toString for class
    def toString(self):
        return "image: {}  pid: {}  session_name: {}  session_num: {}  mem_usage: {}".format(self.__image,
                                                                                             self.__pid,
                                                                                             self.__session_name,
                                                                                             self.__session_num,
                                                                                             self.__mem_usage)

