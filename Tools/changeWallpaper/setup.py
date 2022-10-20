"""
setup.py setHostname
Usage: sudo pip3 install .
"""
__author__ = 'Mag. Stefan Hagmann'

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="changeWallpaper",
        description="change Wallpaper of Win10",
        author=__author__,
        maintainer=__author__,
        license="GPLv3",
        install_requires=[
            'pyyaml',
            'cx_Freeze',
            'click',
            'rich',
        ],
        python_requires='>=3.8',
    )
