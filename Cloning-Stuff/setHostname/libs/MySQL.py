import uuid
import re
import mysql.connector


class MySQL:
    """ load MAC Adress and get Hostname from MySQL DB """

    def __init__(self, config):
        self.config = config
        self.connect()
        
        
    def connect(self):
        mydb = mysql.connector.connect(
          host=self.config['server'],
          user=self.config['user'],
          password=self.config['password']
        )
        
        print(mydb) 

    def getHostData(self):
        self.getMacAdresses()

    def getMacAdresses(self):
        """ get MAC Adresses of eths """
        print(uuid.getnode())

        print("The MAC address in expressed in formatted and less complex way : ", end="")
        print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
