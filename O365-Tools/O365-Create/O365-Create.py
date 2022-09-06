import yaml
import os
import atexit

from pathlib import Path
from libs.MyConsole import MyConsole
from libs.CSVTool import CSVTool
import questionary
from libs.Questions import Questions
from rich.table import Table
from rich.console import Console

# cross-plattform os.startfile
from startfile import startfile


class O365():

    # where to store O365 Users temorary
    csvFilename = "licencedUsers.csv"

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.filesPath = os.path.join(self.rootDir, 'files');

        self.console = MyConsole()

        # catch terminating Signal
        atexit.register(self.exit_handler)

    def exit_handler(self):
        """ do something on sys.exit() """
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
          #print(f"{child.name}")
          if pattern == '':
            data.append(os.path.join(directory, child.name))
          else:
            for p in pattern:
              if child.name.endswith(p):
                data.append(os.path.join(directory, child.name))
      return data
    
    def vorlage(self):
      """ Open Vorlage File """
      startfile(os.path.join(self.filesPath, "Vorlage.csv"))
      

    def importSokrates(self):
      """ Import Sokrates Liste """
      csvFiles = self.search_files_in_dir(self.filesPath, '.csv')
      print("Bitte Nur Schüler aufnehmen, die einen Account bekommen sollen.")
      print(csvFiles)
      flist = []
      for f in csvFiles:
        flist.append(os.path.basename(f))
      a = questionary.select(
          "Welche CSV Datei?",
          choices=flist,
      ).ask()
      

      # check CSV Datei
      csvFile = os.path.join(self.rootDir, a)
      if (os.path.exists(csvFile) is True):
        csv = CSVTool()
        accounts = csv.readSokrates(csvFile)
        
        print(accounts)
        exit()

        # Update Dates
        self.db.Update_Last_Update_Date('sokrates')
        self.db.Truncate('sokrates')

        # insert data
        self.db.Insert_Sokrates(accounts)
        self.console.info("%s SchÃ¼ler in Datenbank Ã¼bernommen" % (self.db.countSokrates()))

    
    def printTable(self, data):
      table = Table(title="Users that may deleted")
      table.add_column("Nr", style="cyan", no_wrap=True)
      table.add_column("Vorname", style="magenta")
      table.add_column("Nachname", style="green")

      i = 1
      for item in data:
        table.add_row(str(i), str(item.vorname), str(item.nachname))
        i += 1

      console = Console()
      console.print(table)
      
    

    





def start():
  debug = True

  o365 = O365()
  questions = Questions()
  a = questions.MainMenue()
  
  if a == 'import':
    o365.importSokrates()
    
  if a == 'vorlage':
    o365.vorlage()

if __name__ == "__main__":
    start()
