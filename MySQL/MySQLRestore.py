import yaml
import os
from pathlib import Path
from datetime import datetime
from time import sleep
import fnmatch
import re
from User import User


class MySQLBackup():
    """ class to Backup MySQL """

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
        if part1 == './' or part2 == '../':
            # relative
            path = os.path.join(self.rootDir, path)

        path = re.sub('\.\/', '', path)  # noqa
        path = re.sub('\.\.\/', '', path)  # noqa

        self.backup_path = path

    def search_files(self, directory, pattern):
        """ search for pattern in directory recursive """
        data = []
        for dirpath, dirnames, files in os.walk(directory):  #noqa
            for f in fnmatch.filter(files, pattern):
                data.append(os.path.join(dirpath, f))
        return data

    def repeat_question(self, maxvalue):
        """ ask until it meets the requirements """
        valid = False
        while valid is False:
            valid = True
            try:
                question = "Select Tarball Number: "
                number = int(input(question).strip())

                if number not in range(1, maxvalue+1):
                    print("\nPlease select a valid Backup (1..%s)!" % max)
                    valid = False
            except ValueError:
                print("\nThat is not a number!")
                valid = False
        return number

    def restoreDB(self):
        """ will restore the DB """
        files = self.search_files(self.backup_path, "*.tar.bzip2")
        data = []
        for f in files:
            # extract dates
            p = re.compile("\d{4}-\d{1,2}-\d{1,2}")  # noqa
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
            index += 1
        if self.debug is False:
            number = self.repeat_question(index-1)

        if self.debug is True:
            backuptar = tars[0][1]
        else:
            backuptar = tars[int(number-1)][1]

        self.startBackup(backuptar)


    def startBackup(self, tarball):
        """ will start the restoring of the backup """
        print("\nStart restoring of backup %s" % os.path.basename(tarball))
        print("Existing datbases will be overwritten!")
        question = "Are you sure (y): "

        # without question
        if self.debug is True:
            self.doit(tarball)

        if self.debug is False:
            answer = input(question).strip()
            if answer.lower() in "y":
                self.doit(tarball)
            else:
                print("-exit -")
                
    def doMySQL(self, cmd):
        """ do a MysQL native command """
        cmd = "mysql --defaults-extra-file=mysql.cnf -e '%s'" % cmd
        os.system(cmd)

    def doit(self, tarball):
        """ really restore data """

        #create full path
        fullpath = re.sub('\.tar\.bzip2', '', tarball)  # noqa
        topath = Path(fullpath).parent.absolute()
        # untar Backup
        print("\nExtracting tarball ... in progress ...")

        if os.path.isdir(fullpath) is False:
            cmd = "tar xfj %s -C %s" % (tarball, topath)
            os.system(cmd)
            print("done ...")
        else:
            print("Tarball is already extracted ... skipping ...")

        files = self.search_files(fullpath, "*.sql")

        if self.debug is False:
            for f in files:
                print("Importing %s ..." % os.path.basename(f))
                filename, file_extension = os.path.splitext(os.path.basename(f))  #noqa
                dbname = filename

                # first drop DB
                self.doMySQL("DROP DATABASE IF EXISTS %s;" % dbname)

                # create DB new
                self.doMySQL("CREATE DATABASE %s;" % dbname)

                sleep(0.5)
                # now import new one
                cmd = "mysql --defaults-extra-file=mysql.cnf %s < %s" % (dbname, f)
                os.system(cmd)

        #change to InnoDB
        self.doMySQL("ALTER TABLE mysql.db ENGINE=InnoDB;")
        self.doMySQL("ALTER TABLE mysql.columns_priv ENGINE=InnoDB;")

        # restoring User Privileges
        # read yaml File
        path = os.path.join(fullpath, 'users.yaml')
        with open(path, 'rt') as f:
            users = yaml.safe_load(f.read())

        self.Users = []
        for block in users.values():
            u = User()

            for k, v in block.items():
                if k in "username":
                    u.set_username(v)
                if k in "hosts":
                    u.set_hosts(v)
                if k in "pwd":
                    u.set_pwd(v)

                if k in "privs":
                    u.set_privileges(v)
            self.Users.append(u)

        for u in self.Users:
            print("Creating User: %s" % u.get_username())

            mysql_upgrade -u root -p --force
mysqlcheck -u root -p --auto-repair --optimize --all-databases
            
            self.doMySQL("CREATE USER \"%s\"@\"%s\" IDENTIFIED BY \"%s\";" % (u.get_username(), u.get_hosts(), u.get_pwd()))

            self.doMySQL("ALTER USER \"%s\"@\"%s\" IDENTIFIED WITH mysql_native_password BY \"%s\";" % (u.get_username(), u.get_hosts(), u.get_pwd()))

            for p in u.get_privileges():
                self.doMySQL(p)
            
            self.doMySQL("FLUSH PRIVILEGES;")
            
                
        
            
        

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
