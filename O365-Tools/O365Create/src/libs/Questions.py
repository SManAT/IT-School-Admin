import questionary
from questionary.prompts.common import Separator


class Questions():

  dict = {
      'Q2': "Vorlagen Datei für Schüler öffnen ...",
      'Q3': "Schülerliste von CSV Datei laden ...",
      'Q4': "Erstelle Serienbrief Datei (Benutzer und Passwörter) ...",
      'Q5': "Informationen anzeigen ...",
  }

  def __init__(self):
    pass

  def MainMenue(self):
    print("\nO365Create.py, (c) Mag. Stefan Hagmann 2023")
    print("------------------------------------------\n")

    a = questionary.select(
        "Was soll ich tun?",
        choices=[
            self.dict['Q3'],
            self.dict['Q4'],
            Separator(),
            self.dict['Q2'],
            self.dict['Q5'],
        ]
    ).ask()

    if a == self.dict['Q2']:
      return "vorlage"

    if a == self.dict['Q3']:
      return "import"

    if a == self.dict['Q4']:
      return "serienbrief"

    if a == self.dict['Q5']:
      return "info"
