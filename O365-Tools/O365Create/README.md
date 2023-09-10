Mit diesem Tool werden O365 Account für Schülern angelegt.
Bitte in der Datei `config.yaml` die entsprechende Domain anpassen!

1. Die Schüler Accounts werden aus Sokrates via CSV Datei importiert.
   Auswertungen > Dynamische Suche > 100 Aktive Schüler > Exportieren als CSV
   Die Datei in das Verzeichnis files/ des Tools legen
2. Starte das Tool

   ```ps
   python src/O365Create.py
   ```

   Es werden die Vor- und Nachnamen aus der CSV Datei verwendet, um eine
   CSV Datei für den Massenimport in O365 erzeugt (`./files/O365-Import-File.csv`).
   Eine entsprechende Vorlagendatei kann man im Programm herunterladen.

3. O365 sendet eine Email mit allen Zugangsdaten zu. Den Text dieser Email wird
   in die Datei `./files/EmailZugangsdaten.txt` kopiert. Aus dem Email Text werden die zugesandeten Zugangsdaten extrahiert, und alle Daten in einer CSV Datei `./files/O365-CreatedUsers-Finished.csv` exportiert.

4. Mit dieser CSV Datei kann man dann einen Serienbrief für die Schüler erstellen lassen.
