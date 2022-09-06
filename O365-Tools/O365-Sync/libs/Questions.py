import questionary
from questionary.prompts.common import Separator


class Questions():

    dict = {
      'Q1': "O365 Benutzer von Azure laden (kann etwas dauern...)",
      'Q2': "Hash erstellen ...",
      'Q3': "Informationen anzeigen ...",
      'Q4': "Sokrates Liste laden ...",
      'Q5': "Synchronisieren!"
    }

    def __init__(self):
      pass

    def MainMenue(self, lastupdates):
      print("\nO365-Sync.py, (c) Mag. Stefan Hagmann 2022")
      msg = "Letztes Azure Update:"
      print(f"{msg :<25} {lastupdates[0]}")
      msg = "Letztes Sokrates Update:"
      print(f"{msg :<25} {lastupdates[1]}")
      print("------------------------------------------\n")

      a = questionary.select(
        "Was soll ich tun?",
        choices=[
          self.dict['Q5'],
          Separator(),
          self.dict['Q4'],
          self.dict['Q1'],
          Separator(),
          self.dict['Q2'],
          self.dict['Q3']
        ]
      ).ask()

      if a == self.dict['Q1']:
        return "getazure"
      if a == self.dict['Q2']:
        return "encrypt"
      if a == self.dict['Q3']:
        return "info"
      if a == self.dict['Q4']:
        return "sokrates"
      if a == self.dict['Q5']:
        return "sync"
