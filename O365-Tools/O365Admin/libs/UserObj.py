
class UserObj:
    lic = {
      'M365EDU_A3_FACULTY': 'L',
      'M365EDU_A3_STUUSEBNFT': 'S',
      'STANDARDWOFFPACK_IW_FACULT': 'V'
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

    def getLicenses(self, vips):
      """ get Licences, check if ist vip user """
      """
      FLOW_FREE;M365EDU_A3_FACULTY = Lehrer
      M365EDU_A3_STUUSEBNFT        = Student
      """
      parts = self.licenses.split(";")
      for p in parts:
        for key, value in self.lic.items():
          if p.lower() == key.lower():
            # check if VIP
            for v in vips['vips']:
              if self.compareVip(v):
                return 'V'
            return value
      return None

    def compareVip(self, vip):
      """ vip Vorname Nachname oder umgekehrt """
      parts = vip.split(" ")
      vorname = parts[0]
      nachname = parts[1]

      if vorname.lower() == self.vorname.lower() and nachname.lower() == self.nachname.lower():
        return True
      else:
        # Namen vertauschen
        if nachname.lower() == self.vorname.lower() and vorname.lower() == self.nachname.lower():
          return True
      return False
