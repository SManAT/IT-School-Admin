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

import os, sys, re, fnmatch
from pathlib import Path
from datetime import timedelta, date

rootPath = os.path.abspath(os.path.join(os.path.dirname(Path(__file__))))
libPath = os.path.join(rootPath, "./libs")
# add to PYTHON Path
sys.path.insert(0, libPath)
from lib.CmdRunner import CmdRunner

# Backup from where
FROMWHERE="/var/lib/samba/"
SAMBA_PATH="/etc/samba/"
# where to place the backups
TO="/backup/Samba-Admin/backup_samba4"
# how many copies will you save
KEEP=10

#### dont change ####    
DIRS=["private", "sysvol", "bind-dns"]
# ISO 8601 standard date
DATE_FORMAT = "%Y-%m-%d"

def checkBackupDir():
    """ be sure the Backup Directory exists """
    global TO
    os.system("mkdir -p %s" % TO)
    
def search_files(directory, pattern):
    """ search for pattern in directory recursive """
    data = []
    for dirpath, dirnames, files in os.walk(directory):
        for f in fnmatch.filter(files, pattern):
            data.append(os.path.join(dirpath, f))
    return data
    
def removeBackFiles(dir):
    """ search for *.ldb.bak and remove them """
    files = search_files(dir, "*.ldb.bak")
    for f in files:
        fpath = os.path.join(dir, f)
        os.system("rm %s" % fpath)
        
def backupTdb(dir):
    """ 
    backup all Database Files
    tdbbackup will create a *.ldb.bak file 
    """
    files = search_files(dir, "*.ldb")
    for f in files:
        fpath = os.path.join(dir, f)
        # create bak Files
        # print("tdbbackup %s" % fpath)
        os.system("tdbbackup %s" % fpath)
        
def createTAR(dir, subdir):
    """ 
    create Tarballs of the database Files
    name is subdir.date.tar.bz2 
    """
    global TO
    x = date.today()
    datestr = x.strftime(DATE_FORMAT)
    targetpath = os.path.join(TO, "%s-%s.tar.bz2" % (subdir, datestr))
    cd_cmd = "cd %s" % dir
    cmd = "tar cjf %s --acls --xattrs --exclude=\*.ldb --warning=no-file-ignored --transform 's/.ldb.bak$/.ldb/' %s" % (targetpath, subdir)
    os.system("%s && %s > /dev/null 2>&1" % (cd_cmd, cmd))
    
def backupSamba():
    """ backup Samba Config """
    global TO
    x = date.today()
    datestr = x.strftime(DATE_FORMAT)
    targetpath = os.path.join(TO, "samba-%s.tar.bz2" % (datestr))
    cmd = "tar cjf %s --acls --xattrs --warning=no-file-ignored %s" % (targetpath, SAMBA_PATH)
    os.system("%s > /dev/null 2>&1" % cmd)

def doBackup():
    """ backup all Dirs """
    global DIRS, FROMWHERE
    
    for dir in DIRS:
        # saving private
        print("------------------------------------------")
        print("Backup directory %s%s" % (FROMWHERE, dir))
        # remove *.bak Files
        removeBackFiles(os.path.join(FROMWHERE, dir))
        # backup all tdb
        print("  >  Creating Database Backup Files ...")
        backupTdb(os.path.join(FROMWHERE, dir))
        # create Tar Balls
        print("  >  Creating Tar Balls of Databases ...")
        createTAR(FROMWHERE, dir)
        # remove *.bak Files that where used for backup
        print("  >  Removing Database Bak Files ...")
        removeBackFiles(os.path.join(FROMWHERE, dir))
    
    print("------------------------------------------")
    print("  >  Backup /etc/samba/ ...")
    backupSamba()

if __name__ == "__main__":
    checkBackupDir()
    doBackup()
    
    
    
    
    
    
    x = date.today()
    print(x.strftime(DATE_FORMAT)) 
    end_date = x + timedelta(days=10)
    print(end_date)
        
        
 
        

