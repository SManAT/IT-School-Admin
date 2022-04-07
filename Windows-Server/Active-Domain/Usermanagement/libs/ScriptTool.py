import os
import logging
import sys
from pathlib import Path
from libs.CmdRunner import CmdRunner
import time


class ScriptTool:
    """ Stuff to Scripts, Filemanagement """

    def __init__(self, config, debug):
        self.logger = logging.getLogger('ScriptTool')
        self.rootDir = Path(__file__).parent.parent
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')
        self.scriptPath = os.path.join(self.rootDir, 'ps/')
        self.config = config
        self.debug = debug

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

    def pathEndingSlash(path):
        """ check for ending slash at path """
        pass

    def modifyScript(self, lines, user):
        """ modify placeholders """
        erg = []
        for line in lines:
            line = line.replace("%VORNAME%", user.getVorname())
            line = line.replace("%NACHNAME%", user.getNachname())
            line = line.replace("%USERNAME%", user.getUsername())
            line = line.replace("%PROFILEDIR%", self.pathEndingSlash(self.config["ad"]["PROFILE_PATH"]))
            line = line.replace("%HOMEDIR%", self.pathEndingSlash(self.config["ad"]["HOME_PATH"]))
            line = line.replace("%OUUSERS%", self.config["ad"]["OU_BENUTZER"])
            line = line.replace("%GRUPPE%", user.getGruppe())
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

    def existsUser(self, user):
      """ check for User in Active Domain Forrest """
      filename = "existsUser.ps1"
      cmdarray = self.loadScript(filename)
      cmdarray = self.modifyScript(cmdarray, user)
      self.createScript(cmdarray, filename)
      script = os.path.join(self.tmpPath, filename)
      runner = CmdRunner()
      if self.debug is False:
        runner.runPSFile(script)
      errors = runner.getStderr()
      if errors:
          self.logger.error(errors)
      # Delete tmp Script
      time.sleep(0.5)
      if self.debug is False:
        self.rmFile(script)

      # analyse answer
      answer = runner.getStdout()
      if answer.find('DistinguishedName') > -1:
        return True
      else:
        return False

    def addUser(self, user):
        """ add User via Powershell Script """
        filename = "addUser.ps1"
        cmdarray = self.loadScript(filename)
        cmdarray = self.modifyScript(cmdarray, user)
        self.createScript(cmdarray, filename)
        # Do the JOB
        print("Creating User: %s " % user.getFullname())

        script = os.path.join(self.tmpPath, filename)
        runner = CmdRunner()
        if self.debug is False:
          runner.runPSFile(script)
        errors = runner.getStderr()
        if errors:
            self.logger.error(errors)
        # Delete tmp Script
        time.sleep(0.5)
        if self.debug is False:
            self.rmFile(script)
