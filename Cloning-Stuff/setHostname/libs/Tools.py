import os
import logging
import sys
from cryptography.fernet import Fernet
from pathlib import Path
from libs.CmdRunner import CmdRunner
import time


class Tools:
    """ Stuff to Scripts, Filemanagement """

    def __init__(self, config, hostname, debug):
        self.logger = logging.getLogger('Tools')
        self.rootDir = Path(__file__).parent.parent
        self.lockFile = os.path.join(self.rootDir, '.lock')
        self.scriptPath = os.path.join(self.rootDir, 'scripts/')
        self.keyFile = os.path.join(self.rootDir, 'libs', 'key.key')
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')
        self.config = config
        self.hostname = hostname
        self.debug = debug

        # Cryptographie
        file = open(self.keyFile, 'rb')
        key = file.read()
        file.close()

        # encrypt
        self.fernet = Fernet(key)

    def decrypt(self, encMessage):
        """ decrypt a String """
        return self.fernet.decrypt(str.encode(encMessage)).decode()

    def getLockFilestatus(self):
        """ is there a Lock File? get the Lock Id """
        if (os.path.exists(self.lockFile) is False):
            return -1
        else:
            with open(self.lockFile, 'r') as f:
                last_line = f.readlines()[-1]
                # convert to int
                try:
                    result = int(last_line)
                    return result
                except Exception:
                    return -1

    def loadScript(self, filename):
        """ load a PS Script """
        path = os.path.join(self.scriptPath, filename)
        if (os.path.exists(path) is False):
            self.logger.error("Script %s does not exist -abort-" % path)
            sys.exit()
        else:
            with open(path, 'r') as f:
                lines = f.readlines()
            return lines

    def modifyScript(self, lines):
        """
        modify placeholders with decrypted passwords.
        not really save, but a bit ;)
        """
        # get Admin Passwords
        hashstr = self.config["config"]["domain"]["passwd"]
        domain_adminpasswd = self.decrypt(hashstr)
        hashstr = self.config["config"]["local"]["passwd"]
        local_adminpasswd = self.decrypt(hashstr)

        erg = []
        for line in lines:
            line = line.replace("{% username %}", self.config["config"]["domain"]["admin"])
            line = line.replace("{% password %}", domain_adminpasswd)
            line = line.replace("{% newhostname %}", self.hostname)
            line = line.replace("{% domain %}", self.config["config"]["domain"]["domainname"])
            line = line.replace("{% localadmin %}", self.config["config"]["local"]["admin"])
            line = line.replace("{% localadminpasswd %}", local_adminpasswd)
            erg.append(line)
        return erg

    def createScript(self, lines, filename):
        """ create a temporary PS Script """
        # tmp exists
        if (os.path.exists(self.tmpPath) is False):
            os.mkdir(self.tmpPath)

        newfile = os.path.join(self.tmpPath, filename)
        file = open(newfile, 'w')
        for line in lines:
            file.write(line)
        file.close()

    def rmFile(self, filename):
        if (os.path.exists(filename) is True):
            os.remove(filename)

    def Rename(self, filename):
        cmdarray = self.loadScript(filename)
        cmdarray = self.modifyScript(cmdarray)
        self.createScript(cmdarray, filename)
        # test
        self.debug = False
        # Do the JOB
        self.logger.info("Renaming Host to " + self.hostname)
        if self.debug is False:
            script = os.path.join(self.tmpPath, filename)
            runner = CmdRunner()
            runner.runPSFile(script)
            errors = runner.getStderr()
            if errors:
                self.logger.error(errors)
            # Delete tmp Script with passwords
            time.sleep(10)
            self.rmFile(script)
        self.logger.info("Host Renamed---------------------------------------------")
