# https://realpython.com/python-csv/#parsing-csv-files-with-the-pandas-library

import pandas


class CSVTool():
  """ Read / Write CSV Files with pandas """

  def __init__():
    pass

  def read(filename):
    """ Read a CSV file """
    df = pandas.read_csv('hrdata.csv')
    print(df)
    print(type(df['Hire Date'][0]))

  def write(filename, data):
    """ Write data to a CSV File """
    df = pandas.read_csv('hrdata.csv',
                         index_col='Employee',
                         parse_dates=['Hired'],
                         header=0,
                         names=['Employee', 'Hired', 'Salary', 'Sick Days'])
    df.to_csv('hrdata_modified.csv')
