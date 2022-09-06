import atexit
import os
from pathlib import Path
import subprocess
import sys

import questionary
from rich.console import Console
from rich.table import Table
from startfile import startfile

from libs.CSVTool import CSVTool
from libs.MyConsole import MyConsole
from libs.Questions import Questions


# cross-plattform os.startfile
class O365():

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.filesPath = os.path.join(self.rootDir, 'files')

        self.console = MyConsole()

        # catch terminating Signal
        atexit.register(self.exit_handler)

    def exit_handler(self):
        """ do something on sys.exit() """
        pass

    def openFileManager(self, path):
        """ cross OS """
        # MacOS
        try:
            if sys.platform == 'darwin':
                subprocess.check_call(['open', path])
            elif sys.platform.startswith('linux'):
                subprocess.check_call(['xdg-open', path])
            elif sys.platform == 'win32':
                subprocess.check_call(['explorer', path])
        except Exception:
            pass

    def search_files_in_dir(self, directory='.', pattern=''):
        """    
        search for pattern in directory NOT recursive
        :param directory: path where to search. relative or absolute
        :param pattern: a list e.g. ['.jpg', '.gif']
        """
        data = []
        for child in Path(directory).iterdir():
            if child.is_file():
                # print(f"{child.name}")
                if pattern == '':
                    data.append(os.path.join(directory, child.name))
                else:
                    for p in pattern:
                        if child.name.endswith(p):
                            data.append(os.path.join(directory, child.name))
        return data

    def vorlage(self):
        """ Open Vorlage File """
        startfile(os.path.join(self.rootDir, "Vorlage.csv"))

    def importSokrates(self):
        """ Import Sokrates Liste """
        csvFiles = self.search_files_in_dir(self.filesPath, '.csv')
        print("Bitte Nur Schüler aufnehmen, die einen Account bekommen sollen.")
        flist = []
        for f in csvFiles:
            flist.append(os.path.basename(f))
        a = questionary.select(
            "Welche CSV Datei?",
            choices=flist,
        ).ask()

        # check CSV Datei
        csvFile = os.path.join(self.filesPath, a)
        if (os.path.exists(csvFile) is True):
            csv = CSVTool()
            accounts = csv.readSokrates(csvFile)
            self.printTable(accounts)

        # Serienbrief Dokument gleich erstellen
        csv.writeSerienbrief(os.path.join(
            self.filesPath, "O365Created-Users-Finished.csv"), accounts)

        # Massenimport erstellen
        csv.writeO365Export(os.path.join(
            self.filesPath, "O365-Import-File.csv"), accounts)
        print("Importfile für O365 esrtellt (O365-Import-File.csv)")
        print("Mit dieser Datei den Massenimport bei O365 durchführen und auf das Email warten ...")
        self.openFileManager(self.filesPath)

    def printTable(self, data):
        table = Table(title="Users that may deleted")
        table.add_column("Nr", style="cyan", no_wrap=True)
        table.add_column("Vorname", style="magenta")
        table.add_column("Nachname", style="green")
        table.add_column("Klasse", style="yellow")

        i = 1
        for item in data:
            table.add_row(str(i), str(item.vorname), str(
                item.nachname), str(item.klasse))
            i += 1

        console = Console()
        console.print(table)

    def email(self):
        """ Import Email Text and create Serienbriefdokument"""
        test = """   
 
Ein Benutzerkonto wurde erstellt oder geändert.
 
Benutzername: Hannah.Burger@frauengasse.eu
Kennwort: Wob17361
 
 
Nächste Schritte:

    Teilen Sie diese Informationen mit ihren Benutzern.
"""


def start():
    o365 = O365()
    questions = Questions()
    a = questions.MainMenue()

    if a == 'import':
        o365.importSokrates()

    if a == 'vorlage':
        o365.vorlage()

    if a == 'email':
        o365.email()


if __name__ == "__main__":
    start()
