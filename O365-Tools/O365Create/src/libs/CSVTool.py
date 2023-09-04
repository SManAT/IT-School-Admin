import os
import pandas

from libs.GlobalConsole import console
from libs.UserObj import UserObj


class CSVTool():
    """ Read / Write CSV Files with pandas """
    userList = []

    def __init__(self, config):
        self.config = config
        self.domain = self.config['config']['domain']

    def getUsers(self):
        """ return all Users from CSV File """
        return self.userList

    def readSokrates(self, filename):
        """ Read a CSV file """
        self.userList.clear()

        if os.path.exists(filename) is True:
            try:
                df = pandas.read_csv(filename, sep=',')

                for index, row in df.iterrows():  # noqa
                    user = UserObj()
                    user.setDomain(self.domain)
                    user.vorname = str(row['Vorname']).strip()
                    user.nachname = str(row['Familienname']).strip()
                    user.klasse = str(row['Klasse']).strip()
                    user.setBenutzername()

                    self.userList.append(user)
            except Exception:
                console.error(
                    "Parsing csv File Error, is the seperator ',' ?")
                exit()
        else:
            print("File ./%s not found! - exit -" % filename)
        return self.userList

    def readFinishFile(self, filename):
        """ Read a CSV file """
        self.userList.clear()

        if os.path.exists(filename) is True:
            try:
                df = pandas.read_csv(filename, sep=',')
                for index, row in df.iterrows():  # noqa
                    user = UserObj()
                    user.setDomain(self.domain)
                    user.vorname = str(row['Vorname']).strip()
                    user.nachname = str(row['Nachname']).strip()
                    user.klasse = str(row['Klasse']).strip()
                    user.benutzername = str(row['O365Benutzername']).strip()

                    self.userList.append(user)
            except Exception as ex:
                console.error(
                    "Parsing csv File Error, is the seperator ',' ?")
                print(ex)
                exit()
        else:
            print("File ./%s not found! - exit -" % filename)
        return self.userList

    def writeO365Export(self, filename, data):
        """ Write data to a CSV File """
        file1 = open(filename, "w", encoding="utf-8")
        header = "Benutzername,Vorname,Nachname,Anzeigename,Position,Abteilung,Telefon – Geschäftlich,Telefon (geschäftlich),Mobiltelefon,Fax,Alternative E-Mail-Adresse,Adresse,Ort,Bundesstaat,Postleitzahl,Land oder Region"
        file1.write("%s\n" % header)
        for d in data:
            file1.write("%s,%s,%s,%s,,,,,,,,,,,,%s\n" % (
                d.getBenutzername(), d.getVorname(), d.getNachname(), d.getAnzeigename(), "Österreich"))
        file1.close()

    def writeSerienbrief(self, filename, data):
        """ Write data to a CSV File """
        file1 = open(filename, "w", encoding="utf-8")
        header = "Klasse,Vorname,Nachname,O365Benutzername,Passwort"
        file1.write("%s\n" % header)
        for d in data:
            file1.write("%s,%s,%s,%s,%s\n" % (
                d.getKlasse(), d.getVorname(), d.getNachname(), d.getBenutzername(), d.getPasswort()))
        file1.close()

    def save(self, filename, data):
        """ Write data to a CSV File """
        df = pandas.DataFrame([vars(c) for c in data])
        df.to_csv(filename, sep=";")
