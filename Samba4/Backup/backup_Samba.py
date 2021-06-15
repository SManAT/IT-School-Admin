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

import os
import sys
import re
import fnmatch

from pathlib import Path
from datetime import date, datetime
from lib.RotateBackup import RotateBackup
import yaml

class BackupSamba4():
    """ Backup Samba4 """
    debug = False
    prefix = "Samba4-"

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')

        self.config = self.load_yml()
        versions = self.config['samba']['versions']
        info = ("Backup Samba4s\n"
                "(c) Mag. Stefan Hagmann 2021\n"
                "will create a Backup from Samba4 AD\n"
                "  - will keep last %s Versions of Backups\n"
                "  - run as root!\n"
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
        """ check if BackupPath exists """
        path = self.config['samba']['backupPath']
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

        self.thisbackup_path = "%s%s" % (self.prefix, today.strftime("%Y-%m-%d"))

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

    def search_files(self, directory, pattern):
        """ search for pattern in directory recursive """
        data = []
        for dirpath, dirnames, files in os.walk(directory):  # noqa
            for f in fnmatch.filter(files, pattern):
                data.append(os.path.join(dirpath, f))
        return data

    def removeBackFiles(self, path):
        """ search for *.ldb.bak and remove them """
        files = self.search_files(path, "*.ldb.bak")
        for f in files:
            fpath = os.path.join(path, f)
            os.system("rm %s" % fpath)
            if self.debug is True:
                print("Removing %s" % fpath)

    def backupTdb(self, path):
        """
        backup all Database Files
        tdbbackup will create a *.ldb.bak file
        """
        files = self.search_files(path, "*.ldb")
        for f in files:
            fpath = os.path.join(path, f)
            if self.debug is True:
                print("tdbbackup %s" % fpath)
            os.system("tdbbackup %s" % fpath)

    def createTAR(self, path, filename):
        """ create Tarballs """
        # is there a today backup?
        self.tarball = "%s.tar.bzip2" % os.path.join(
            self.backup_path, self.thisbackup_path, filename)
        if os.path.isfile(self.tarball) is True:
            self.exitScript(self.tarball)

        # store relative Path
        # tar -cjf site1.tar.bz2 -C /var/www/site1 .
        # -C = change to that directory, dont miss . at the end!
        full_path = path
        cmd = "tar -cjf %s --acls --xattrs --exclude=\*.ldb --exclude=\*.bak-offline --warning=no-file-ignored --transform 's/.ldb.bak$/.ldb/' -C %s ." % (
            self.tarball, full_path)

        if self.debug is True:
            print(cmd)

        if self.debug is False:
            # tar it
            # os.system("%s > /dev/null 2>&1" % (cmd))
            os.system("%s" % (cmd))
            print("created %s" % self.tarball)
            print("-done-\n")

    def backupSamba(self):
        """ backup Samba Config """
        self.tarball = "%s.tar.bzip2" % os.path.join(
            self.backup_path, self.thisbackup_path, "samba")
        if os.path.isfile(self.tarball) is True:
            self.exitScript(self.tarball)

        full_path = os.path.join("/etc/samba/")
        cmd = "tar -cjf %s --acls --xattrs --exclude=\*.ldb --exclude=\*.bak-offline --warning=no-file-ignored --transform 's/.ldb.bak$/.ldb/' -C %s ." % (
            self.tarball, full_path)

        if self.debug is False:
            # tar it
            # os.system("%s > /dev/null 2>&1" % (cmd))
            os.system("%s" % (cmd))
            print("created %s" % self.tarball)
            print("-done-\n")

    def doBackup(self):
        """ backup all Dirs """
        samba_lib_path = self.config['samba']['SAMBA_LIB']
        DIRS = self.config['samba']['SUB_DIRS']

        for directory in DIRS:
            path = os.path.join(samba_lib_path, directory)
            # saving private
            print("Backup directory %s" % path)
            # remove *.bak Files
            self.removeBackFiles(path)

            # backup all tdb
            print(">  Creating Database Backup Files ...")
            self.backupTdb(path)

            # create Tar Balls
            print(">  Creating Tar Balls of Databases ...")
            self.createTAR(path, directory)

            # remove *.bak Files that where used for backup
            print(">  Removing Database Bak Files ...")
            self.removeBackFiles(path)

        # bis da her gehts
        print("\n>  Backup /etc/samba/ ...")
        self.backupSamba()

    def cleanUpBackups(self):
        """Rotate Backups to keep #versions"""
        versions = self.config['samba']['versions']
        rotateTool = RotateBackup(versions, self.backup_path, self.debug)
        rotateTool.cleanUp()


if __name__ == "__main__":
    start_time = datetime.now()

    backup = BackupSamba4()
    backup.doBackup()
    backup.cleanUpBackups()

    time_elapsed = datetime.now() - start_time
    print("Backup of Samba4 finished ...")
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
