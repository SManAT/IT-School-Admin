import os
from pathlib import Path
import re
import subprocess
import sys

import questionary
from rich.table import Table
from startfile import startfile
import yaml

from libs.CSVTool import CSVTool
from libs.GlobalConsole import console
from libs.Questions import Questions


# cross-plattform os.startfile
class O365():

  def __init__(self):
    self.rootDir = Path(__file__).parent
    self.filesPath = os.path.join(self.rootDir, 'files')
    self.configFile = os.path.join(self.rootDir, 'config.yaml')
    self.infoFile = os.path.join(self.rootDir, 'Informationen.txt')
    self.config = self.load_yml()

    # check dir files and Email.txt File
    self.createDir(self.filesPath)
    if os.path.exists(os.path.join(self.filesPath, self.config['files']['emailFile'])) is False:
      with open(os.path.join(self.filesPath, self.config['files']['emailFile']), 'w') as fp:
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
        # die Erzeugungsfiles ausblenden
        if child.name != self.config['files']['importFile'] and child.name != self.config['files']['serienbriefFile']:
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
    console.print("[info]Verwenden Sie diese Datei als Vorlage für den Import neuer Schüler Accounts ...[/]")

  def showInformations(self):
    """ give an overview """
    with open(self.infoFile, 'r', encoding="utf-8") as f:
      lines = f.readlines()
    for line in lines:
      console.print(line.replace('\n', ''))

  def importSokrates(self):
    """ Import Sokrates Liste """
    csvFiles = self.search_files_in_dir(self.filesPath, ['.csv'])
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
        self.filesPath, self.config['files']['serienbriefFile'] ), accounts)

    # Massenimport erstellen
    csv.writeO365Export(os.path.join(
        self.filesPath, self.config['files']['importFile']), accounts)
    console.print(f"Importfile für O365 erstellt ({self.config['files']['importFile']})")
    console.print("Mit dieser Datei den Massenimport bei O365 durchführen und auf das Email warten ...")
    console.print(f"Den Email Text in die Datei {self.config['files']['emailFile']} kopieren und das Tool erneut starten ...")
    console.print(f"Die Datei {self.config['files']['serienbriefFile']} kann im Anschluss zum ertsellen der Serienbriefe verwendet werden ...")
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

    console.print(table)

  def serienbrief(self):
    """ Import Email Text and create Serienbriefdokument"""

    f = open(os.path.join(self.filesPath, self.config['files']['emailFile']),
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
    csvFile = os.path.join(self.filesPath, self.config['files']['serienbriefFile'] )
    if (os.path.exists(csvFile) is True):
      csv = CSVTool(self.config)
      accounts = csv.readExportFile(csvFile)
      # Abgleichen
      for account in accounts:
        for email in allUsers:
          if account.benutzername == email[0]:
            # Passwd setzen
            account.password = email[1].strip()
            break

    self.printTable(accounts)

    csv.writeSerienbrief(os.path.join(
        self.filesPath, self.config['files']['serienbriefFile'] ), accounts)
    console.print("Serienbrief CSV Datei erstellt (%s)" % self.config['files']['serienbriefFile'] )
    console.print("Damit bitte Infoblatt für die Schüler ausdrucken oder zukommen lassen ...")
    console.print("Fertige Datei auch am Sharepoint ablegen für die KV's ...")
    self.openFileManager(self.filesPath)


def start():
  debug = False
  o365 = O365()

  questions = Questions()
  if debug is True:
    console.print("[info]DEBUGGING :::[/]")
    a = 'import'
  else:
    a = questions.MainMenue()

  if a == 'import':
    o365.importSokrates()

  if a == 'vorlage':
    o365.vorlage()

  if a == 'serienbrief':
    o365.serienbrief()

  if a == 'info':
    o365.showInformations()


if __name__ == "__main__":
  start()
