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
from pathlib import Path

import yaml
import logging
from libs.LoggerConfiguration import configure_logging
from libs.Worker import Worker
import atexit
import shutil
import click
from libs.Cryptor import Cryptor


class setWLAN():

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
        self.keyFile = os.path.join(self.rootDir, 'libs', 'key.key')
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')
        self.logger = logging.getLogger('setHostname')

        # catch terminating Signal
        atexit.register(self.exit_handler)
        self.config = self._load_yml()
        self.cryptor = Cryptor(self.keyFile)
        
        info = ("setHostname.py, (c) Mag. Stefan Hagmann 2021\n"
                "- is changing Hostname of client with Powershell\n"
                "- hostname is loaded via MAC from MySQL Databse\n"
                "- is joining a domain\n"
                "- will reset KMS\n"
                "- see config.yaml for config parameters\n"
                "-------------------------------------------------------\n")
        print(info)

    def _load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml


    def exit_handler(self):
        """ do something on sys.exit() """
        # be sure to delete tmp/ dir
        if (os.path.exists(self.tmpPath) is True):
            try:
                shutil.rmtree(self.tmpPath)
            except OSError as e:
                print("Error: %s : %s" % (self.tmpPath, e.strerror))


@click.command()
@click.option('-c', '--createkey', required=False, is_flag=True, help='Create an encryption key')
@click.option('-e', '--encrypt', required=False, default=None, help='Will encrypt the TEXT')
@click.option('-l', '--list', required=False, default=None, help='List all WLAN Keys')
@click.option('-d', '--delete', required=False, default=None, help='Delete a WLAN Key')
@click.option('-a', '--add', required=False, default=None, help='Add a WLAN Key')
def start(createkey, encrypt, list, delete, add):
    """
    Will manage WLAN COnfigurations for Windows
    """
    sethostname = setHostname()
    if createkey is True:
        sethostname.cryptor.createKeyFile()
    elif encrypt is not None:
        chiper = sethostname.cryptor.encrypt(encrypt)
        print("\n%s: %s" % (encrypt, chiper.decode()))
        print("Use this hash in your config File for sensible data, e.g. passwords")
    else:
        # normal Operation
        worker = Worker(sethostname.config, sethostname.rootDir, sethostname.cryptor)
        worker.doTheJob()


if __name__ == "__main__":
    # load logging Config
    print("# debug is active ....!")
    configure_logging()
    start()
