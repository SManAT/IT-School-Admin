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
from cryptography.fernet import Fernet
from libs.LoggerConfiguration import configure_logging
from libs.Worker import Worker
import atexit
import shutil
import click


class setHostname():

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
        self.keyFile = os.path.join(self.rootDir, 'libs', 'key.key')
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')
        self.logger = logging.getLogger('setHostname')

        # catch terminating Signal
        atexit.register(self.exit_handler)
        self.config = self._load_yml()

    def _load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml

    def createKeyFile(self):
        """ Create an encryption key """
        # Test if key.key is present
        if (os.path.exists(self.keyFile) is False):
            # create a key file
            key = Fernet.generate_key()
            file = open(self.keyFile, 'wb')
            file.write(key)
            file.close()
            print("KeyFile created in %s" % self.keyFile)

    def do_encrypt(self, estring):
        """ Encrypt this string """
        # if not exists
        self.createKeyFile()

        # read Key File
        file = open(self.keyFile, 'rb')
        key = file.read()
        file.close()

        # encrypt
        fernet = Fernet(key)
        encMessage = fernet.encrypt(estring.encode())
        print("%s: %s" % (estring, encMessage.decode()))
        print("\nUse this hash in your config File for sensible data, e.g. passwords")

    def exit_handler(self):
        """ do something on sys.exit() """
        # be sure to delete tmp/ dir
        if (os.path.exists(self.tmpPath) is True):
            try:
                shutil.rmtree(self.tmpPath)
            except OSError as e:
                print("Error: %s : %s" % (self.tmpPath, e.strerror))


@click.command()
@click.option('-c', '--createkey', required=False, default=False, help='Create an encryption key')
@click.option('-e', '--encrypt', required=False, default=None, help='Will encrypt the TEXT')
def start(createkey, encrypt):
    """
    After a fresh Cloning session, this tool will do
    - rename to Hostname via MAC Address from a MySQL Database
    - will join a defined domain
    - will activate KMS and will contact it
    - when finished, client will shut down
    """
    sethostname = setHostname()
    if createkey is True:
        sethostname.createKeyFile()
    elif encrypt is not None:
        sethostname.do_encrypt(encrypt)
    else:
        # normal Operation
        worker = Worker(sethostname.config, sethostname.rootDir)
        worker.doTheJob()


if __name__ == "__main__":
    # load logging Config
    configure_logging()
    start()
