import questionary
from questionary.prompts.common import Separator


class Questions():

    dict = {
        'Q1': "Schülerliste von CSV Datei einlesen ...",
        'Q2': "Vorlagen Datei öffnen ...",
        'Q3': "Email von O365 einlesen ...",
    }

    def __init__(self):
        pass

    def MainMenue(self):
        print("\nO365Create.py, (c) Mag. Stefan Hagmann 2022")
        print("------------------------------------------\n")

        a = questionary.select(
            "Was soll ich tun?",
            choices=[
                self.dict['Q1'],
                self.dict['Q3'],
                Separator(),
                self.dict['Q2'],
            ]
        ).ask()

        if a == self.dict['Q1']:
            return "import"

        if a == self.dict['Q2']:
            return "vorlage"

        if a == self.dict['Q3']:
            return "email"
