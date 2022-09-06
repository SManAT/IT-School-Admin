
class UserObj:
    vorname = ""
    password = ""
    mail = ""
    nachname = ""

    def __str__(self):
        return "%s %s %s %s %s" % (self.vorname,
              self.nachname,
              self.mail,
              self.password
              )

    def getVorname(self):
      return self.vorname

    def getNachname(self):
      return self.nachname

    def getMail(self):
      return self.mail

