import atexit
import os
from pathlib import Path
import shutil
import sys

from rich.table import Table
import yaml

from libs.AzurePS import AzurePS
from libs.CSVTool import CSVTool
from libs.Compare import Compare
from libs.Cryptor import Cryptor
from libs.Database import Database
from libs.Loader import Loader
from libs.Questions import Questions

from libs.GlobalConsole import console


class O365():

  # where to store O365 Users temorary
  csvFilename = "licencedUsers.csv"

  def __init__(self, debug):
    self.rootDir = Path(__file__).parent

    self.debug = debug
    self.debugPath = os.path.join(self.rootDir, 'debug')
    if self.debug:
      self.createDir(self.debugPath)
    else:
      self.deleteDir(self.debugPath)

    self.createDir(os.path.join(self.rootDir, 'config'))
    self.createDir(os.path.join(self.rootDir, 'db'))
    self.createDir(os.path.join(self.rootDir, 'files'))

    self.filesDir = os.path.join(self.rootDir, 'files')

    self.keyFile = os.path.join(self.rootDir, 'config', 'key.key')
    # will create Key if not exists
    self.cryptor = Cryptor(self.keyFile)

    self.dbPath = os.path.join(self.rootDir, "db", "database.db")
    self.configFile = os.path.join(self.rootDir, 'config', 'config.yaml')
    self.infoFile = os.path.join(self.rootDir, 'Informationen.txt')
    self.scriptPath = os.path.join(self.rootDir, 'scripts')
    self.config = self.load_yml()

    self.vipFile = os.path.join(self.rootDir, 'config', 'vip.yaml')

    self.encrypt = False
    try:
      if self.config['DB']['encrypt'] == 1:
        self.encrypt = True
        console.print("[warning]Data is ENCRYPTED! ... [/]\n")
      else:
        console.print("[error]Debugging ... NOT encrypting data! ... [/]\n")
    except:
      console.print("[error]Debugging ... NOT encrypting data! ... [/]\n")

    if (os.path.exists(self.vipFile) is False):
      self.createEmptyVipFile()
    else:
      self.vips = self.load_vips()

    # Database Setup --------------------------
    self.DBSetup()
    # catch terminating Signal
    atexit.register(self.exit_handler)

  def exit_handler(self):
    """ do something on sys.exit() """
    pass

  def createDir(self, path):
    """ create dir if it not exists """
    if os.path.isdir(path) is False:
      os.mkdir(path)

  def deleteDir(self, path):
    """ delete a directory, even if it is not empty """
    try:
      shutil.rmtree(path)
    except OSError as e:
      print("Error: %s : %s" % (path, e.strerror))

  def showInformations(self):
    """ give an overview """
    with open(self.infoFile, 'r', encoding="utf-8") as f:
      lines = f.readlines()
    for line in lines:
      console.print(line.replace('\n', ''))

  def DBSetup(self):
    """ check if DB exists, or create it """
    if os.path.exists(self.dbPath) is False:
      sql_azure = """CREATE TABLE "azure" (
                "id"  INTEGER,
                "vorname"  STRING(100) NOT NULL,
                "nachname"  STRING(100) NOT NULL,
                "email"  STRING(255) NOT NULL,
                "licenses"  STRING(255) NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
              )"""
      sql_dates = """CREATE TABLE "dates" (
                "id"  INTEGER,
                "name"  STRING(20) NOT NULL,
                "date"  INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
              )"""
      sql_sokrates = """CREATE TABLE "sokrates" (
                "id"  INTEGER,
                "vorname"  STRING(100),
                "nachname"  STRING(100),
                PRIMARY KEY("id" AUTOINCREMENT)
              )"""
      self.db = Database(self.dbPath, self.cryptor, self.encrypt)
      self.db.query(sql_azure)
      self.db.query(sql_dates)
      self.db.query(sql_sokrates)
      self.db.close()
    else:
      # just connect to DB
      self.db = Database(self.dbPath, self.cryptor, self.encrypt)

  def createEmptyConfigFile(self):
    """ will create an Empty Config File """
    """ With O365 module
        data = dict(
            app=dict(
                title='MyApp',
            ),
            azure=dict(
                client_id='xxxx',
                client_secret='xxx',
                tenant_id='xxx',
            )
        )
        """
    data = dict(
        o365=dict(
            username='xxxx',
            password='xxx',
            encrypt=1,
        )
    )
    with open(self.configFile, 'w', encoding="utf-8") as f:
      yaml.dump(data, f, sort_keys=False, default_flow_style=False)

  def createEmptyVipFile(self):
    """ will create an Empty Vip File """
    data = {"vips": ['Hans Moser', 'Sepp Moser']}
    with open(self.vipFile, 'w', encoding="utf-8") as f:
      yaml.dump(data, f, sort_keys=False, default_flow_style=False)

  def load_yml(self):
    """ Load the yaml file config.yaml """
    if os.path.exists(self.configFile) is False:
      self.createEmptyConfigFile()
      self.console.print("\n[error]New config.yml File created ...[/]")
      self.console.print("[error]Please edit config/config.yml as needed ...[/]")
      self.console.print("[error]Use O365Admin.py to encrypt your password ...[/]")
      sys.exit(-1)
    with open(self.configFile, 'rt', encoding="utf-8") as f:
      yml = yaml.safe_load(f.read())
    return yml

  def load_vips(self):
    with open(self.vipFile, 'rt', encoding="utf-8") as f:
      yml = yaml.safe_load(f.read())
    return yml

  def getLastDBUpdate(self):
    return self.db.getLastDBUpdate()

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

  def azureUpdate(self):
    """ Update Users from Azure DB """
    loader = Loader("Loading from Azure ... pls wait ... ",
                    "", 0.1).start()

    csvFilePath = os.path.join(self.filesDir, self.csvFilename)

    self.azure = AzurePS(self.config, self.scriptPath,
                         self.keyFile, csvFilePath, self.debug, self.debugPath)
    self.azure.start()
    # block until finished
    self.azure.getThread().join()
    loader.stop()

    # sind Fehler passiert?
    if self.azure.hasErrors():
      exit()

    console.print("[info]CSV File saved to %s[/]" % self.csvFilename)
    # Finished process CSV File -----------------------------------
    csv = CSVTool()
    accounts = csv.read(os.path.join(self.rootDir, csvFilePath))

    # Update Dates
    self.db.Update_Last_Update_Date('azure')
    self.db.Truncate('azure')
    # insert data
    self.db.Insert_Azure(accounts, self.vips)
    console.print("[info]%s Lehrer, %s Schüler, %s Specials in Datenbank übernommen[/]" % (
        self.db.countLehrer(), self.db.countStudents(), self.db.countVips()))

  def importSokrates(self, questions):
    """ Import Sokrates Liste """
    csvFiles = self.search_files_in_dir(self.filesDir, '.csv')
    # print(csvFiles)
    flist = []
    for f in csvFiles:
      flist.append(os.path.basename(f))
    a = questions.AskSokrates(flist)

    # check CSV Datei
    csvFile = os.path.join(self.filesDir, a)
    if (os.path.exists(csvFile) is True):
      csv = CSVTool()
      accounts = csv.readSokrates(csvFile)

      # Update Dates
      self.db.Update_Last_Update_Date('sokrates')
      self.db.Truncate('sokrates')

      # insert data
      self.db.Insert_Sokrates(accounts)
      console.print("[info]%s Datensätze in die Datenbank übernommen[/]" %
                    (self.db.countSokrates()))

  def sync(self):
    """ Azure und Sokrates abgleichen """
    azure = self.db.loadAzureTable()
    sokrates = self.db.loadSokratesTable()

    console.print("[info]Abgleich der Datensätze ...[/]")
    console.print("[info]Sokrates > Azure < VIP's[/]")

    compare = Compare(azure, sokrates, self.cryptor,
                      self.encrypt, self.vips)
    compare.start()
    # block until finished
    compare.getThread().join()

    delete = compare.getDelete()

    self.printTable(delete)
    # save it
    csv = CSVTool()
    path = os.path.join(self.filesDir, "deleteUsers.csv")
    csv.save(path, delete)
    console.print(
        "[info]Datensätze diegelöscht werden können liegen in ./files/deleteUsers.csv[/]")

  def printTable(self, data):
    table = Table(title="Users that may deleted")
    table.add_column("Nr", style="cyan", no_wrap=True)
    table.add_column("Vorname", style="magenta")
    table.add_column("Nachname", style="green")

    i = 1
    for item in data:
      table.add_row(str(i), str(item.vorname), str(item.nachname))
      i += 1

    console.print(table)


def start():
  debug = True

  o365 = O365(debug)
  lastdates = []
  lastdates.append(o365.db.getLastDBUpdate('azure'))
  lastdates.append(o365.db.getLastDBUpdate('sokrates'))

  questions = Questions()

  if debug is False:
    a = questions.MainMenue(lastdates)

  if debug is True:
    console.print("[info]DEBUGGING :::[/]")
    console.print("[info]Sync Data O365 <> Local DB[/]")
    a = 'sync'

  if a == 'getazure':
    o365.azureUpdate()

  if a == 'info':
    o365.showInformations()

  if a == 'sokrates':
    o365.importSokrates(questions)

  if a == 'sync':
    o365.sync()

  if a == 'encrypt':
    text = questions.Ask("Klartext: ")

    chiper = o365.cryptor.encrypt(text)
    console.print("\n%s: %s" % (text, chiper.decode()))
    console.print("Use this hash in your config File for sensible data, e.g. passwords")

  console.print("\n[error]Beachte den Datenschutz![/]")
  console.print("[warning]Lösche alle CSV Daten aus dem Verzeichnis ./files ...[/]")


if __name__ == "__main__":
  start()
