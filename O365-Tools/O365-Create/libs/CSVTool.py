import os
import pandas
from libs.UserObj import UserObj
import logging
from libs.MyConsole import MyConsole


class CSVTool():
  """ Read / Write CSV Files with pandas """
  userList = []

  def __init__(self):
    self.logger = logging.getLogger('Azure')
    self.console = MyConsole()

  def getUsers(self):
    """ return all Users from CSV File """
    return self.userList

  def read(self, filename):
    """ Read a CSV file """
    self.userList.clear()

    if os.path.exists(filename) is True:
      try:
        df = pandas.read_csv(filename)

        for index, row in df.iterrows():  # noqa
          user = UserObj()

          user.vorname = str(row['GivenName']).strip()
          user.nachname = str(row['Surname']).strip()
          user.displayName = str(row['DisplayName']).strip()
          user.mail = str(row['Mail']).strip()
          user.licenses = str(row['AzureADUserLicenseDetail']).strip()

          self.userList.append(user)
      except Exception:
        self.logger.error("Parsing csv File Error, is the seperator ',' ?")
        exit()
    else:
      self.console.error("File ./%s not found! - exit -" % filename)
    return self.userList

  def readSokrates(self, filename):
    """ Read a CSV file """
    self.userList.clear()

    if os.path.exists(filename) is True:
      try:
        df = pandas.read_csv(filename, sep=';')

        for index, row in df.iterrows():  # noqa
          user = UserSokrates()
          user.vorname = str(row['Vorname']).strip()
          user.nachname = str(row['Familienname']).strip()

          self.userList.append(user)
      except Exception:
        self.console.error("Parsing csv File Error, is the seperator ';' ?")
        exit()
    else:
      self.logger.error("File ./%s not found! - exit -" % filename)
    return self.userList

  def write(self, filename, data):
    """ Write data to a CSV File """
    df = pandas.read_csv('hrdata.csv',
                         index_col='Employee',
                         parse_dates=['Hired'],
                         header=0,
                         names=['Employee', 'Hired', 'Salary', 'Sick Days'])
    df.to_csv('hrdata_modified.csv')

  def save(self, filename, data):
    """ Write data to a CSV File """
    df = pandas.DataFrame([vars(c) for c in data])
    df.to_csv(filename, sep=";")
