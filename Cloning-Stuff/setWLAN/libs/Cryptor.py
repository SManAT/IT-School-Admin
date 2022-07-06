import os
from cryptography.fernet import Fernet


class Cryptor:
    """ Class to encrypt/decrypt """
   

    def __init__(self, keyFile):
        self.keyFile = keyFile
        
        if (os.path.exists(self.keyFile) is False):
            print("There is no Key file to encrypt/decrypt -exit-")
            print("Path: %s" % self.keyFile)
            exit()
        # read Key File
        file = open(self.keyFile, 'rb')
        self.KEY = file.read()
        file.close()
        
        self.fernet = Fernet(self.KEY)
    
    def keyExists(self):
        return os.path.exists(self.keyFile)
        
    def createKeyFile(self):
        """ Create an encryption key """
        # Test if key.key is present
        if (os.path.exists(self.keyFile) is False):
            # create a key file
            key = Fernet.generate_key()
            file = open(self.keyFile, 'wb')
            file.write(key)
            file.close()
            print("KeyFile created in %s" % self.keyFile)

    def encrypt(self, estring):
        """ Encrypt this string """
        return self.fernet.encrypt(estring.encode())
  
    def decrypt(self, encMessage):
        """ decrypt a String """
        return self.fernet.decrypt(str.encode(encMessage)).decode()
    
