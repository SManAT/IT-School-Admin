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

import os, sys, re
from pathlib import Path

rootPath = os.path.abspath(os.path.join(os.path.dirname(Path(__file__))))
libPath = os.path.join(rootPath, "./libs")
# add to PYTHON Path
sys.path.insert(0, libPath)
from lib.CmdRunner import CmdRunner


def extractID(line):
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

def getGPOIDs():
    cmdRunner = CmdRunner()
    cmdRunner.runCmd("samba-tool gpo listall")
    response = cmdRunner.getLines()
    ids = []
    for line in response:
        i = extractID(line)
        if i:
            ids.append(i)
    return ids

def backupIDs(ids, path):
    """ Backup all IDS to this Directory """
    for line in ids:
        os.system("samba-tool gpo backup %s --tmpdir %s" % (line, path))   

if __name__ == "__main__":
    path = "./Backup/"
    
    # cleanup
    os.system("rm -r %s > /dev/null 2>&1" % path)
    os.system("mkdir -p %s" % path)
    # get all GPO IDs
    ids = getGPOIDs()
    # backup
    backupIDs(ids, path)
    
    print("GPO's Backup complete ... here the are ...")
    os.system("ls -a %s/policy/" % path)
    
        
        
 
        

