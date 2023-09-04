from libs.NameTools import NameTools


class UserObj:
    domain = ""
    klasse = ""
    vorname = ""
    nachname = ""
    benutzername = ""
    password = ""

    def __init__(self):
      self.nameTools = NameTools()

    def __str__(self):
        return "%s %s %s %s %s" % (self.klasse,
                                   self.vorname,
                                   self.nachname,
                                   self.benutzername,
                                   self.password
                                   )

    def setDomain(self, domain):
        self.domain = domain

    def getAnzeigename(self):
        return "%s %s" % (self.nameTools.getVorname(self.vorname), self.nameTools.getNachname(self.nachname))

    def getBenutzername(self):
        v = self.nameTools.getVorname(self.vorname)
        n = self.nameTools.getNachname(self.nachname)
        return "%s.%s@%s" % (self.nameTools.normalize(v), self.nameTools.normalize(n), self.domain)

    def setBenutzername(self):
        v = self.nameTools.getVorname(self.vorname)
        n = self.nameTools.getNachname(self.nachname)
        self.benutzername = "%s.%s@%s" % (
            self.nameTools.normalize(v), self.nameTools.normalize(n), self.domain)

    def getVorname(self, reduce=True):
        """
        get Vorname
        :param reduce: Von Doppelnamen nur den ersten Namen nehmen
        """
        # only 1 Vorname
        return self.nameTools.getVorname(self.vorname, reduce)

    def getNachname(self):
        """
        get Vorname
        Wenn Doppelnamen dann mit -, z.B. Huber Hansl > Huber-Hansel
        """
        return self.nameTools.getNachname(self.nachname)

    def getKlasse(self):
        return self.klasse

    def getPasswort(self):
        return self.password
