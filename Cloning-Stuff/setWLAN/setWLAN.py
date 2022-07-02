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
        self.keyFile = os.path.join(self.rootDir, 'libs', 'key.key')
        self.logger = logging.getLogger('setWLAN')

        # catch terminating Signal
        atexit.register(self.exit_handler)
        self.config = self._load_yml()
        self.cryptor = Cryptor(self.keyFile)
        
        info = ("setWLAN.py, (c) Mag. Stefan Hagmann 2021\n"
                "- mange WLAN Keys for WIndows\n"
                "-------------------------------------------------------\n")
        print(info)


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
    Will manage WLAN Configurations for Windows
    """
    setwlan = setWLAN()
    if createkey is True:
        setwlan.cryptor.createKeyFile()
    elif encrypt is not None:
        chiper = setwlan.cryptor.encrypt(encrypt)
        print("\n%s: %s" % (encrypt, chiper.decode()))
        print("Use this hash in your config File for sensible data, e.g. passwords")
    else:
        pass
        # normal Operation
        # worker = Worker(sethostname.config, sethostname.rootDir, sethostname.cryptor)
        # worker.doTheJob()


if __name__ == "__main__":
    # load logging Config
    configure_logging()
    start()
