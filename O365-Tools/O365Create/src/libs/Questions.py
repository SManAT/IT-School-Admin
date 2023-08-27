import questionary
from questionary.prompts.common import Separator


class Questions():

  dict = {
      'Q1': "AD mit Datenbank synchronisieren einlesen ...",
      'Q2': "Vorlagen Datei für Schüler öffnen ...",
      'Q3': "Schülerliste von CSV Datei laden ...",
      'Q4': "AD mit neuen Schülern Synchronisieren ...",
  }

  def __init__(self):
    pass

  def MainMenue(self):
    print("\nADUserAdmin.py, (c) Mag. Stefan Hagmann 2023")
    print("------------------------------------------\n")

    a = questionary.select(
        "Was soll ich tun?",
        choices=[
            self.dict['Q1'],
            self.dict['Q3'],
            self.dict['Q4'],
            Separator(),
            self.dict['Q2'],
        ]
    ).ask()

    if a == self.dict['Q1']:
      return "adimport"

    if a == self.dict['Q2']:
      return "vorlage"

    if a == self.dict['Q3']:
      return "load"

    if a == self.dict['Q3']:
      return "sync"
