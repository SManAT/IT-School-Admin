
class UserObj:
    lic = {
        'M365EDU_A3_FACULTY': 'L',
        'M365EDU_A3_STUUSEBNFT': 'S',
        # A1 für Lehrpersonen
        'STANDARDWOFFPACK_IW_FACULTY': 'V'
    }

    displayName = ""
    licenses = ""
    vorname = ""
    given_name = ""
    mail = ""
    nachname = ""

    def __str__(self):
        return "%s %s %s %s %s" % (self.displayName,
                                   self.vorname,
                                   self.nachname,
                                   self.mail,
                                   self.licenses
                                   )

    def getVorname(self):
        return self.vorname

    def getNachname(self):
        return self.nachname

    def getMail(self):
        return self.mail

    def getLicensesOLD(self, vips):
        """
        get Licences, check if ist vip user
        M365EDU_A3_FACULTY            > A3 Lehrer
        M365EDU_A3_STUUSEBNFT         > A3 Schüler
        STANDARDWOFFPACK_IW_FACULTY   > A1 Lehrer
        """
        print(self.licenses)
        # MehrfachLizenzen sind durch SPACE getrennt
        parts = self.licenses.split(" ")
        for p in parts:
            for key, value in self.lic.items():
                if p.lower() == key.lower():
                    # check if VIP wenn keine A3 Lehrer
                    if p.lower() != "M365EDU_A3_FACULTY".lower():
                        for v in vips['vips']:
                            if self.compareVip(v):
                                return 'V'
                        return value
        return None

    def getLicenses(self, vips):
        """
        get Licences, check if ist vip user
        M365EDU_A3_FACULTY            > A3 Lehrer
        M365EDU_A3_STUUSEBNFT         > A3 Schüler
        STANDARDWOFFPACK_IW_FACULTY   > A1 Lehrer
        """
        for key, value in self.lic.items():
          search_index = self.licenses.find(key)
          if search_index != -1:
            # print(f"Search in {self.licenses} for {key} position {search_index}")

            # check if VIP wenn keine A3 Lehrer Lizenz
            if key != "M365EDU_A3_FACULTY":
              for v in vips['vips']:
                  if self.compareVip(v):
                      return 'V'
            # return Value S, L
            return value
        return None

    def compareVip(self, vip):
        """ vip Vorname Nachname oder umgekehrt """
        parts = vip.split(" ")
        vorname = parts[0]
        nachname = parts[1]

        if vorname.lower() == self.vorname.lower() and nachname.lower() == self.nachname.lower():
            # print("VIP: %s %s" % (self.vorname, self.nachname))
            return True
        else:
            # Namen vertauschen
            if nachname.lower() == self.vorname.lower() and vorname.lower() == self.nachname.lower():
                # print("VIP: %s %s" % (self.vorname, self.nachname))
                return True
        return False
