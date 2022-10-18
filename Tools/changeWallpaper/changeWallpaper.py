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
import struct


# https://stackoverflow.com/questions/53878508/change-windows-10-background-in-python-3
class Wallpaper():
    PATH = 'C:\\Users\\Patrick\\Desktop\\0200200220.jpg'
    SPI_SETDESKWALLPAPER = 20

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')
        self.config = self.load_yml()

    def is_64bit_windows(self):
        """Check if 64 bit Windows OS"""
        return struct.calcsize('P') * 8 == 64

    def changeBG(self, path):
        """Change background depending on bit size"""
        if is_64bit_windows():
          # use Unicode string
          # path = 'C:\\Users\\Patrick\\Desktop\\0200200220.jpg'
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, PATH, 3)
        else:
          # use ANSI string
          # path = b'C:\\Users\\Patrick\\Desktop\\0200200220.jpg'
            ctypes.windll.user32.SystemParametersInfoA(
                SPI_SETDESKWALLPAPER, 0, PATH, 3)

    def load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml

    def list(self):
        """ list all wallpapers """
        print('2Do: list all wallpapers')


@click.command(no_args_is_help=True)
@click.option('-l', '--list', 'listing', is_flag=True, help='list all wallpapers')
def start():
    paper = Wallpaper()
    if listing is True:
        paper.list()
    else:
        # change wallpaper
        paper.start()


if __name__ == "__main__":
    start()  # noqa


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
