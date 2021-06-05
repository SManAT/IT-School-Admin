import yaml
import os
from pathlib import Path
from libs.CmdRunner import CmdRunner
from datetime import date, datetime
import sys
import fnmatch
import re
from User import User


class MySQLBackup():
    """ Mysql Backup """

    prefix = "mysql-backup-"
    debug = False

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')

        self.config = self.load_yml()
        versions = self.config['misc']['versions']

        info = ("MySQLBackup\n"
                "(c) Mag. Stefan Hagmann 2021\n"
                "this tool is creating mysqldumps of all MySQL databases\n"
                "  - will keep last %s Versions of Backups\n"
                "-------------------------------------------------------\n" % versions)
        print(info)

        try:
            # ensure BackupPath exists
            self.checkBackupPath()
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
        if part1 == './' or part2 == '../':
            # relative
            path = os.path.join(self.rootDir, path)
        if os.path.isdir(path) is False:
            os.makedirs(path)

        path = re.sub('\.\/', '', path)
        path = re.sub('\.\.\/', '', path)
        self.backup_path = path

        # create dump-YYYY-MM-DD directory
        today = date.today()

        self.thisbackup_path = "%s%s" % (
            self.prefix, today.strftime("%Y-%m-%d"))

        path = os.path.join(path, self.thisbackup_path)
        if os.path.isdir(path) is False:
            os.makedirs(path)
        else:
            if self.debug is False:
                print("Das Backup %s gibt es bereits" % path)
                print("-exit-")
                sys.exit()

    def backupDB(self):
        """ Backup all Databases in a Directory with Logrotate """
        runner = CmdRunner()
        cmd = "mysql --defaults-extra-file=mysql.cnf -e 'show databases' -s --skip-column-names"
        runner.runCmd(cmd)
        errors = runner.getStderr()
        if errors:
            print(errors)
        databases = runner.getLines()

        path = os.path.join(self.backup_path, self.thisbackup_path)

        unwanted_db = {"sys", "information_schema",
                       "mysql", "performance_schema"}
        databases = [ele for ele in databases if ele not in unwanted_db]
        for db in databases:
            if len(db.strip()) > 0:
                cmd = "mysqldump --defaults-extra-file=mysql.cnf --single-transaction %s > %s/%s.sql" % (
                    db, path, db)
                # print("%s\n" % cmd)
                if self.debug is False:
                    print("Backup DB: %s" % db)
                    os.system(cmd)

        if self.debug is False:
            print("-done-\n")

        self.backupUsers()
        self.createTAR()

    def backupUsers(self):
        """ backup Users and Privileges to a yaml file """
        self.Users = []

        runner = CmdRunner()
        cmd = "mysql --defaults-extra-file=mysql.cnf -e 'SELECT host,user,authentication_string FROM mysql.user;'"
        runner.runCmd(cmd)
        errors = runner.getStderr()
        if errors:
            print(errors)
        userdata = runner.getLines()
        # remove first line
        userdata.pop(0)

        for line in userdata:
            if line:
                parts = line.split()
                username = parts[1]
                if username not in ["root", "debian-sys-maint", "mysql.sys", "mysql.session"]:
                    u = User()
                    u.set_hosts(parts[0])
                    u.set_username(parts[1])
                    u.set_pwd(parts[2])

                    self.Users.append(u)

        # now get Privileges
        for u in self.Users:
            # all hosts
            cmd = "mysql --defaults-extra-file=mysql.cnf -e \"SHOW GRANTS FOR '%s'@'%s';\"" % (
                u.get_username(), "%")
            runner.runCmd(cmd)
            errors = runner.getStderr()
            userdata = runner.getLines()
            # remove first element, only info
            userdata.pop(0)

            for line in userdata:
                if "error" not in line.lower():
                    if len(line) > 0:
                        u.add_privilege(line)

            # localhost
            cmd = "mysql --defaults-extra-file=mysql.cnf -e \"SHOW GRANTS FOR '%s'@'localhost';\"" % (
                u.get_username())
            runner.runCmd(cmd)
            errors = runner.getStderr()
            userdata = runner.getLines()
            # remove first element, only info
            userdata.pop(0)

            for line in userdata:
                if "error" not in line.lower():
                    if len(line) > 0:
                        u.add_privilege(line)

        # create yAMl File
        dict_file = {}
        for u in self.Users:
            data = {}
            data['privs'] = u.get_privileges()
            data['username'] = u.get_username()
            data['hosts'] = u.get_hosts()
            data['pwd'] = u.get_pwd()

            dict_file[u.get_username()] = data

        path = os.path.join(
            self.backup_path, self.thisbackup_path, 'users.yaml')
        with open(path, 'w') as file:
            documents = yaml.dump(dict_file, file)  # noqa

    def createTAR(self):
        """ create Tarballs """
        if self.debug is False:
            print("Creating Tarball ...")

        tarball = "%s.tar.bzip2" % os.path.join(
            self.backup_path, self.thisbackup_path)
        cd_cmd = "cd %s" % self.backup_path
        cmd = "tar cjf %s --acls --xattrs --warning=no-file-ignored %s" % (
            tarball, self.thisbackup_path)

        if self.debug is False:
            # tar it
            os.system("%s && %s > /dev/null 2>&1" % (cd_cmd, cmd))
            # delete Backup Dir
            cmd = "rm -r %s" % os.path.join(self.backup_path,
                                            self.thisbackup_path)
            os.system(cmd)
            print("-done-\n")

    def cleanUpBackups(self):
        """Rotate Backups to keep #versions"""
        print("Cleaning in progress")
        data = []
        # search backups
        files = self.search_files(self.backup_path, "*.tar.bzip2")
        for f in files:
            # extract dates
            p = re.compile("\d{4}-\d{1,2}-\d{1,2}")
            erg = p.findall(f)
            if erg:
                data.append([f, erg[0]])
        # keep versions
        versions = self.config['misc']['versions']

        # sort with key, take the date as key
        data.sort(key=lambda the_file: the_file[1])

        while(len(data) >= int(versions) + 1):
            # delete oldest backup Versions
            cmd = "rm %s" % data[0][0]
            if self.debug is False:
                os.system(cmd)
                # remove first element
                data.pop(0)

        if self.debug is False:
            print("-done-\n")

    def search_files(self, directory, pattern):
        """ search for pattern in directory recursive """
        data = []
        for dirpath, dirnames, files in os.walk(directory):  # noqa
            for f in fnmatch.filter(files, pattern):
                data.append(os.path.join(dirpath, f))
        return data


if __name__ == "__main__":
    start_time = datetime.now()

    backup = MySQLBackup()
    backup.backupDB()
    backup.cleanUpBackups()

    time_elapsed = datetime.now() - start_time
    print("MySQL Backup finished ...")
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
