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
import yaml
from pathlib import Path
from datetime import date, datetime
from lib.CmdRunner import CmdRunner
from lib.RotateBackup import RotateBackup


class BackupGPOs():
    """ Group Policy Backup """
    debug = False
    prefix = "GPO-"

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')

        self.config = self.load_yml()
        versions = self.config['samba']['versions']
        info = ("BackupGPOs\n"
                "(c) Mag. Stefan Hagmann 2021\n"
                "will create a Backup from GPO's via samba-tool\n"
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

    def start(self):
        """ will do the backup """
        # get all GPO IDs
        ids = self.getGPOIDs()
        # backup
        self.backupIDs(ids)
        self.createTAR()

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

    def extractID(self, line):
        """
        get the GPO ID from line, e.g. {6AC1786C-016F-11D2-945F-00C04FB984F9}
        """
        try:
            if "GPO" in line:
                p = re.compile(r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}')
                found = re.findall(p, line)
                return "{%s}" % found[0]
        except Exception:
            return None

    def getGPOIDs(self):
        cmdRunner = CmdRunner()
        cmdRunner.runCmd("samba-tool gpo listall")
        response = cmdRunner.getLines()
        if cmdRunner.getStderr():
            print(cmdRunner.getStderr())
        ids = []
        for line in response:
            print(line)
            i = self.extractID(line)
            if i:
                ids.append(i)
        print("GPO's extracted ...")
        return ids

    def backupIDs(self, ids):
        """ Backup all IDS to this Directory """
        path = os.path.join(self.backup_path, self.thisbackup_path)
        for line in ids:
            cmd = "samba-tool gpo backup %s --tmpdir %s" % (line, path)
            os.system(cmd)

    def cleanUpBackups(self):
        """Rotate Backups to keep #versions"""
        versions = self.config['samba']['versions']
        path = os.path.join(self.rootDir, self.backup_path)
        rotateTool = RotateBackup(versions, path, self.debug)
        rotateTool.cleanUpGPO()

if __name__ == "__main__":
    start_time = datetime.now()

    backup = BackupGPOs()
    backup.start()
    backup.cleanUpBackups()

    time_elapsed = datetime.now() - start_time
    print("Backup of GPO's finished ...")
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
