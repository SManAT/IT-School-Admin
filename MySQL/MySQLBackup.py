#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) Mag. Stefan Hagmann 2021

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import yaml
import os
from pathlib import Path
from datetime import date, datetime
import sys
import fnmatch
import re

from libs.User import User
from libs.CmdRunner import CmdRunner


class MySQLBackup():
    """ Mysql Backup """

    prefix = "mysql-backup-"
    debug = False

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
        self.extrafile = os.path.join(self.rootDir, 'mysql.cnf')

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

        path = re.sub('\.\/', '', path)  # noqa
        path = re.sub('\.\.\/', '', path)  # noqa
        self.backup_path = path

        # create dump-YYYY-MM-DD directory
        today = date.today()

        self.thisbackup_path = "%s%s" % (
            self.prefix, today.strftime("%Y-%m-%d"))

        # is there a today backup?
        self.tarball = "%s.tar.bzip2" % os.path.join(
            self.backup_path, self.thisbackup_path)
        if os.path.isfile(self.tarball) is True:
            self.exitScript(self.tarball)

        path = os.path.join(path, self.thisbackup_path)
        if os.path.isdir(path) is False:
            os.makedirs(path)
        else:
            self.exitScript(path)

    def exitScript(self, value):
        """ stop it """
        if self.debug is False:
            print("Das Backup %s gibt es bereits" % value)
            print("-exit-")
            sys.exit()

    def backupDB(self):
        """ Backup all Databases in a Directory with Logrotate """
        runner = CmdRunner()
        cmd = "mysql --defaults-extra-file=%s -e 'show databases' -s --skip-column-names" % self.extrafile
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
                cmd = "mysqldump --defaults-extra-file=%s --single-transaction %s > %s/%s.sql" % (
                    self.extrafile, db, path, db)
                # print("%s\n" % cmd)
                if self.debug is False:
                    print("Backup DB: %s" % db)
                    os.system(cmd)

        if self.debug is False:
            print("-done-\n")
        if self.debug is False:
            self.backupUsers()
        self.createTAR()

    def backupUsers(self):
        """ backup Users and Privileges to a yaml file """
        self.Users = []

        runner = CmdRunner()
        cmd = "mysql --defaults-extra-file=%s -e 'SELECT host,user,authentication_string FROM mysql.user;'" % self.extrafile
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
            cmd = "mysql --defaults-extra-file=%s -e \"SHOW GRANTS FOR '%s'@'%s';\"" % (
                self.extrafile, u.get_username(), "%")
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
            cmd = "mysql --defaults-extra-file=%s -e \"SHOW GRANTS FOR '%s'@'localhost';\"" % (
                self.extrafile, u.get_username())
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

        # store relative Path
        # tar -cjf site1.tar.bz2 -C /var/www/site1 .
        # -C = change to that directory, dont miss . at the end!
        full_path = os.path.join(self.backup_path, self.thisbackup_path)
        cmd = "tar -cjf %s --warning=no-file-ignored -C %s ." % (
            self.tarball, full_path)

        if self.debug is False:
            # tar it
            os.system("%s > /dev/null 2>&1" % (cmd))
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
            p = re.compile("\d{4}-\d{1,2}-\d{1,2}")  # noqa
            erg = p.findall(f)
            if erg:
                data.append([f, erg[0]])
        # keep versions
        versions = self.config['misc']['versions']

        # sort with key, take the date as key
        data.sort(key=lambda the_file: the_file[1])

        while(len(data) >= (int(versions) + 1)):
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
