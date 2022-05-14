import os
import logging
import sys
from pathlib import Path
from libs.CmdRunner import CmdRunner
import time


class ScriptTool:
    """ Stuff to Scripts, Filemanagement """

    def __init__(self, config, debug, counter):
        self.logger = logging.getLogger('ScriptTool')
        self.rootDir = Path(__file__).parent.parent
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')
        self.scriptPath = os.path.join(self.rootDir, 'ps/')
        self.config = config
        self.debug = debug
        self.counter = counter

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

    def pathEndingSlash(self, path):
        """ check for ending slash at path """
        if path.endswith(os.path.sep) is False:
          path = "%s%s" % (path, os.path.sep)
        return path

    def modifyScript(self, lines, user):
        """ modify placeholders """
        erg = []
        grpgOU = "CN=%s,%s" % (user.getGruppe(), self.config["ad"]["OU_GRUPPEN"])
        userDN = "CN=%s %s,OU=%s,%s" % (user.getNachname(), user.getVorname(), user.getGruppe(), self.config["ad"]["OU_BENUTZER"])
        principal = "%s@%s" % (user.getUsername(), self.config["ad"]["DOMAIN"])

        nvn = user.getVorname().lower()
        nnn = user.getNachname().lower()
        loginName = "%s.%s" % (nvn[:1], nnn)

        for line in lines:
            line = line.replace("%VORNAME%", user.getVorname())
            line = line.replace("%NACHNAME%", user.getNachname())
            
            # hans.moser@schule.local
            line = line.replace("%USERNAME%", principal)
            line = line.replace("%USERNAMEDN%", userDN) 

            # hans.moser also ohne domain
            ushort = principal.split("@")
            line = line.replace("%USERNAME_SHORT%", ushort[0])

            line = line.replace("%LOGIN_NAME%", loginName)           

            line = line.replace("%HOMEDIR%", self.pathEndingSlash(self.config["ad"]["HOME_PATH"]))
            line = line.replace("%PROFILEDIR%", self.pathEndingSlash(self.config["ad"]["PROFILE_PATH"]))

            
            line = line.replace("%OUUSERS%", self.config["ad"]["OU_BENUTZER"])
            
            line = line.replace("%GRUPPE%", grpgOU)
            line = line.replace("%GRUPPE_SHORT%", user.getGruppe())

            line = line.replace("%PASSWORD%", self.config["ad"]["INIT_PWD"])
            line = line.replace("%HOMEDRIVE%", self.config["ad"]["HOME_DRIVE"])

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

    def unblockFile(self, filename):
      """ Use the Unblock cmd from PS """
      runner = CmdRunner()
      cmd = "Unblock-File -Path %s" % filename
      runner.runCmd(cmd)

    def createCmd(self, arr):
      """ from array to line;line;line """
      erg = ""
      for line in arr:
        erg += ";%s" % line
      # delete first ;
      erg = erg[1:]
      # replace line breaks
      erg = erg.replace('\n', '')
      # escape sign
      erg = erg.replace('"', '\\"')
      return erg

    def debugOutput(self, data):
      """ just Debug Output """
      for line in data:
        line = line.replace('\n', '')
        print(line)

    def _execute(self, psfile, user):
      # Set Owner -----
      psTemplate = psfile
      cmdarray = self.loadScript(psTemplate)
      cmdarray = self.modifyScript(cmdarray, user)
      cmd = self.createCmd(cmdarray)

      print(cmd)
      exit()

      if self.debug is False:
        self.runner.runCmd(cmd)

      # grant Permissions to this owner
      psTemplate = "setPermission.ps1"
      cmdarray = self.loadScript(psTemplate)
      cmdarray = self.modifyScript(cmdarray, user, filename)
      #self.debugOutput(cmdarray)
      cmd = self.createCmd(cmdarray)

      if self.debug is False:
        self.runner.runCmd(cmd)

    def existsUser(self, user):
      """ check for User in Active Domain Forrest """
      answer = self._execute("existsUser.ps1", user)

      # analyse answer
      if answer.find('DistinguishedName') > -1:
        return True
      else:
        return False

    def groupExists(self, user):
      """ doese the group exists in AD """
      answer = self._execute("existsGroup.ps1", user)

      # analyse answer
      if answer.find('DistinguishedName') > -1:
        return True
      else:
        return False

    def addUser2Group(self, user):
        """ add User via Powershell Script to a AD Group"""
        script = self._createRunningScript("addToGroup.ps1", user)
        # Do the JOB
        print("Adding User %s to Group: %s " % (user.getFullname(), user.getGruppe()))
        self._execute(script)

    def addUser(self, user):
        """ add User via Powershell Script """
        if self.groupExists(user) or self.debug is True:
          script = self._createRunningScript("addUser.ps1", user)

          # Do the JOB
          print("Creating User: %s " % user.getFullname())

          if self.debug is False:
            self._execute(script)
          self.counter.incUser()

          # Add User to Goup -------------------------------------------------
          self.addUser2Group(user)
        else:
          self.counter.incWrongGroups()
          print("AD Group %s does not exists! User %s will be not created!" % (user.getGruppe(), user.getFullname()))
