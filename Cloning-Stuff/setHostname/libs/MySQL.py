import uuid
import re
import mysql.connector
import logging


class MySQL:
    """ load MAC Adress and get Hostname from MySQL DB """

    def __init__(self, config):
        """
        config['server']
        config['user']
        config['password']
        """
        self.logger = logging.getLogger('MySQL')
        self.config = config
        self.con = None
        
    def connect(self):
        if self.con is None:           
            try:
                self.con = mysql.connector.connect(
                  host=self.config['server'],
                  user=self.config['user'],
                  password=self.config['password']
                )
            except Exception as e:
                print(e)
                exit()
            
    def close(self):
        if self.con is not None:
            self.con.close()
    
    def getHostName(self, sql, mac):
        self.connect()
        
        # replace __mac__ with mac adress
        sql = sql.replace('__mac__', mac)
        cursor = self.con.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        
        cursor.close() 
        self.close()
   
        erg = None
        # only return first hit
        for (hostname, mac) in data:
            erg = hostname
            break
        return erg
        

    def TEST_getMacAdresses(self):
        """ get MAC Adresses of eths """
        print(uuid.getnode())

        print("The MAC address in expressed in formatted and less complex way : ", end="")
        print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
