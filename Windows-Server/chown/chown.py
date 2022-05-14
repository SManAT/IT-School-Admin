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

import click
from pathlib import Path

from libs.PSTool import PSTool


class changeOwner():
    """ Backup Samba4 """
    debug = False

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.debug = False

        info = ("\nchangeOwner, (c) Mag. Stefan Hagmann 2022\n"
                "will change Owner from Files and Directories with Powershell\n"
                "-------------------------------------------------------\n")
        print(info)

    def chown(self, user, target):
      tool = PSTool(self.debug)
      tool.chown(user, target)


@click.command()
@click.option('-u', '--user', help='which User to set, e.g. MYDOMAIN\\h.moser')
@click.option('-t', '--target', help='which Target to change (File or Directory)')
def start(user, target):

    if user is None or target is None:
      ctx = click.get_current_context()
      print(ctx.get_help())
      exit(-1)

    if user is not None and target is not None:
      changer = changeOwner()
      changer.chown(user, target)


if __name__ == "__main__":
    start()
