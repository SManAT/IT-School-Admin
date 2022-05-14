import os
from pathlib import Path
from libs.ScriptTool import ScriptTool
from libs.CmdRunner import CmdRunner


class PSTool:
    """ Stuff to use Powershell """

    def __init__(self, debug):
        self.rootDir = Path(__file__).parent.parent
        self.scriptPath = os.path.join(self.rootDir, 'ps/')
        self.debug = debug
        self.runner = CmdRunner()
        self.tool = ScriptTool(self.debug)

    def pathEndingSlash(self, path):
        """ check for ending slash at path """
        if path.endswith(os.path.sep) is False:
          path = "%s%s" % (path, os.path.sep)
        return path

    def chown(self, user, target):
      """ will change target to Ownership of user """
      # target is valid?
      path = Path(target)
      if path.is_dir():
        self.chownDir(user, path)
        return

      if path.is_file():
        self.chownFile(user, path)
        return

      # Error Handling
      print("The file/directory %s is not valid or does not exists! -exit-" % target)
      exit(-1)

    def chownDir(self, user, path):
      """ change Owner of directory recursive """
      self.tool.chownDir(user, path)

    def chownFile(self, user, filename):
      """ change Owner of this file """
      self.tool.chownFile(user, filename)
