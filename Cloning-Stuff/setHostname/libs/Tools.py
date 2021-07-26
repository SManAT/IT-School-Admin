import os
import logging
import sys
from cryptography.fernet import Fernet
from pathlib import Path
import signal


class Tools:
    """ Stuff to Scripts, Filemanagement """

    def __init__(self, config, hostname):
        self.logger = logging.getLogger('Tools')
        self.rootDir = Path(__file__).parent.parent
        self.lockFile = os.path.join(self.rootDir, '.lock')
        self.scriptPath = os.path.join(self.rootDir, 'scripts/')
        self.keyFile = os.path.join(self.rootDir, 'libs', 'key.key')
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')
        self.config = config
        self.hostname = hostname
        
        # Cryptographie
        file = open(self.keyFile, 'rb')
        key = file.read()
        file.close()

        # encrypt
        self.fernet = Fernet(key)
        
    def exit_handler(self):
        print("EXIT Handler")

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
            self.logger.error("Script scripts/%s does not exist -abort-" % filename)
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
        sys.exit()

    def Rename(self, filename):
        cmdarray = self.loadScript(filename)
        cmdarray = self.modifyScript(cmdarray)
        print(cmdarray)
        self.createScript(cmdarray, filename)
        """
        
        Path filepath = Paths.get(TMP_Dir + filename)

        if(FileTools.Exists(filepath) == false){
            logger.error("Script not found: " + filepath)
            this.triggerCloseEvent()
        }

        //Do the JOB
        logger.info("Renaming Host to " + host.getName())
        if(this.debug == false){
            aRuntime shell = new aRuntime()
            shell.executePSScript(filepath, true)
            // Delete tmp Script with passwords
            FileTools.Delete(Paths.get(TMP_Dir + "Rename.ps1"))
        }
        logger.info("Host Renamed---------------------------------------------")
        """
