"""
setup.py setHostname
Usage: sudo pip3 install .
"""
__author__ = 'Mag. Stefan Hagmann'

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="O365-Sync",
        description="Manage O365 Accounts in school",
        author=__author__,
        maintainer=__author__,
        license="GPLv3",
        install_requires=[
            # 'O365', 'msal', 'pyjwt == 1.7.1', 'requests',
            'datetime',
            'fsspec',
            'cx_Freeze',
            'rich',
            'pandas',
            'questionary',
        ],
        python_requires='>=3.8',
    )
