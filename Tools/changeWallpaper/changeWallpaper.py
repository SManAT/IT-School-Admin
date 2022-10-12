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

    def __init__(self):
        pass
    
    PATH = 'C:\\Users\\Patrick\\Desktop\\0200200220.jpg'
    SPI_SETDESKWALLPAPER = 20
    
    def is_64bit_windows(self): 
        """Check if 64 bit Windows OS"""
        return struct.calcsize('P') * 8 == 64
    
    def changeBG(self, path):
        """Change background depending on bit size"""
        if is_64bit_windows():
          # use Unicode string
          # path = 'C:\\Users\\Patrick\\Desktop\\0200200220.jpg'
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, PATH, 3)
        else:
          # use ANSI string
          # path = b'C:\\Users\\Patrick\\Desktop\\0200200220.jpg'
            ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, PATH, 3)
    

def start():
    paper = Wallpaper()
    paper.start()


if __name__ == "__main__":
    start()  # noqa

