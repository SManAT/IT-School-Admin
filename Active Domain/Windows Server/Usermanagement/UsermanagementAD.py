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

from pathlib import Path


class UsermanagementAD():
    """ Backup Samba4 """
    debug = False

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')

        self.config = self.load_yml()
        info = ("UsermanagementAD\n"
                "(c) Mag. Stefan Hagmann 2021\n"
                "will manage AD Users on a Windows Server with Powershell\n"
                "-------------------------------------------------------\n")
        print(info)

        try:
            # ensure BackupPath exists
            pass
        except Exception as ex:
            print(ex)

    def _load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml


@click.command()
@click.option('-f', '--file', required=True, default=False, help='which file to use')
@click.option('-i', '--import', 'importoption', required=False, default=False, help='Import Users aus CSV Datei')
@click.option('-e', '--export', 'exportoption', required=False, default=False, help='Export Users in CSV Datei')
def start(file, importoption, exportoption):
    print(file, importoption, exportoption)
    if importoption is True:

      ou_benutzer = self.config["ad"]["OU_BENUTZER"]
        pass
    elif exportoption is not None:
        pass
    else:
        if file is False:
          ctx = click.get_current_context()
          print(ctx.get_help())


if __name__ == "__main__":
    # load logging Config
    start()
