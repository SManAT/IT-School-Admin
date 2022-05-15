import os
import logging
import sys

from libs.CmdRunner import CmdRunner


class ScriptTool():
  """ Stuff to Scripts, Filemanagement """

  def __init__(self, rootDir, config=None, debug=False, counter=None):
    self.logger = logging.getLogger('ScriptTool')
    self.tmpPath = os.path.join(rootDir, 'tmp/')
    self.scriptPath = os.path.join(rootDir, 'ps/')
    self.config = config
    self.debug = debug
    self.counter = counter
    self.runner = CmdRunner()

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

  def unblockFile(self, filename):
    """ Use the Unblock cmd from PS """
    cmd = "Unblock-File -Path %s" % filename
    self.runner.runCmd(cmd)

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

  def debugOutput(self, data):
    """ just Debug Output """
    for line in data:
      line = line.replace('\n', '')
      print(line)

  def _execute(self, psTemplate, user):
    """ load Code from PS File, replace variables and excute it """
    cmdarray = self.loadScript(psTemplate)
    cmdarray = self.modifyScript(cmdarray, user)

    # self.debugOutput(cmdarray)
    cmd = self.createCmd(cmdarray)

    if self.debug is False:
      self.runner.runCmd(cmd)
    return self.runner.getStdout()

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
    # Do the JOB
    print("Adding User %s to Group: %s " % (user.getFullname(), user.getGruppe()))
    self._execute("addToGroup.ps1", user)

  def addUser(self, user):
    """ add User via Powershell Script """
    if self.groupExists(user) or self.debug is True:
        # Do the JOB
      print("Creating User: %s " % user.getFullname())

      if self.debug is False:
        answer = self._execute("addUser.ps1", user)
        print(answer)
      self.counter.incUser()

      # Add User to Goup -------------------------------------------------
      self.addUser2Group(user)
    else:
      self.counter.incWrongGroups()
      print("AD Group %s does not exists! User %s will be not created!" % (user.getGruppe(), user.getFullname()))
