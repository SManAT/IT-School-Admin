import os
import sys
from pathlib import Path
from libs.CmdRunner import CmdRunner
import time


class ScriptTool:
    """ Stuff to Scripts, Filemanagement """

    def __init__(self, debug):
        self.rootDir = Path(__file__).parent.parent
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')
        self.scriptPath = os.path.join(self.rootDir, 'ps/')
        self.debug = debug

    def loadScript(self, filename):
        """ load a PS Script """
        path = os.path.join(self.scriptPath, filename)
        if (os.path.exists(path) is False):
            print("Script %s does not exist -abort-" % path)
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

    def modifyScript(self, lines, user, filename):
        """ modify placeholders """
        erg = []
        for line in lines:
            line = line.replace("%PATH%", "%s" % filename)
            line = line.replace("%USER%", user) 
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

    def _execute(self, script, override_debug = False):
      """ excute PS Script """
      runner = CmdRunner()
      
      if self.debug is False or override_debug is True:
        runner.runPSFile(script)
      errors = runner.getStderr()
      if errors:
          print(errors)
      # Delete tmp Script
      time.sleep(0.5)
      if self.debug is False:
        self.rmFile(script)
      return runner.getStdout()

    def chownFile(self, user, filename):
      psTemplate = "chownFile.ps1"
      cmdarray = self.loadScript(psTemplate)      
      cmdarray = self.modifyScript(cmdarray, user, filename)
      self.createScript(cmdarray, psTemplate)
      psFile =  os.path.join(self.tmpPath, filename)
      if self.debug is False:
        self._execute(psFile)
        

        
   