import yaml
import os
from pathlib import Path
from libs.CmdRunner import CmdRunner
from datetime import date, datetime
from time import sleep
import sys
import fnmatch
import re
import timeit
import time


class User():
    """ Data Wrapper """
    def __init__(self):
        self.username = ""
        self.hosts = ""
        self.pwd = ""
        self.privileges = []

    def get_username(self):
        return self.__username


    def get_hosts(self):
        return self.__hosts


    def get_pwd(self):
        return self.__pwd


    def set_username(self, value):
        self.__username = value


    def set_hosts(self, value):
        self.__hosts = value


    def set_pwd(self, value):
        self.__pwd = value
        
    def add_privilege(self, value):
        self.privileges.append(value)
        
    def get_privileges(self):
        return self.privileges
    
    def print_privileges(self):
        for line in self.privileges:
            print(line)

        
    def __str__(self):
        return("%s; %s; %s" % (self.get_username(), self.get_hosts(), self.get_pwd()))

    
    