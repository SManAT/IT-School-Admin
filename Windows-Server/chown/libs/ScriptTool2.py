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
    self.runner = CmdRunner()

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
    if self.debug is False or override_debug is True:
      self.runner.runPSFile(script)
    errors = self.runner.getStderr()
    if errors:
      print(errors)
    # Delete tmp Script
    time.sleep(0.5)
    if self.debug is False:
      self.rmFile(script)
    return self.runner.getStdout()

  def existsUser(self, user):
      """ check for User in Active Domain Forrest """
      answer = self._execute("existsUser.ps1", user)

      # analyse answer
      if answer.find('DistinguishedName') > -1:
        return True
      else:
        return False

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

  def change(self, psfile, user, filename):
    # Set Owner -----
    psTemplate = psfile
    cmdarray = self.loadScript(psTemplate)
    cmdarray = self.modifyScript(cmdarray, user, filename)
    cmd = self.createCmd(cmdarray)

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
      self.chownSingleDir(user, p)

    # chmod files
    files = self.search_files(path)
    for f in files:
      self.chownFile(user, f)
