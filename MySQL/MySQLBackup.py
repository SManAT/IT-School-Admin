import yaml
import os
from pathlib import Path
from libs.CmdRunner import CmdRunner
from datetime import date
import sys


class MySQLBackup():
    
    prefix = "mysql-backup-"

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
                
        info = ("MySQLBackup\n"
        "(c) Mag. Stefan Hagmann 2021\n"
        "this tool is creating mysqldumps of all databases\n"
        "=================================================\n") 
        print(info)

        try:
            self.config = self.load_yml()
            # ensure BackupPath exists
            self.checkBackupPath()
            self.backupDB()
        except Exception as ex:
            print(ex)

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
        if os.path.isdir(path) is False:
            os.makedirs(path)
            
        # create dump-YYYY-MM-DD directory
        today = date.today()
        path = os.path.join(path, "%s%s" % (self.prefix, today.strftime("%Y-%m-%d")))
        if os.path.isdir(path) is False:
            os.makedirs(path)
        else:
            print("Das Backup %s gibt es bereits" % path)
            print("-exit-")
            sys.exit()
        
        self.backup_path = path

    def backupDB(self):
        """ Backup all Databases in a Directory with Logrotate """
        runner = CmdRunner()  
        cmd = "mysql --defaults-extra-file=mysqldump.cnf -e 'show databases' -s --skip-column-names"
        runner.runCmd(cmd)
        errors = runner.getStderr()
        if errors:
            print(errors)
        databases = runner.getLines()
        
        unwanted_db = {"sys", "information_schema"}
        databases = [ele for ele in databases if ele not in unwanted_db]
        for db in databases:
            if db.strip() is not "":
                print("Backup DB: %s" % db)
                cmd = "mysqldump --defaults-extra-file=mysqldump.cnf --single-transaction %s > %s/%s.sql" % (db, self.backup_path, db)
                # print("%s\n" % cmd)
                os.system(cmd)
                
        print("-done-")
            
            
            


if __name__ == "__main__":
    backup = MySQLBackup()
    backup.backupDB()

"""
--single-transaction uses a consistent read and guarantees that data seen by mysqldump does not change.

IMPORT
mysql -u root -p -e'flush privileges;'
"""
