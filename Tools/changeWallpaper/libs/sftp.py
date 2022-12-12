import pysftp
import os

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
      pysftp.CnOpts.log = self.sftplog
      cnopts = pysftp.CnOpts(knownhosts=self.knownhosts)
      self.sftp = pysftp.Connection(
          self.hostname, 
          username=self.username, 
          password=self.passwd,
          cnopts=cnopts
        )
    except Exception as ex:
      print(f"Can't connect to SFTP Server {self.hostname} ...")
      print(ex)
      exit(-1)
      
  def close(self):
    try:
      self.sftp.close()
    except:
      pass
      

  def test(self):
    pass
    """
        with sftp.cd('/allcode'):           # temporarily chdir to allcode
            sftp.put('/pycode/filename')  	# upload file to allcode/pycode on remote
            sftp.get('remote_file')         # get a remote file
    """