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

import ctypes
import os
from pathlib import Path
import random
import shutil
import struct
from winreg import CloseKey, SetValueEx, CreateKey, HKEY_CURRENT_USER, REG_SZ

import click
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
import yaml

from libs import Cryptor


# https://stackoverflow.com/questions/53878508/change-windows-10-background-in-python-3
class Wallpaper():
    STYLE = {
        'CENTER': 0,
        'STRECH': 2,
        'FIT': 6,
        'FILL': 10,
        'SPAN': 22
    }

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
        self.config = self.load_yml()

        self.console = Console()

        self.share = self.config['config']['share']['PATH']
        self.last = self.config['config']['LAST']
        self.isrealtive = False
        if self.config['config']['USE_SHARE'] == 0:
            self.isrealtive = True
        self.wallpaperPath = os.path.join(
            self.rootDir, self.config['config']['LOCAL_PATH'])

        self.TMP_WALLPAPER_PATH = os.path.join(
            self.rootDir, self.config['config']['LOCAL_STORAGE'])

        if os.path.isdir(self.TMP_WALLPAPER_PATH) is False:
            os.mkdir(self.TMP_WALLPAPER_PATH)

    def start(self):
        """ will change the wallpaper """
        if self.isrealtive is False:
            # use net Share
            self.connect_network_share(self.share)
            self.wallpaperPath = self.share
            self.loadWallpapers(True)
        else:
            self.loadWallpapers()

        rand_index = random.randint(0, len(self.wallpapers))
        path = self.wallpapers[rand_index]

        while self.last == os.path.basename(path):
            rand_index = random.randint(0, len(self.wallpapers))
            path = self.wallpapers[rand_index]

        self.changeWallpaper(path)

        self.storeLastOne(path)

    def storeLastOne(self, filename):
        """ stores the last used wallpaer in config.yaml """
        data = dict(
            config=dict(
                USE_SHARE=self.config['config']['USE_SHARE'],
                LOCAL_PATH=self.config['config']['LOCAL_PATH'],
                LOCAL_STORAGE=self.config['config']['LOCAL_STORAGE'],
                LAST=os.path.basename(filename),

                share=dict(
                    PATH=self.config['config']['share']['PATH'],
                    USER=self.config['config']['share']['USER'],
                    PWD=self.config['config']['share']['PWD']
                )
            )
        )
        with open(self.configFile, 'w', encoding="UTF-8") as f:
            yaml.dump(data, f, sort_keys=False, default_flow_style=False)

    def loadWallpapers(self, copy=False):
        """ 
        load all Wallpapers from PATH/SHARE
        :param copy: copy wallpapers from Share to host into TMP_WALLPAPER_PATH
        """
        self.wallpapers = []
        self.wallpapers = self.search_files_in_dir(
            self.wallpaperPath, '*.jp[e]?g')

        if copy is True:
            newwallpapers = []
            # copy the new once to TMP_WALLPAPER_PATH
            for file in self.wallpapers:
                target = os.path.join(self.TMP_WALLPAPER_PATH,
                                      os.path.basename(file))
                if os.path.exists(target) is False:
                    shutil.copy(file, self.TMP_WALLPAPER_PATH)
                newwallpapers.append(target)
            self.wallpapers = newwallpapers

    def search_files_in_dir(self, directory='.', pattern=''):
        """
        search for pattern in directory NOT recursive
        :param directory: path where to search. relative or absolute
        :param pattern: a list e.g. ['.jpg', '.gif']
        """
        data = []
        for child in Path(directory).iterdir():
            if child.is_file():
                # print(f"{child.name}")
                if pattern == '':
                    data.append(os.path.join(directory, child.name))
                else:
                    for p in pattern:
                        if child.name.endswith(p):
                            data.append(os.path.join(directory, child.name))
        return data

    # Wallpaper Section ------------------------------------------------------
    def is_64bit_windows(self):
        """Check if 64 bit Windows OS"""
        return struct.calcsize('P') * 8 == 64

    def changeWallpaper(self, filepath, STYLE=None):
        """
        Change background depending on bit size
        0: The image is centered if TileWallpaper=0 or tiled if TileWallpaper=1
        2: Strech
        6: Fit
        10: Fill
        22: Span
        """
        # Default value
        if STYLE is None:
            STYLE = self.STYLE['STRECH']
        STYLE = self.STYLE['SPAN']
        # 16:9 STRECH
        # 4:3 FILL

        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x01     # forces instant update
        SPIF_SENDWININICHANGE = 0x02  # noqa
        TILEWALLPAPER = 0

        if self.is_64bit_windows():
            # use Unicode string
            # path = 'C:\\Users\\...\\Desktop\\0200200220.jpg'
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, STYLE, filepath, SPIF_UPDATEINIFILE)
        else:
            # use ANSI string
            # path = b'C:\\Users\\...\\Desktop\\0200200220.jpg'
            filepath = bytes(filepath, 'UTF-8')
            ctypes.windll.user32.SystemParametersInfoA(
                SPI_SETDESKWALLPAPER, STYLE, filepath, SPIF_UPDATEINIFILE)

        # Registry anpassen, erst dann klappts
        keyVal = r'Control Panel\Desktop'
        key = CreateKey(HKEY_CURRENT_USER, keyVal)
        SetValueEx(key, "TileWallpaper", 0, REG_SZ, str(TILEWALLPAPER))
        SetValueEx(key, "WallpaperStyle", 0, REG_SZ, str(STYLE))
        CloseKey(key)

    # NET SHARE Section ------------------------------------------------------

    def connect_network_share(self, path, username="", pwd=""):
        """ 
        connect to a Network share
        :param path: the unc path to the share
        :param username: the username to connect with
        :param pwd: the password for the user
        """
        backup_storage_available = os.path.isdir(path)

        if backup_storage_available:
            print("Already connected with SHARE %s ..." % path)
        else:
            print("Connecting to backup storage.")
            mount_command = 'net use "%s" /persistent:no /user:"%s" "%s"' % (
                path, username, pwd)

            os.system(mount_command)
            backup_storage_available = os.path.isdir(path)

            if backup_storage_available:
                print("Connection to SHARE success...")
            else:
                raise Exception("Failed to connect to SHARE %S ..." % path)

    def load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml

    def list(self):
        """ list all wallpapers """
        # see https://rich.readthedocs.io/en/stable/appendix/colors.html
        self.wallpapers = []
        self.wallpapers = self.search_files_in_dir(
            self.TMP_WALLPAPER_PATH, '*.jp[e]?g')

        self.console.print("\nWallpapers in path:")
        self.console.print(self.TMP_WALLPAPER_PATH, style="green")
        table = Table()
        table.add_column("Nr", style="yellow", no_wrap=True)
        table.add_column("Filename", style="magenta")
        i = 1
        for item in self.wallpapers:
            table.add_row(str(i), str(os.path.basename(item)))
            i += 1

        self.console.print(table)

    def clear(self):
        """ delete all local stored wallpapers """
        for root, dirs, files in os.walk(self.TMP_WALLPAPER_PATH):
            for file in files:
                os.remove(os.path.join(root, file))
        self.console.print("All wallpapers deleted!", style="red")


@click.command(no_args_is_help=False)
@click.option('-l', '--list', 'listing', is_flag=True, help='list all wallpapers')
@click.option('--clear', 'clear', is_flag=True, help='delete all local stored wallpapers')
@click.option('-e', '--encrypt', required=False, default=None, help='Will encrypt the TEXT')
def start(listing, clear, encrypt):
    paper = Wallpaper()
    if listing is True:
        paper.list()
        exit()
    if clear is True:
        paper.clear()
        exit()

    if encrypt is not None:
        cryptor = Cryptor()
        chiper = cryptor.encrypt(encrypt)
        print("\n%s: %s" % (encrypt, chiper.decode()))
        print("Use this hash in your config File for sensible data, e.g. passwords")

    # change wallpaper
    paper.start()


def checkKeyFile():
    """ will create an encrypr Key if no one exists """
    rootDir = Path(__file__).parent
    keyFile = os.path.join(rootDir, 'libs', 'key.key')
    if (os.path.exists(keyFile) is False):
        key = Fernet.generate_key()
        file = open(keyFile, 'wb')
        file.write(key)
        file.close()
        print("KeyFile created in %s" % keyFile)


if __name__ == "__main__":
    checkKeyFile()
    start()  # noqa
