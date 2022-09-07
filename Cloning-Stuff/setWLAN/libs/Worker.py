import logging
import os
from pathlib import Path
import re
import sys

from libs.CmdRunner import CmdRunner
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

        self.ssid = None
        self.profilePath = None

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

    def modifyScript(self, lines):
        """ modify placeholders """
        erg = []
        for line in lines:
            if self.ssid:
                line = line.replace("{% profile_name %}", self.ssid)
            line = line.replace("{% path %}", os.path.abspath(self.xmlPath))

            if self.profilePath:
                line = line.replace("{% file_name %}", self.profilePath)
            # line = line.replace("{% interface_name %}", ssid)

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

        # self.debugOutput(cmdarray)
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

    def search_files_in_dir(self, directory='.', pattern=''):
        """
        search for pattern in directory NOT recursive
        :param directory: path where to search. relative or absolute
        :param pattern: a list e.g. ['.jpg', '.gif']
        """
        data = []
        for child in Path(directory).iterdir():
            if child.is_file():
                # print(f"{child.name}")
                if pattern == '':
                    data.append(os.path.join(directory, child.name))
                else:
                    for p in pattern:
                        if child.name.endswith(p):
                            data.append(os.path.join(directory, child.name))
        return data

    def readInteger(self, msg):
        hasErrors = True
        while hasErrors is True:
            try:
                print(msg, sep='', end='')
                number = eval(input())
                hasErrors = False
            except:
                print(">> not a number ... try again")
        return number

    def getWlanSize(self):
        i = 0
        lines = self.getArrayFromString(self.wlanlist)
        data = self.processList(lines)
        for key, item in data.items():  # noqa
            i += 1
        return i

    def addWlan(self):
        self.getWlan()
        self.printWlanList()
        hasErrors = True
        while hasErrors is True:
            number = self.readInteger(
                "\nWhich WLAN Creditentials will you save?: ")
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

        self.ssid = ssid
        cmdarray = self.loadScript("saveWLAN")
        cmdarray = self.modifyScript(cmdarray)
        cmd = self.createCmd(cmdarray)
        self.runner.runCmd(cmd)
        print("Wlan Profile %s saved ..." % ssid)

        # ------------------------------------
        ssidPath = os.path.abspath(os.path.join(
            self.xmlPath, "WLAN-" + ssid + ".xml"))

        xmltool = XMLTool(ssidPath)
        ns = 'http://www.microsoft.com/networking/WLAN/profile/v1'
        elem = xmltool.find_chain(
            ['MSM', 'security', 'sharedKey', 'keyMaterial'], ns)
        # print("Found: %s, %s, %s" % (elem.tag, elem.attrib, elem.text))

        if self.cryptor.keyExists is False:
            self.cryptor.createKeyFile()
        chiper = self.cryptor.encrypt(elem.text)
        print("%s > %s" % (elem.text, chiper))

        xmltool.changeText(elem, chiper)
        xmltool.write()

    def showStoredWLan(self):
        """ shows all stored Wlan Profiles """

        if os.path.isdir(self.xmlPath) is True:
            print("Stored Wlan Profiles are ...")
            print("============================")
            files = self.search_files_in_dir(self.xmlPath, '*.xml')
            key = 1
            for item in files:
                # extract Wlan Profile Name
                # WLAN-PNMS_Schueler
                file = os.path.basename(item)[5:-4]
                print(f"{key:>3}: { file }")
                key += 1
        else:
            print("Im moment gibt es noch keine gespeicherten WLAN Profile ...")

    def rmFile(self, filename):
        if (os.path.exists(filename) is True):
            os.remove(filename)

    def importStoredWLan(self):
        """ will import all stored Wlan Profiles to this client """
        files = self.search_files_in_dir(self.xmlPath, '*.xml')
        for item in files:
            ssid = os.path.basename(item)[5:-4]
            print("Importing Wlan Profile %s ..." % ssid)

            # load xml and decrypt passwd
            xmltool = XMLTool(item)
            ns = 'http://www.microsoft.com/networking/WLAN/profile/v1'
            elem = xmltool.find_chain(
                ['MSM', 'security', 'sharedKey', 'keyMaterial'], ns)

            # print("Found: %s, %s, %s" % (elem.tag, elem.attrib, elem.text))

            if self.cryptor.keyExists is False:
                print("No Key file for decrypting found ... exiting now!")
                exit()
            text = self.cryptor.decrypt(elem.text)
            # print("%s > %s" % (elem.text, text))

            # create temp xml file WLAN-PNMS_Schueler.xml >
            # WLAN-PNMS_Schueler-tmp.xml
            filename = item[:-4] + "-tmp.xml"
            xmltool.changeText(elem, text)
            xmltool.write(filename)

            self.importWlan(filename)

            # delete tmp file
            f = os.path.join(self.xmlPath, filename)
            self.rmFile(f)

    def importWlan(self, filename):
        """ import from xml file """
        self.profilePath = os.path.join(self.xmlPath, filename)
        cmdarray = self.loadScript("importWLAN")
        cmdarray = self.modifyScript(cmdarray)
        cmd = self.createCmd(cmdarray)

        self.runner.runCmd(cmd)
        print(self.runner.getStdout())

        profile = os.path.basename(filename)[5:-8]
        print("Wlan Profile %s imported ..." % profile)
