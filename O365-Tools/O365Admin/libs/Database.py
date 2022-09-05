import sqlite3
from sqlite3 import Error
import datetime
from rich.progress import Progress
from libs.UserObj import UserObj
from libs.UserSokrates import UserSokrates


class Database():
    """ a class to manage SQLite Database """

    def __init__(self, dbPath):
        self.dbPath = dbPath
        self.connect()

    def connect(self):
        """ connect to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.dbPath)
            # Datensatz-Cursor erzeugen
            self.cursor = self.conn.cursor()
        except Error as e:
          print("SQlite: %s" % sqlite3.version)
          print(e)

    def close(self):
        """ close an open SQLite Connection """
        if self.conn:
            self.conn.close()

    def query(self, sql):
      """ execute a sql query """
      if self.conn:
        self.cursor.execute(sql)
        # sofortiges Ausführen gegen die db
        self.conn.commit()

# QUERYS =================================================================================
    def Update_Last_Update_Date(self, table):
        """ Azure DB was updated """
        # search for entry
        self.connect()
        cmd = "SELECT * FROM dates WHERE name='%s' LIMIT 1" % table
        result = self.cursor.execute(cmd)
        data = result.fetchone()
        self.close()

        self.connect()
        # neu anlegen
        today = datetime.datetime.now()
        now = today.strftime("%Y-%m-%d %H:%M:%S")
        if data is None:
            self.cursor.execute("INSERT INTO dates ('id','name','date') VALUES (?,?,?)", (None, table, now))
        else:
            # update
            theid = data[0]
            self.cursor.execute("UPDATE dates SET name=?, date=? WHERE id=?", (table, now, theid))
        self.conn.commit()
        self.close()

    def Truncate(self, table):
        """ empty azure users """
        self.connect()
        cmd = "DELETE FROM %s" % table
        self.cursor.execute(cmd)
        self.conn.commit()
        self.close()

    def Insert_Azure(self, accounts, vips):
        """ insert User Accounts Object into DB """
        # nicht so oft den Progressbar updaten
        delta = 10
        index = 0

        with Progress() as progress:
          task = progress.add_task("[green]Updating Database...", total=len(accounts))

          self.connect()
          for account in accounts:
            licence = account.getLicenses(vips)
            if licence is not None:
              data = (None,
                      account.getVorname(),
                      account.getNachname(),
                      account.getMail(),
                      licence,
                      )
              self.cursor.execute("INSERT INTO azure ('id','vorname','nachname', 'email', 'licenses') VALUES (?,?,?,?,?)", data)
              self.conn.commit()

            index += 1
            if index == delta:
              progress.update(task, advance=delta)
              index = 0
        self.close()

    def Insert_Sokrates(self, accounts):
        """ insert User Accounts Object into DB """
        # nicht so oft den Progressbar updaten
        delta = 10
        index = 0

        with Progress() as progress:
          task = progress.add_task("[green]Updating Database...", total=len(accounts))

          self.connect()
          for account in accounts:
            data = (None,
                    account.getVorname(),
                    account.getNachname(),
                    )
            self.cursor.execute("INSERT INTO sokrates ('id','vorname','nachname') VALUES (?,?,?)", data)
            self.conn.commit()

            index += 1
            if index == delta:
              progress.update(task, advance=delta)
              index = 0
        self.close()

    def countLehrer(self):
      self.connect()
      result = self.cursor.execute("SELECT COUNT(*) FROM azure WHERE licenses = 'L'")
      data = result.fetchone()
      self.close()
      return data[0]

    def countStudents(self):
      self.connect()
      result = self.cursor.execute("SELECT COUNT(*) FROM azure WHERE licenses = 'S'")
      data = result.fetchone()
      self.close()
      return data[0]

    def countVips(self):
      self.connect()
      result = self.cursor.execute("SELECT COUNT(*) FROM azure WHERE licenses = 'V'")
      data = result.fetchone()
      self.close()
      return data[0]

    def countSokrates(self):
      self.connect()
      result = self.cursor.execute("SELECT COUNT(*) FROM sokrates")
      data = result.fetchone()
      self.close()
      return data[0]

    def getLastDBUpdate(self, table):
      self.connect()
      cmd = "SELECT * FROM dates WHERE name='%s' LIMIT 1" % table
      result = self.cursor.execute(cmd)
      data = result.fetchone()
      self.close()

      if data is not None:
        dt_object = datetime.datetime.strptime(data[2], "%Y-%m-%d %H:%M:%S")
        return dt_object.strftime("%d.%m.%Y")
      else:
        return None

    def loadAzureTable(self):
      self.connect()
      cmd = "SELECT * FROM azure"
      result = self.cursor.execute(cmd)
      data = result.fetchall()
      self.close()

      erg = []
      for o in data:
        user = UserObj()
        user.vorname = o[1]
        user.nachname = o[2]
        user.mail = o[3]
        user.licenses = o[4]

        erg.append(user)
      return erg

    def loadSokratesTable(self):
      self.connect()
      cmd = "SELECT * FROM sokrates"
      result = self.cursor.execute(cmd)
      data = result.fetchall()
      self.close()

      erg = []
      for o in data:
        user = UserSokrates()
        user.vorname = o[1]
        user.nachname = o[2]

        erg.append(user)
      return erg
