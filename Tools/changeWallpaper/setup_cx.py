"""
cx_Freeze
see https://cx-freeze.readthedocs.io/en/latest/distutils.html
Build a executeable App for everything.
Windows: python setup_cx.py build_exe
"""
from distutils.dir_util import copy_tree
import os
from pathlib import Path
import sys

from cx_Freeze import setup, Executable

__author__ = 'Mag. Stefan Hagmann'
__version__ = '1.0.0'
# without Extension
__pyfile__ = "changeWallpaper"

# use relative paths
include_files = ['config.yaml', 'README.md']
include_dirs = []
includes = []
excludes = []
packages = []
# add other dirs to search for custom modules
path = ["libs"] + sys.path

# base="Win32GUI" should be used only for Windows UIs
if sys.platform == "win32":
    base = "Win32GUI"
# Console App
base = None

setup(
    name=__pyfile__,
    description="change Wallpaper of Win10",
    version=__version__,
    executables=[Executable(__pyfile__ + '.py', base=base, icon='App.ico')],
    options={'build_exe': {
        'packages': packages,
        'includes': includes,
        'include_files': include_files,
        'include_msvcr': True,
        'excludes': excludes,
        'path': path
        # 'optimize': 2
    }},
)

# Copy needed directories ------------------------

# search all build subdirs
depth = 1
rootPath = Path(__file__).parent
searchPath = os.path.abspath(os.path.join(rootPath, "build/"))

copyTo = []
for root, dirs, files in os.walk(searchPath):
    if root[len(searchPath):].count(os.sep) < depth:
        for dirpath in dirs:
            copyTo.append(os.path.join(searchPath, dirpath))
# copy additional dirs to lib/ folder
for dirpath in copyTo:
    for incdir in include_dirs:
        copy_tree(incdir, os.path.join(dirpath, "lib", incdir))
