"""
setup.py setHostname
Usage: sudo pip3 install .
"""
__author__ = 'Mag. Stefan Hagmann'

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="O365Create",
        description="Create O365 Accounts Helper",
        author=__author__,
        maintainer=__author__,
        license="GPLv3",
        install_requires=[
            'datetime',
            'fsspec',
            'cx_Freeze',
            'rich',
            'pandas',
            'questionary',
            'universal-startfile',
        ],
        python_requires='>=3.8',
    )
