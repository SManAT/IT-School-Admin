from multiprocessing import Lock
import re
import sys
import threading
import time

from libs.UserObj import UserObj
from libs.UserSokrates import UserSokrates

# Amalie Loderer
# Ginic


class Compare():
  # needed for printing
  lock = Lock()

  def __init__(self, azure, sokrates, cryptor, encrypt, vips):
    self.azure = azure
    self.sokrates = sokrates
    self.cryptor = cryptor
    self.encrypt = encrypt
    self.vips = vips

    self.delete = []

    self.thread = threading.Thread(target=self.run, args=())
    self.thread.daemon = True

  def start(self):
    self.thread.start()

  def getThread(self):
    return self.thread

  def setAzureUser(self, obj: UserObj):
    self.aUser = obj

  def setSokratesUser(self, obj: UserSokrates):
    self.sUser = obj

  def getDelete(self):
    """ all User which can be deleted """
    return self.delete

  def normalize(self, thestr):
    patterns = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'ß': 'ss',
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'ë': 'e',
        'á': 'a',
        'à': 'a',
        'â': 'a',
        'î': 'i',
        'ï': 'i',
        'ç': 'c',
        'ú': 'u',
        'ù': 'u',
        'û': 'u',
        'ò': 'o',
        'ó': 'o',
        'ô': 'o',
        'š': 's',
        'ć': 'c',
        'č': 'c',
        'ň': 'n',
    }
    thestr = str(thestr)
    for key, val in patterns.items():
      thestr = thestr.replace(key, val)
    return thestr

  def compareNames(self, avorname, anachname, svorname, snachname):
    """ vergl, Vor und Nachnamen und auch mit tauschen """
    if avorname.lower() == svorname.lower() and anachname.lower() == snachname.lower():
      return True
    # Vor-Nachname tauschen
    if avorname.lower() == snachname.lower() and anachname.lower() == svorname.lower():
      return True
    return False

  def getNameParts(self, name):
    """ Doppelnamen aufbrechen """
    parts = re.split(r'[\ _\-]', name)
    return parts

  def compareDoppelnamen(self, name1, name2):
    p1 = self.getNameParts(name1)
    p2 = self.getNameParts(name2)

    # bool array, nur wenn alle flags = True passt der Name
    size = len(p1)
    if len(p2) > size:
      size = len(p2)
    flags = [False] * size

    index = 0
    for n1 in p1:
      for n2 in p2:
        if n1.lower() in n2.lower():
          flags[index] = True
      index += 1

    erg = True
    for f in flags:
      if f is False:
        erg = False
    return erg

  def compareDoubleNames(self, avorname, anachname, svorname, snachname):
    """
    vergl, Vor und Nachnamen auf Doppelname und auch mit tauschen
    """
    # Debugging --------------------------------
    testname = "diego"
    # print(type(avorname))
    if testname == avorname.lower():
      if testname == svorname.lower():
        k = 0
    testname = "Yousefzadeh".lower()
    if testname == anachname.lower():
      if testname == snachname.lower():
        k = 0

    #avorname = "Anna"
    #svorname = "Anna-Patricia"

    # Debugging --------------------------------

    # Vor- Nachname vertauscht
    if avorname.lower() in svorname.lower() and anachname.lower() in snachname.lower():
      return True
    if avorname.lower() in snachname.lower() and anachname.lower() in svorname.lower():
      return True

    # split Doppelname -----
    nachnamepart = self.compareDoppelnamen(anachname, snachname)
    if nachnamepart is False:
      # teste Azure > Sokrates und Sokrates -> Azure
      if anachname.lower() in snachname.lower() or snachname.lower() in anachname.lower():
        nachnamepart = True

    # Vorname -----
    vornameepart = self.compareDoppelnamen(avorname, svorname)
    if vornameepart is False:
      # teste Azure > Sokrates und Sokrates -> Azure
      if avorname.lower() in svorname.lower() or svorname.lower() in avorname.lower():
        vornameepart = True

    # Falls Vor und Nachname passen dann treffer
    if vornameepart is True and nachnamepart is True:
      return True

    return False

  def getName(self, what):
    if self.encrypt:
      return self.cryptor.decrypt(what.decode())
    else:
      return what

  def searchVIP(self, aUser):
    found = False
    for vip in self.vips['vips']:
      avorname = self.getName(aUser.vorname)
      anachname = self.getName(aUser.nachname)

      parts = vip.split(" ")
      svorname = parts[0].strip()
      snachname = parts[1].strip()

      if self.compareNames(avorname, anachname, svorname, snachname):
        found = True
        break

      avorname = self.normalize(self.getName(aUser.vorname))
      anachname = self.normalize(self.getName(aUser.nachname))
      svorname = self.normalize(parts[0])
      snachname = self.normalize(parts[1])
      if self.compareDoubleNames(avorname, anachname, svorname, snachname):
        found = True
        break

    return found

  def run(self):
    """ compare Azure User against Sokrates User """

    for aUser in self.azure:
      print(".", end="")
      sys.stdout.flush()

      # CPU breath
      time.sleep(0.01)

      found = False
      # keine Lehrer keine Vips aus DB
      # oder keine Vips falls nur config verändert
      if aUser.licenses == 'L' or aUser.licenses == 'V' or self.searchVIP(aUser):
        found = True
      else:
        for sUser in self.sokrates:
          # print(type(aUser.vorname.decode()))
          avorname = self.getName(aUser.vorname)
          anachname = self.getName(aUser.nachname)
          svorname = self.getName(sUser.vorname)
          snachname = self.getName(sUser.nachname)

          if self.compareNames(avorname, anachname, svorname, snachname):
            found = True
            break

          # Sonderzeichen herausnehmen ....
          # print(type(aUser.vorname.decode()))
          avorname = self.normalize(self.getName(aUser.vorname))
          anachname = self.normalize(self.getName(aUser.nachname))
          svorname = self.normalize(self.getName(sUser.vorname))
          snachname = self.normalize(self.getName(sUser.nachname))

          if self.compareDoubleNames(avorname, anachname, svorname, snachname):
            found = True
            break

      if found is False:
        # gibt es nicht mehr
        if self.encrypt:
          user = UserObj()
          user.nachname = self.cryptor.decrypt(
              aUser.nachname.decode())
          user.vorname = self.cryptor.decrypt(aUser.vorname.decode())
          user.mail = self.cryptor.decrypt(aUser.mail.decode())

          self.delete.append(user)
        else:
          self.delete.append(aUser)

    return False
