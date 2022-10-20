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
import struct
from winreg import CloseKey, SetValueEx, CreateKey, HKEY_CURRENT_USER, REG_SZ

import click
from rich.console import Console
from rich.table import Table
import yaml


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

        self.share = self.config['config']['SHARE']
        self.isrealtive = False
        if self.config['config']['USE_SHARE'] == 0:
            self.isrealtive = True
        self.wallpaperPath = os.path.join(
            self.rootDir, self.config['config']['PATH'])

        self.loadWallpapers()

    def start(self):
        """ will change the wallpaper """

        rand_index = random.randint(0, len(self.wallpapers))
        path = self.wallpapers[rand_index]
        self.changeWallpaper(path)

        print(self.wallpapers[rand_index])

    def loadWallpapers(self):
        """ 
        load all Wallpapers from PATH/SHARE
        if from SHARE, store them in relative PATH wallpapers/
        """
        self.wallpapers = []
        if self.isrealtive is True:
            self.wallpapers = self.search_files_in_dir(
                self.wallpaperPath, '*.jp[e]?g')

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
    """
    def network_share(self):
        backup_storage_available = os.path.isdir(BACKUP_REPOSITORY_PATH)

        if backup_storage_available:
            logger.info("Backup storage already connected.")
        else:
            logger.info("Connecting to backup storage.")

            mount_command = "net use /user:" + BACKUP_REPOSITORY_USER_NAME + " " + \
                BACKUP_REPOSITORY_PATH + " " + BACKUP_REPOSITORY_USER_PASSWORD
            os.system(mount_command)
            backup_storage_available = os.path.isdir(BACKUP_REPOSITORY_PATH)

            if backup_storage_available:
                logger.fine("Connection success.")
            else:
                raise Exception("Failed to find storage directory.")
    """

    def load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml

    def list(self):
        """ list all wallpapers """
        # see https://rich.readthedocs.io/en/stable/appendix/colors.html
        console = Console()
        console.print("\nWallpapers in path:")
        console.print(self.wallpaperPath, style="green")
        table = Table()
        table.add_column("Nr", style="yellow", no_wrap=True)
        table.add_column("Filename", style="magenta")
        i = 1
        for item in self.wallpapers:
            table.add_row(str(i), str(os.path.basename(item)))
            i += 1

        console.print(table)


@click.command(no_args_is_help=False)
@click.option('-l', '--list', 'listing', is_flag=True, help='list all wallpapers')
def start(listing):
    paper = Wallpaper()
    if listing is True:
        paper.list()
    else:
        # change wallpaper
        paper.start()


if __name__ == "__main__":
    start()  # noqa
