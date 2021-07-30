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
import argparse

import yaml
import logging
from cryptography.fernet import Fernet
from libs.LoggerConfiguration import configure_logging
from libs.Worker import Worker
import atexit
import shutil


class setHostname():
    """
    After a fresh Cloning session, this tool will do
    - rename to Hostname via MAC Address from a MySQL Database
    - will join a defined domain
    - will activate KMS and will contact it
    - when finished, client will shut down
    """

    _debug = False

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
        self.keyFile = os.path.join(self.rootDir, 'libs', 'key.key')
        self.tmpPath = os.path.join(self.rootDir, 'tmp/')
        self.logger = logging.getLogger('setHostname')

        # catch terminating Signal
        atexit.register(self.exit_handler)

        self.read_cli_args()
        self.config = self._load_yml()

    def _load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml

    def read_cli_args(self):
        """ Read the command line args passed to the script """
        # see https://www.golinuxcloud.com/python-argparse/
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--createkey',
                            default=False,
                            action='store_true',
                            dest="createkey",
                            help='Create an encryption key'
                            )
        parser.add_argument('-e', '--encrypt',
                            default=None,
                            dest='estring',
                            help='Encrypt this string',
                            type=str,
                            required=False
                            )
        args = parser.parse_args()

        self.estring = args.estring
        self.createkey = args.createkey

    def start(self):
        if self.createkey is True:
            # encrypt something
            self.createKeyFile()
        elif self.estring is not None:
            self.do_encrypt()

        else:
            # normal Operation
            worker = Worker(self.config, self.rootDir)
            worker.doTheJob()

    def createKeyFile(self):
        # Test if key.key is present
        if (os.path.exists(self.keyFile) is False):
            # create a key file
            key = Fernet.generate_key()
            file = open(self.keyFile, 'wb')
            file.write(key)
            file.close()
            print("KeyFile created in %s" % self.keyFile)

    def do_encrypt(self):
        """ will encrypt a String """
        # if not exists
        self.createKeyFile()

        # read Key File
        file = open(self.keyFile, 'rb')
        key = file.read()
        file.close()

        # encrypt
        fernet = Fernet(key)
        encMessage = fernet.encrypt(self.estring.encode())
        print("%s: %s" % (self.estring, encMessage.decode()))
        print("\nUse this hash in your config File for sensible data, e.g. passwords")

    def exit_handler(self):
        """ do something on sys.exit() """
        # be sure to delete tmp/ dir
        if (os.path.exists(self.tmpPath) is True):
            try:
                shutil.rmtree(self.tmpPath)
            except OSError as e:
                print("Error: %s : %s" % (self.tmpPath, e.strerror))


if __name__ == "__main__":
    # load logging Config
    configure_logging()
    sethostname = setHostname()
    sethostname.start()

