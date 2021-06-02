import yaml
import os
from pathlib import Path
from libs.CmdRunner import CmdRunner
import inspect


class MySQLBackup():

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
                
        info = ("MySQLBackup\n"
        "(c) Mag. Stefan Hagmann 2021\n"
        "this tool is creating mysqldumps of all databases\n"
        "=================================================\n\n") 
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

    def backupDB(self):
        """ Backup all Databases in a Directory with Logrotate """
        runner = CmdRunner()  
        cmd = "mysql --defaults-extra-file=mysqldump.cnf -e 'show databases' -s --skip-column-names"
        runner.runCmd(cmd)
        errors = runner.getStderr()
        if errors:
            print(errors)
        databases = runner.getLines()
        for db in databases:
            print(db)


if __name__ == "__main__":
    backup = MySQLBackup()
    backup.backupDB()

"""
--single-transaction uses a consistent read and guarantees that data seen by mysqldump does not change.

Backup in single Files

for DB in $(mysql - u root - p mysqlmaster - e 'show databases' - s - -skip-column-names)
do
mysqldump $DB > "$DB.sql"
done
"""
