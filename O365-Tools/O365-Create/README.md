Mit diesem Tool werden O365 Account für die Ersten Klassen angelegt.
Das Tool funktioniert aber auch für alle anderen Account.

1. Die Schüler Accounts werden aus Sokrates via CSV Datei importiert.
   Auswertungen > Dynamische Suche > 100 Aktive Schüler > Exportieren als CSV
   Die Datei in das root Verzeichnis des Tools legen
      
2. Starte das Tool
   ```ps
   python O365-Create.py
   ```
   Es werden die Vor- und Nachnamen aus der CSV Datei verwendet, um eine
   CSV Datei für den Massenimport in O365 erzeugt.

3. O365 sendet eine Email mit allen Zugangsdaten zu. Den Text dieser Email wird
   in die Datei Email.txt kopiert.

4. Starte das Tool
   ```ps
   python O365-Create.py
   ```
   Aus dem Email Text werden die zugesandeten Zugangsdaten extrahiert, und alle Daten in
   einer CSV Datei **O365-Create-Users.csv** exportiert.

5. Mit dieser CSV Datei kann man dann einen Serienbrief für die Schüler erstellen lassen.