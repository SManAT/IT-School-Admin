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
from pathlib import Path
import argparse
import os
import sys


class BuildPyInstaller():
    """ a wrapper for some PyInstaller cmds """
    mainFile = "setHostname.py"

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.read_cli_args()
        parts = self.mainFile.split(".")
        self.fname = parts[0]
        self.start()

    def read_cli_args(self):
        """ Read the command line args passed to the script """
        # see https://www.golinuxcloud.com/python-argparse/
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--init',
                            default=False,
                            dest="init",
                            help='Initialize PyInstaller, will create the *.spec File',
                            action='store_true'
                            )
        parser.add_argument('-b', '--build',
                            default=True,
                            dest='build',
                            help='Build your Executeable',
                            action='store_true'
                            )
        parser.add_argument('-f', '--file',
                            default=None,
                            required=True,
                            dest='file',
                            help='which File to parse',
                            type=str
                            )
        args = parser.parse_args()

        self.init = args.init
        self.build = args.build
        self.file = args.file

    def start(self):
        """ do main Job """
        if self.init is True:
            cmd = "pyi-makespec %s" % self.mainFile
            print(cmd)
            os.system(cmd)
            print("---")
            
            print("Make your changes to the %s.spec file" % self.fname)
            print("then build it with python build.py -f %s" % self.mainFile)
            sys.exit(1)
        elif self.build is True:
            cmd = "pyinstaller %s.spec -w -y" % self.fname
            print(cmd)
            os.system(cmd)
            print("---")
            
            print("Build complete, see dist/ for result")


if __name__ == "__main__":
    build = BuildPyInstaller()
