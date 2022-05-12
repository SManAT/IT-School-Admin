import os
from pathlib import Path
from libs.CmdRunner import CmdRunner
from libs.ScriptTool import ScriptTool
import time


class PSTool:
    """ Stuff to use Powershell """

    def __init__(self, debug):
        self.rootDir = Path(__file__).parent.parent
        self.scriptPath = os.path.join(self.rootDir, 'ps/')
        self.debug = debug

    def pathEndingSlash(self, path):
        """ check for ending slash at path """
        if path.endswith(os.path.sep) is False:
          path = "%s%s" % (path, os.path.sep)
        return path

    def _execute(self, script, override_debug=False):
      """ excute PS Script """
      runner = CmdRunner()

      if self.debug is False or override_debug is True:
        self.unblockFile(script)
        runner.runPSFile(script)
      errors = runner.getStderr()
      if errors:
          self.logger.error(errors)
      # Delete tmp Script
      time.sleep(0.5)
      # if self.debug is False:
      #  self.rmFile(script)
      return runner.getStdout()

    def chown(self, user, target):
      """ will change target to Ownership of user """
      # target is valid?
      path = Path(target)
      if path.is_dir():
        print(">>> Directory")
        self.chownDir(user, path)
        return

      if path.is_file():
        print(">>> File")
        self.chownFile(user, path)
        return

      # Error Handling
      print("The file/directory %s is not valid or does not exists! -exit-" % target)
      exit(-1)   

    def chownDir(self, user, path):
      """ change Owner of directory recursive """
      pass
  
    def chownFile(self, user, filename):
      """ change Owner of this file """
      script = ScriptTool(self.debug)
      script.chownFile(user, filename)
      pass