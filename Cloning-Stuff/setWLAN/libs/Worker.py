import logging
import re
import sys
import time
import psutil
import os
from libs.CmdRunner import CmdRunner
import xml.etree.ElementTree as ET
from libs.XMLTool import XMLTool



class Worker:
    """ Class to do all the Stuff """
    debug = True

    def __init__(self, rootDir, cryptor):
        self.logger = logging.getLogger('Worker')
        self.rootDir = rootDir
        self.cryptor = cryptor
        self.runner = CmdRunner()
        self.scriptPath = os.path.join(self.rootDir, 'cmd/')
        self.xmlPath = os.path.join(self.rootDir, 'xml/')
        self.wlanlist = {}

    def decrypt(self, encMessage):
        """ decrypt a String """
        return self.fernet.decrypt(str.encode(encMessage)).decode()
    
    def debugOutput(self, data):
        """ just Debug Output """
        for line in data:
          line = line.replace('\n', '')
          print(line)
          
    def createDir(self, path):
        """ create dir if it not exists """
        if os.path.isdir(path) is False:
          os.mkdir(path)
          
    def loadScript(self, filename):
        """ load a PS Script """
        path = os.path.join(self.scriptPath, filename)
        if (os.path.exists(path) is False):
            self.logger.error("Script %s does not exist -abort-" % path)
            sys.exit()
        else:
            with open(path, 'r', encoding='utf8') as f:
                lines = f.readlines()
            return lines
        
    def modifyScript(self, lines, ssid):
        """ modify placeholders """
        erg = []
        for line in lines:
            line = line.replace("{% profile_name %}", ssid)
            line = line.replace("{% path %}", os.path.abspath(self.xmlPath))
            erg.append(line)
        return erg

    def createCmd(self, arr):
        """ from array to line;line;line """
        erg = ""
        for line in arr:
            # replace line breaks
            line = line.replace('\n', '')
            # no comments
            line = line.strip()
            # delete empty lines
            char = line[:1]
            if char != "#":
                if len(line) != 0:
                    if erg[-1:] == "{":  # nach { oder } darf kein ; sein
                        erg += "%s" % line
                    else:
                        erg += ";%s" % line
        # delete first ;
        erg = erg[1:]
    
        # escape sign, will run inside String
        erg = erg.replace('"', '\\"')
        return erg
    
    def _execute(self, template):
        """ load Code from cmd File and execute it """
        cmdarray = self.loadScript(template)
    
        #self.debugOutput(cmdarray)
        cmd = self.createCmd(cmdarray)
        self.runner.runCmd(cmd)
        return self.runner.getStdout()
    
    def getArrayFromString(self, lines):
        lines = lines.split('\n')
        return lines
    
    def processList(self, lines):
        erg = {}
        index = 1
        for line in lines:
            match = re.fullmatch(r'.*(Profil)+.*:(.*)$', line)
            if match:
                data = match.groups()
                data = data[-1].strip()
                if data != "":
                    erg[index] = data
                    index += 1
        return erg
    
    def getWlan(self):
        self.wlanlist.clear()
        self.wlanlist = self._execute("listWLAN")
        
    def printWlanList(self):
        lines = self.getArrayFromString(self.wlanlist)
        data = self.processList(lines) 
        for key, item in data.items():
            print(f"{key:>3}: { item }")
    
    def listWlan(self):
        """ list all available WLAN """
        self.getWlan()
    
        print("WLANS stored on this client:")
        print("----------------------------")
        self.printWlanList()
        
            
    def readInteger(self, msg):
        hasErrors =True
        while hasErrors is True:
            try:
                print(msg, sep='', end='')
                number = eval(input())
                hasErrors =False
            except:
                print(">> not a number ... try again")
        return number
    
    def getWlanSize(self):
        i = 0
        lines = self.getArrayFromString(self.wlanlist)
        data = self.processList(lines) 
        for key, item in data.items():
            i += 1
        return i
            
    def addWlan(self):
        self.getWlan()
        self.printWlanList()
        hasErrors = True
        while hasErrors is True:
            number = self.readInteger("\nWhich WLAN Creditentials will you save?: ")
            # print("1 <= %s <= %s" % (number, self.getWlanSize()))
            if number >= 1 and number <= self.getWlanSize():
                hasErrors = False
                
        # get WLAN via number
        lines = self.getArrayFromString(self.wlanlist)
        data = self.processList(lines)
        ssid = data[number]
        
        # save to xml folder
        self.saveWlanProfile(ssid)
        
    def saveWlanProfile(self, ssid):
        """ export Wlan Profile to disk and encrypt it """
        self.createDir(self.xmlPath)
        
        cmdarray = self.loadScript("saveWLAN")
        cmdarray = self.modifyScript(cmdarray, ssid)
        cmd = self.createCmd(cmdarray)
        self.runner.runCmd(cmd)
        print("Wlan Profile %s saved ..." % ssid)
        
        # ------------------------------------   
        ssidPath = os.path.abspath(os.path.join(self.xmlPath, "WLAN-"+ssid+".xml"))
        print(ssidPath)
        
        xmltool = XMLTool(ssidPath) 
        elem = xmltool.find('keyMaterial')
        print(elem)
        #print("Found: %s, %s, %s" % (elem.tag, elem.attrib, elem.text))
        
       # elem.text ="Hallo"
                
       # https://www.geeksforgeeks.org/modify-xml-files-with-python/        
        #xmltool.write()
        
  
        
        
            
     
