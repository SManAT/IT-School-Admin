"""
setup.py setHostname
Usage: sudo pip3 install .
"""
__author__ = 'Mag. Stefan Hagmann'

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="changeOwner",
        description="change Owner from Files and Directories with Powershell",
        author=__author__,
        maintainer=__author__,
        license="GPLv3",
        install_requires=[
            'pyyaml',
            'click',
        ],
        python_requires='>=3.8',
    )
