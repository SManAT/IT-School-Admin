import logging
import re
import sys
import time
import psutil


class Worker:
    """ Class to do all the Stuff """
    debug = True

    def __init__(self, config, rootDir, cryptor):
        self.logger = logging.getLogger('Worker')
        self.config = config
        self.rootDir = rootDir
        self.cryptor = cryptor
        
     


    def decrypt(self, encMessage):
        """ decrypt a String """
        return self.fernet.decrypt(str.encode(encMessage)).decode()
    
  
     
