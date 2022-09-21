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

    def setVorname(self, value):
        self.vorname = self.test(value)

    def setNachname(self, value):
        self.nachname = self.test(value)

    def setUsername(self, value):
        self.username = self.test(value)

    def setEmail(self, value):
        self.email = self.test(value)

    def setGruppe(self, value):
        self.gruppe = self.test(value)

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
