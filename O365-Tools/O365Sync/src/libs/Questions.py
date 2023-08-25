import questionary
from questionary.prompts.common import Separator
from questionary import Style


class Questions():

  dict = {
      'Q1': "O365 Benutzer von Azure laden (kann etwas dauern...)",
      'Q2': "Hash erstellen ...",
      'Q3': "Informationen anzeigen ...",
      'Q4': "Sokrates Liste laden ...",
      'Q5': "Synchronisieren!"
  }
  custom_style_fancy = Style([
      ('qmark', 'fg:#00ff00 bold'),       # token in front of the question
      ('question', 'fg:#c0c0c0 bold'),               # question text
      ('answer', 'fg:#c0c0c0 bold'),      # submitted answer text behind the question
      ('pointer', 'fg:#00ff00 bold'),     # pointer used in select and checkbox prompts
      ('highlighted', 'fg:#00ff00 bold'),  # pointed-at choice in select and checkbox prompts
      ('selected', 'fg:#c0c0c0'),         # style for a selected item of a checkbox
      ('separator', 'fg:#c0c0c0'),        # separator in lists
      ('instruction', 'fg:#c0c0c0'),      # user instructions for select, rawselect, checkbox
      ('text', 'fg:#c0c0c0'),             # plain text
      ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
  ])

  def __init__(self):
    pass

  def Ask(self, question):
    return questionary.text("Klartext: ", style=self.custom_style_fancy).ask()

  def MainMenue(self, lastupdates):
    print("\nO365Sync.py, (c) Mag. Stefan Hagmann 2022")
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
        ],
        style=self.custom_style_fancy
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
