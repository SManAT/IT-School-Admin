import os
from pathlib import Path
import re
import subprocess
import sys

import questionary
from rich.console import Console
from rich.table import Table
from startfile import startfile
import yaml

from libs.CSVTool import CSVTool
from libs.MyConsole import MyConsole
from libs.Questions import Questions


# cross-plattform os.startfile
class O365():
  finishFile = "O365Created-Users-Finished.csv"
  emailFile = "Email.txt"

  def __init__(self):
    self.rootDir = Path(__file__).parent
    self.filesPath = os.path.join(self.rootDir, 'files')
    self.configFile = os.path.join(self.rootDir, 'config.yaml')
    self.config = self.load_yml()
    self.console = MyConsole()

    # check dir files and Email.txt File
    self.createDir(self.filesPath)
    if os.path.exists(os.path.join(self.filesPath, self.emailFile)) is False:
      with open(os.path.join(self.filesPath, self.emailFile), 'w') as fp:
        pass
      fp.close()

  def createDir(self, path):
    """ create dir if it not exists """
    if os.path.isdir(path) is False:
      os.mkdir(path)

  def load_yml(self):
    """ Load the yaml file config.yaml """
    with open(self.configFile, 'rt') as f:
      yml = yaml.safe_load(f.read())
    return yml

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
      csv = CSVTool(self.config)
      accounts = csv.readSokrates(csvFile)
      self.printTable(accounts)

    # Serienbrief Dokument gleich erstellen
    csv.writeSerienbrief(os.path.join(
        self.filesPath, self.finishFile), accounts)

    # Massenimport erstellen
    csv.writeO365Export(os.path.join(
        self.filesPath, "O365-Import-File.csv"), accounts)
    print("Importfile für O365 erstellt (O365-Import-File.csv)")
    print("Mit dieser Datei den Massenimport bei O365 durchführen und auf das Email warten ...")
    self.openFileManager(self.filesPath)

  def printTable(self, data):
    # see https://rich.readthedocs.io/en/stable/appendix/colors.html
    table = Table(title="Users that may deleted")
    table.add_column("Nr", style="yellow", no_wrap=True)
    table.add_column("Vorname", style="magenta")
    table.add_column("Nachname", style="magenta")
    table.add_column("Klasse", style="green")
    table.add_column("O365", style="yellow2")
    table.add_column("Pwd", style="yellow2")

    i = 1
    for item in data:
      table.add_row(str(i), str(item.vorname), str(
          item.nachname), str(item.klasse), str(item.benutzername), str(item.password))
      i += 1

    console = Console()
    console.print(table)

  def email(self):
    """ Import Email Text and create Serienbriefdokument"""

    f = open(os.path.join(self.filesPath, self.emailFile),
             "r", encoding="utf-8")
    emailLines = f.read()

    lines = emailLines.splitlines()
    nextIsPassword = False
    userData = []
    allUsers = []
    for line in lines:
      line = line.strip()
      if len(line) > 0:
        # Detect Benutzername:
        match = re.match(r'Benutzername\:(.*)', line)
        if match:
          benutzer = match.group(1).strip()
          nextIsPassword = True
          userData.append(benutzer)

        if nextIsPassword is True:
          # Detect Kennwort:
          match = re.match(r'.*Kennwort\:(.*)', line)
          if match:
            pwd = match.group(1).strip()
            nextIsPassword = False
            userData.append(pwd)
            allUsers.append(userData)
            userData = []

    # -------------------------------------------------------------------------------
    # Passwörter in Serienbrief Dokument setzen
    csvFile = os.path.join(self.filesPath, self.finishFile)
    if (os.path.exists(csvFile) is True):
      csv = CSVTool(self.config)
      accounts = csv.readFinishFile(csvFile)
      # Abgleichen
      for account in accounts:
        for email in allUsers:
          if account.benutzername == email[0]:
            # Passwd setzen
            account.password = email[1].strip()
            break

    self.printTable(accounts)

    csv.writeSerienbrief(os.path.join(
        self.filesPath, self.finishFile), accounts)
    print("Serienbrief CSV Datei erstellt (%s)" % self.finishFile)
    print("Damit bitte Infoblatt für die Schüler ausdrucken oder zukommen lassen ...")
    print("Fertige Datei auch am Sharepoint ablegen für die KV's ...")
    self.openFileManager(self.filesPath)


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
