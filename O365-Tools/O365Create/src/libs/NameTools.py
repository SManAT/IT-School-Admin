
class NameTools:
    """ Class for handling real Names """
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

    def getVorname(self, vorname, reduce=True):
        """
        get Vorname
        :param reduce: Von Doppelnamen nur den ersten Namen nehmen
        """
        v = vorname
        # only 1 Vorname
        if reduce:
            parts = vorname.split(" ")
            if len(parts) > 1:
                # nimm nur den ersten Vornamen
                v = parts[0]

        # first Letter to uppercase
        erg = v[0].upper() + v[1:]
        return erg

    def getNachname(self, nachname):
        """
        get Vorname
        Wenn Doppelnamen dann mit -, z.B. Huber Hansl > Huber-Hansel
        """
        parts = nachname.split(" ")
        new_nachname = nachname

        if len(parts) > 1:
          new_nachname = ""
          for p in parts:
            p = p.strip()
            # spanisch not
            if p == 'de':
              new_nachname += p + "-"
            else:
              # first Letter to uppercase
              new_nachname += p[0].upper() + p[1:] + "-"

          # delte last -
          new_nachname = new_nachname[:-1]

        return new_nachname
