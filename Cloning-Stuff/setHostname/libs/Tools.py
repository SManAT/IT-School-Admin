import os
import logging
import sys
from cryptography.fernet import Fernet
from pathlib import Path


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
                
    def setLockFileStatus(self, status, msg):
        """ Falls nicht existiert = 0 1... Renamed 2... Joined Domain """
        file1 = open(self.lockFile, 'w')
        file1.write("%s\n" % msg)
        file1.write("%s\n" % status)
        file1.close()
       
        self.logger.info("Lock File gesetzt (%s) ..." % status);
        
    def appendLockFileStatus(self, status, msg):
        """ self explaining """
        file1 = open(self.lockFile, "a")
        file1.write("%s\n" % msg)
        file1.write("%s\n" % status)
        file1.close()

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
    
    def _execute(self, psTemplate):
        """ load Code from PS File, replace variables and excute it """
        cmdarray = self.loadScript(psTemplate)
        cmdarray = self.modifyScript(cmdarray)
    
        # self.debugOutput(cmdarray)
        cmd = self.createCmd(cmdarray)
    
        if self.debug is False:
            if self.error.hasErrors() is False:
                self.runner.runCmd(cmd)
                return self.runner.getStdout()
        else:
            print("\nCommand:")
            print(cmd)
            print("\n")
            return ""

    

    def Rename(self, hostname):
        """ Rename the Host to hostname """
        self.hostname = hostname
      
        # Do the JOB
        self.logger.info("Renaming Host to " + self.hostname)
        self._execute("Rename.ps1")
        self.logger.info("Host Renamed---------------------------------------------")
        
    def RestartHost(self):
        """ Resart the Host """
        self.logger.info("Restart ...")
        if self.debug is False:
            self._execute("Restart.ps1")
            
    def JoinDomain(self):
        """ Join the host to the domain """
        # Do the JOB
        self.logger.info("Joining to Domain %s" % self.config["config"]["domain"]["domainname"])
        self._execute("joinDomain.ps1")
        self.logger.info("Joined Domain--------------------------------------------");

    def KMSRearm(self):
        self._execute("KMSPart1.ps1")
        self.logger.info("KMS Rearmed --------------------------------------------");
        
    def KMSAto(self):
        self._execute("KMSPart2.ps1")
        self.logger.info("KMS Ato --------------------------------------------");
        
    def Shutdown(self):
        """ shutdown the host """
        self._execute("Shutdown.ps1")
        
    
        
        
        
        
        
        
        
        
        
        
        