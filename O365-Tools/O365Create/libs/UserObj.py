
class UserObj:
    domain = ""
    klasse = ""
    vorname = ""
    nachname = ""
    benutzername = ""
    password = ""

    def __str__(self):
        return "%s %s %s %s %s" % (self.klasse,
                                   self.vorname,
                                   self.nachname,
                                   self.benutzername,
                                   self.password
                                   )

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
        }
        thestr = str(thestr)
        for key, val in patterns.items():
            thestr = thestr.replace(key, val)
        return thestr

    def setDomain(self, domain):
        self.domain = domain

    def getBenutzername(self):
        v = self.getVorname(True)
        n = self.getNachname()

        return "%s.%s@%s" % (self.normalize(v), self.normalize(n), self.domain)

    def getVorname(self, reduce=False):
        """
        get Vorname
        :param reduce: Von Doppelnamen nur den ersten Namen nehmen
        """
        # only 1 Vorname
        v = self.vorname
        if reduce:
            parts = self.vorname.split(" ")
            if len(parts) > 1:
                # nimm nur den ersten Vornamen
                v = parts[0]

        # first Letter to uppercase
        erg = v[0].upper() + v[1:]
        return erg

    def getNachname(self):
        # first Letter to uppercase
        erg = self.nachname[0].upper() + self.nachname[1:]
        return erg

    def getKlasse(self):
        return self.klasse

    def getPasswort(self):
        return self.password
