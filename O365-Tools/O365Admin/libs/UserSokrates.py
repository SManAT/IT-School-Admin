
class UserSokrates:
    vorname = ""
    nachname = ""

    def __str__(self):
        return "%s %s" % (self.vorname, self.nachname)

    def getVorname(self):
      return self.vorname

    def getNachname(self):
      return self.nachname

