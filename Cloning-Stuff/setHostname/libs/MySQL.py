import uuid
import re
import mysql.connector


class MySQL:
    """ load MAC Adress and get Hostname from MySQL DB """

    def __init__(self, config):
        self.config = config
        self.con = None
        
        
        
    def connect(self):
        if self.con is None:
            self.con = mysql.connector.connect(
              host=self.config['server'],
              user=self.config['user'],
              password=self.config['password']
            )
            
    def close(self):
        if self.con is not None:
            self.con.close()
    
    def getHostData(self):
        self.getMacAdresses()

    def TEST_getMacAdresses(self):
        """ get MAC Adresses of eths """
        print(uuid.getnode())

        print("The MAC address in expressed in formatted and less complex way : ", end="")
        print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
