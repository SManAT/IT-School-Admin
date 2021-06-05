import yaml
import os
from pathlib import Path
from libs.CmdRunner import CmdRunner
from datetime import date, datetime
from time import sleep
import sys
import fnmatch
import re
import timeit
import time


class MySQLBackup():
    
    prefix = "mysql-backup-"
    debug = True

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
        
        self.config = self.load_yml()    
        try:
            # ensure BackupPath exists
            self.checkBackupPath()
        except Exception as ex:
            print(ex)
        
        info = ("MySQLRestore\n"
        "(c) Mag. Stefan Hagmann 2021\n"
        "this tool is restoring MySQL databases, from MySQLBackup Tarballs\n"
        "restoring from %s\n"
        "------------------------------------------------------------------\n" % self.backup_path) 
        print(info)
        

    def load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml

    def checkBackupPath(self):
        """ check if BackupPathexists """
        path = self.config['misc']['backupPath']
        # relative path?
        part1 = path[:2]
        part2 = path[:3]
        if './' == part1 or '../' == part2:
            # relative
            path = os.path.join(self.rootDir, path)  
        
        path = re.sub('\.\/', '', path)
        path = re.sub('\.\.\/', '', path)     
 
        self.backup_path = path
           
    def search_files(self, directory, pattern):
        """ search for pattern in directory recursive """
        data = []
        for dirpath, dirnames, files in os.walk(directory):
            for f in fnmatch.filter(files, pattern):
                data.append(os.path.join(dirpath, f))
        return data
    
    def repeat_question(self, max):
        """ ask until it meets the requirements """
        valid = False
        while valid is False:
            valid = True
            try:
                question="Select Tarball Number: "
                number=int(input(question).strip())
                
                if number not in range(1, max+1):
                    print("\nPlease select a valid Backup (1..%s)!" % max)
                    valid = False
            except ValueError:
                print("\nThat is not a number!")
                valid = False
        return number
    
    def restoreDB(self):
        """ will restore the DB """
        files = self.search_files(self.backup_path, "*.tar.bzip2")
        data=[]
        for f in files:
            # extract dates
            p = re.compile("\d{4}-\d{1,2}-\d{1,2}")
            erg = p.findall(f) 
            if erg:
                data.append([f, erg[0]])
        # sort with key, take the date as key
        data.sort(key=lambda the_file: the_file[1])
        
        print("Which backup schould be restored?")
        tars = []
        index = 1
        for f in data:
            print("(%s) %s" % (index, os.path.basename(f[0])))
            tars.append([index, f[0]])
            index+=1
        if self.debug is False:
            number = self.repeat_question(index-1)
        
        if self.debug is True:
            backup = tars[0][1]
        else:
            backup = tars[int(number-1)][1]
            
        self.startBackup(backup)

        
    def startBackup(self, tarball):
        """ will start the restoring of the backup """
        print("\nStart restoring of backup %s" % os.path.basename(tarball))
        print("Existing datbases will be overwritten!")
        question="Are you sure (y): "
        
        if self.debug is True:
            self.doit(tarball)

        if self.debug is False:
            answer=input(question).strip()
            if answer.lower() in "y":
                self.doit(tarball)
            else:
                print("-exit -")
            
    def doit(self, tarball):
        """ really restore data """
        
        #create full path
        fullpath = re.sub('\.tar\.bzip2', '', tarball)
        print(fullpath)
        
        # untar Backup
        print("\nExtracting tarball ... in progress ...")
        
        if os.path.isdir(fullpath) is False:
            cmd = "tar xfj %s" % tarball
            os.system(cmd)
            print("done ...")
        else:
            print("Tarball is already extracted ... skipping ...")
        
        files = self.search_files(fullpath, "*.sql")
        for f in files:
            print("Importing %s ..." % os.path.basename(f))
            filename, file_extension = os.path.splitext(os.path.basename(f))
            dbname = filename
            
            # first drop DB
            cmd = "DROP DATABASE IF EXISTS %s;" % dbname
            cmd = "mysql --defaults-extra-file=mysql.cnf -e '%s'" % cmd
            os.system(cmd)

            # create DB new
            cmd = "CREATE DATABASE %s;" % dbname
            cmd = "mysql --defaults-extra-file=mysql.cnf -e '%s'" % cmd
            os.system(cmd)
            
            sleep(0.5)
            # now import new one
            cmd = "mysql --defaults-extra-file=mysql.cnf %s < %s" % (dbname, f)
            os.system(cmd)
        
        
        
            
        

if __name__ == "__main__":
    start_time = datetime.now() 
    
    backup = MySQLBackup()    
    backup.restoreDB()
    
    time_elapsed = datetime.now() - start_time 
    print("\nMySQL Restore finished ...")
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))

    
    

"""
--single-transaction uses a consistent read and guarantees that data seen by mysqldump does not change.

IMPORT
mysql -u root -p -e'flush privileges;'
"""
