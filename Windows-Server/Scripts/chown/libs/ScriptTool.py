import os
import sys
from pathlib import Path
from libs.CmdRunner import CmdRunner
import time
import fnmatch


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
      # dont use comments
      if not line.startswith("#"):
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

  def _execute(self, script, override_debug=False):
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

  def change(self, psfile, user, filename):
    # Set Owner -----
    psTemplate = psfile
    cmdarray = self.loadScript(psTemplate)
    cmdarray = self.modifyScript(cmdarray, user, filename)
    self.createScript(cmdarray, psTemplate)
    psFile = os.path.join(self.tmpPath, psTemplate)

    if self.debug is False:
      self._execute(psFile)

    # grant Permissions to this owner
    psTemplate = "setPermission.ps1"
    cmdarray = self.loadScript(psTemplate)
    cmdarray = self.modifyScript(cmdarray, user, filename)
    self.createScript(cmdarray, psTemplate)
    psFile = os.path.join(self.tmpPath, psTemplate)
    if self.debug is False:
      self._execute(psFile)

  def chownFile(self, user, filename):
    """ change Owner of File and set Permissions to Full Control """
    print("chown %s %s" % (user, filename))
    self.change("chownFile.ps1", user, filename)

  def chownSingleDir(self, user, dir):
    """ change Owner of File and set Permissions to Full Control """
    print("chown %s %s" % (user, dir))
    self.change("chownDir.ps1", user, dir)
    
  def getFileExtension(self, filename):
    """ get Extension of a File without . """
    return os.path.splitext(filename)[1][1:].strip().lower()

  def getSubDirs(self, rootdir):
    """ get alls Subdirectories from rootdir """
    erg = []
    for it in os.scandir(rootdir):
      if it.is_dir():
        erg.append(it.path)
        self.getSubDirs(it)
    return erg

  def search_files(self, directory='.', pattern='.*'):
    """
    search for pattern in directory recursive
    :param directory: path where to search. relative or absolute
    :param pattern: a list e.g. ['*.jpg', '__.*']
    """
    data = []
    for dirpath, dirnames, files in os.walk(directory):
      for p in pattern:        
        for f in fnmatch.filter(files, p):
          data.append(os.path.join(dirpath, f))
    return data

  def chownDir(self, user, path):
    """ change Owner of Directory and set Permissions to Full Control recursive """
    print("chown -R %s %s" % (user, path))

    # chmod dirs
    dirs = self.getSubDirs(path)
    for p in dirs:
      print(p)
      self.chownSingleDir(user, p)
    
    # chmod files
    files = self.search_files(path)
    for f in files:
      pass
      #print(f)
      #self.chownFile(user, f)

    
