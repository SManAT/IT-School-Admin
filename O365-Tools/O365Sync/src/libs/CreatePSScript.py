import os
import sys

from libs.GlobalConsole import console
from libs.UserObj import UserObj
from cryptography.fernet import Fernet


class CreatePSScript():
  def __init__(self, config, rootPath, filename, deleteData, keyFile):
    self.config = config
    self.rootPath = rootPath
    self.scriptPath = os.path.join(self.rootPath, 'scripts')
    self.filesPath = os.path.join(self.rootPath, 'files')
    self.deleteData = deleteData
    self.keyFile = keyFile

    # Cryptographie
    file = open(self.keyFile, 'rb')
    key = file.read()
    file.close()

    # encrypt
    self.fernet = Fernet(key)

    # get Admin Passwords
    hashstr = self.config["o365"]["password"]
    self.admin_password = self.decrypt(hashstr)

  def create(self):
    erg = []
    # Authentication Script
    originalLines = self.loadScript("deleteUserHeader.ps1")
    dummyUser = UserObj()
    lines = self.modifyScript(originalLines, dummyUser)
    for line in lines:
        erg.append(line)

    # User Scripts
    originalLines = self.loadScript("deleteUser.ps1")
    for user in self.deleteData:
      lines = self.modifyScript(originalLines, user)
      for line in lines:
        erg.append(line)

    self.save(erg, "deleteUsers.ps1")

  def loadScript(self, filename):
    """ load a PS Script """
    path = os.path.join(self.scriptPath, filename)
    if (os.path.exists(path) is False):
      console.print("[error]Script %s does not exist -abort-[/]" % path)
      sys.exit()
    else:
      with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
      return lines

  def decrypt(self, encMessage):
    """ decrypt a String """
    try:
      return self.fernet.decrypt(str.encode(encMessage)).decode()
    except Exception:
      print("\n")
      console.print(
          "[error]Wrong Encryption Key! Create a new one/or hash your password again in config/config.yml ...[/]")
      self.errors = True
      exit()

  def modifyScript(self, lines, user):
    erg = []
    for line in lines:
      line = line.replace("{% principal %}", user.mail)
      line = line.replace("{% username %}", self.config['o365']['username'])
      line = line.replace("{% password %}", self.admin_password)
      erg.append(line)
    return erg

  def save(self, lines, filename):
    filename = os.path.join(self.filesPath, filename)
    f = open(filename, "w", encoding='utf-8')
    for line in lines:
      f.write(line)
    f.close()
