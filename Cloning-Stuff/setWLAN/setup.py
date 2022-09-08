"""
setup.py setWLAN
Usage: sudo pip3 install .
"""
__author__ = 'Mag. Stefan Hagmann'

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="setWLAN",
        description="manage WLAN Keys for Windows (encrypted)",
        author=__author__,
        maintainer=__author__,
        license="GPLv3",
        install_requires=[
            'cryptography',
            'click',
            'PyYAML',
            'lxml',
            'wheel',
            'cx_Freeze',
        ],
        python_requires='>=3.8',
    )
