class User():
  """ single User Object """
  vorname = ""
  nachname = ""
  username = ""
  email = ""
  gruppe = ""
  # is the Userdata valid
  valid = False

  def __init__(self):
    pass

  def __str__(self):
    return "%s %s %s %s" % (self.vorname, self.nachname, self.username, self.email)

  def test(self, data):
    """ test if nan """
    if data == "nan":
      return ""
    else:
      return data

  def setVorname(self, str):
    self.vorname = self.test(str)

  def setNachname(self, str):
    self.nachname = self.test(str)

  def setUsername(self, str):
    self.username = self.test(str)

  def setEmail(self, str):
    self.email = self.test(str)

  def setGruppe(self, str):
    self.gruppe = self.test(str)

  def getVorname(self):
    return self.vorname

  def getNachname(self):
    return self.nachname

  def getUsername(self):
    return self.username

  def getEmail(self):
    return self.email

  def getGruppe(self):
    return self.gruppe

  def getFullname(self):
    return "%s %s" % (self.getNachname(), self.getVorname())

  def isValid(self):
    """ are the data valid? are all fields are set? """
    if self.getVorname() != "" and self.getNachname() != "" and self.getEmail() != "" and self.getGruppe() != "":
      return True
    else:
      return False
