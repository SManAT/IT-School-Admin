import os

import pysftp


class SFTP:

    def __init__(self, rootDir, hostname, username, passwd):
        self.hostname = hostname
        self.username = username
        self.passwd = passwd
        self.sftp = None
        
        self.knownhosts = os.path.join(rootDir, ".knownhosts")
        self.sftplog = os.path.join(rootDir, "sftp_log.txt")
    
        # Connection
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            cnopts.log = self.sftplog
            
            self.sftp = pysftp.Connection(
              self.hostname,
              username=self.username,
              password=self.passwd,
              cnopts=cnopts
            )
        except Exception as ex:
            print(ex)
            print(f"Can't connect to SFTP Server {self.hostname} ... exit")
            exit(-1)
      
    def close(self):
        try:
            self.sftp.close()
        except:
            pass
        
    def get(self, source, target):
        """ 
        load wallpaper from directory
        :param source: Path on SFTP Server
        :param target: Path on local OS
        :param filename: filename to copy 
        """
        #  get(remotepath, localpath=None, callback=None, preserve_mtime=False)
        self.sftp.get(source, target, preserve_mtime=True)

    def load_wallpapapers(self, path):
        self.sftp.chdir(path)
        data = self.sftp.listdir()
        return data

