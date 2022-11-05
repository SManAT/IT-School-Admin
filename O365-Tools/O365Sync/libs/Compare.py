#!!!!!!!!!!!! ó = o
from multiprocessing import Lock
import re
import sys
import threading

from requests_oauthlib.compliance_fixes.mailchimp import mailchimp_compliance_fix

from libs.UserObj import UserObj
from libs.UserSokrates import UserSokrates


# VIPS fehlen# H.Dietl-L  Johannes  STANDARDWOFFPACK_IW_FACULTY
# Odegaard      Doppelnamen
# Paulina Lara  Doppelnamen
# Zalan > Zalán
class Compare():
  # needed for printing
    lock = Lock()

    def __init__(self, azure, sokrates, cryptor, encrypt):
        self.azure = azure
        self.sokrates = sokrates
        self.cryptor = cryptor
        self.encrypt = encrypt
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

    def compareDoubleNames(self, avorname, anachname, svorname, snachname):
        """ vergl, Vor und Nachnamen auf Doppelname und auch mit tauschen 
        # Nachname Doppelname
          Steiner Pérez
          Schönfelder-Kickinger
        """
        # Debugging --------------------------------
        testname = "diego"
        # print(type(avorname))
        if testname == avorname.lower():
            if testname == svorname.lower():
                k = 0
        testname = "lentschig"
        if testname == anachname.lower():
            if testname == snachname.lower():
                k = 0
        # Debugging --------------------------------

        if avorname.lower() in svorname.lower() and anachname.lower() in snachname.lower():
            return True
        if avorname.lower() in snachname.lower() and anachname.lower() in svorname.lower():
            return True
        # split Doppelname
        nachnamepart = False
        parts = re.split(' |-', anachname)
        if len(parts) > 1:
            for p in parts:
                # check in Nachname Sokrates
                if p.lower() in snachname.lower():
                    nachnamepart = True
                    break
        # Vorname -----
        parts = re.split(' |-', avorname)
        vornameepart = False
        if len(parts) > 1:
            for p in parts:
                # check in Nachname Sokrates
                if p.lower() in svorname.lower():
                    vornameepart = True
                    break

        # Falls Vor und Nachname passen dann treffer
        if vornameepart is True and nachnamepart is True:
            return True

        return False

    def run(self):
        """ compare Azure User against Sokrates User """

        for aUser in self.azure:
            print(".", end="")
            sys.stdout.flush()

            found = False

            # keine Lehrer keine Vips
            if aUser.licenses == 'L' or aUser.licenses == 'V':
                found = True
            else:
                for sUser in self.sokrates:
                    if self.encrypt:
                        # print(type(aUser.vorname.decode()))
                        avorname = self.cryptor.decrypt(aUser.vorname.decode())
                        anachname = self.cryptor.decrypt(
                            aUser.nachname.decode())
                        svorname = self.cryptor.decrypt(sUser.vorname.decode())
                        snachname = self.cryptor.decrypt(
                            sUser.nachname.decode())
                    else:
                        avorname = aUser.vorname
                        anachname = aUser.nachname
                        svorname = sUser.vorname
                        snachname = sUser.nachname
                    if self.compareNames(avorname, anachname, svorname, snachname):
                        found = True
                        break

                    # Sonderzeichen herausnehmen ....
                    if self.encrypt:
                        # print(type(aUser.vorname.decode()))
                        avorname = self.normalize(
                            self.cryptor.decrypt(aUser.vorname.decode()))
                        anachname = self.normalize(self.cryptor.decrypt(
                            aUser.nachname.decode()))
                        svorname = self.normalize(
                            self.cryptor.decrypt(sUser.vorname.decode()))
                        snachname = self.normalize(self.cryptor.decrypt(
                            sUser.nachname.decode()))
                    else:
                        avorname = self.normalize(aUser.vorname)
                        anachname = self.normalize(aUser.nachname)
                        svorname = self.normalize(sUser.vorname)
                        snachname = self.normalize(sUser.nachname)

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
