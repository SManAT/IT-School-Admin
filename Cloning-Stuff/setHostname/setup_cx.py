"""
cd_Freeze
see https://cx-freeze.readthedocs.io/en/latest/distutils.html
"""
import sys
import os
from cx_Freeze import setup, Executable
from distutils.dir_util import copy_tree
from pathlib import Path

__author__ = 'Mag. Stefan Hagmann'
__version__ = '1.0.0'
# without Extension
__pyfile__ = "setHostname"

# use relative paths
include_files = ["config.yaml"]
include_dirs = ["libs/", "scripts/"]
includes = []
excludes = []
packages = []

# base="Win32GUI" should be used only for Windows UIs
if sys.platform == "win32":
    base = "Win32GUI"
# Console App
base = None

setup(
    name=__pyfile__,
    description='set the hostname of a windows client via MySQL',
    version=__version__,
    executables=[Executable(__pyfile__ + '.py', base=base, icon='App.ico')],
    options={'build_exe': {
        'packages': packages,
        'includes': includes,
        'include_files': include_files,
        'include_msvcr': True,
        'excludes': excludes,
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
# copy dirs
print(copyTo)
for dirpath in copyTo:
    for incdir in include_dirs:
        copy_tree(incdir, os.path.join(dirpath, incdir))
