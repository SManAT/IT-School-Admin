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

from pathlib import Path


def getSubDirs(rootdir):
  """ get alls Subdirectories from rootdir, not recursive """
  return [f.path for f in os.scandir(rootdir) if f.is_dir()]


def startUp(go, domain, path):
  """ do your Job """
  if path is None:
    rootDir = Path(__file__).parent
  else:
    # use Path
    rootDir = path
  dirs = getSubDirs(rootDir)

  print("\n")

  for dir in dirs:
    # extract Username
    parts = os.path.split(dir)
    username = "%s\\%s" % (domain, parts[len(parts) - 1])
    if username == "Administrator":
      print("%s will not be processed! - skipping-" % username)
    else:
      print("Set Owner (%s) on: %s" % (username, dir))

      path = os.path.join(Path(__file__).parent, "chown", "chown.py")
      cmd = "python %s -u %s -t %s" % (path, username, dir)
      if go is True:
        os.system(cmd)
        print("\n----\n")

  if go is False:
    print("\n==================================================================")
    print("Simulation > ausführen mit -g Parameter !")
    print("==================================================================\n")


@click.command()
@click.option('-g', '--go', is_flag=True, help='go, do it!')
@click.option('-d', '--domain', required=True, help='the Domainname')
@click.option('-p', '--path', required=False, help='which Path to work on')
def start(go, domain, path):
  startUp(go, domain, path)


if __name__ == "__main__":
    start()
