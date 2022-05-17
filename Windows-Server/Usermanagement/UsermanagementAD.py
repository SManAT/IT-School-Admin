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
import click
import yaml
import logging
import sys

from pathlib import Path
from libs.CSVTool import CSVTool
from libs.LoggerConfiguration import configure_logging
from libs.Counter import Counter
from libs.ScriptTool import ScriptTool
from libs.Error import Error

class UsermanagementAD():
    """ Backup Samba4 """
    debug = False

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')

        # Logging Stuff
        self.logger = logging.getLogger('UsermanagementAD')
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')

        self.config = self.load_yml()
        self.debug = False
        if self.config['config']['DEBUG'] == 1:
          self.debug = True

        self.error = Error()

        info = ("\nUsermanagementAD, (c) Mag. Stefan Hagmann 2021\n"
                "will manage AD Users on a Windows Server with Powershell\n"
                "-------------------------------------------------------\n")
        print(info)

        if self.debug:
          print("TEST MODE, no script will be executed (see config.yaml)\n")

        self.counter = Counter()
        self.csv = CSVTool(self.debug)
        self.tool = ScriptTool(self.rootDir, self.error, self.config, self.debug, self.counter)

    def load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml

    def Import(self, file):
      """ Import Users from CSV File """
      self.csv.read(file)

      for user in self.csv.getUsers():
        if user.isValid():
          self.error.reset()  # set no errors yet
          if self.tool.existsUser(user) is False:
            self.tool.addUser(user)
          else:
            self.counter.incUserExists()
            print("User EXISTS: %s\n" % user.getFullname())
        else:
          print("INVALID Data: %s" % user)
          self.counter.incUserInvalid()

      print("\n---------------------------------------------------")
      # :<25 box with 25 chars length
      print(f"{'Wrong Groups: ':<26} { str(self.counter.getWrongGroups()) }")
      print(f"{'Import done ... ':<25} +{self.counter.getCreatedUser()} ({str(self.counter.getUserExists())} Existing Users, {str(self.counter.getUserInvalid())} Invalid Users)")

    def Export(self):
      """ Export Users to CSV File """
      pass


@click.command()
@click.option('-f', '--file', required=True, help='which file to use')
@click.option('-i', '--import', 'importoption', is_flag=True, help='Import Users aus CSV Datei')
@click.option('-e', '--export', 'exportoption', is_flag=True, help='Export Users in CSV Datei')
def start(file, importoption, exportoption):

    if file is False:
      ctx = click.get_current_context()
      print(ctx.get_help())
      exit(-1)

    if importoption is True:
      userMgmt = UsermanagementAD()
      userMgmt.Import(file)
    elif exportoption is not None:
      userMgmt = UsermanagementAD()
      userMgmt.Export()


if __name__ == "__main__":
    # load logging Config
    configure_logging()
    start()
