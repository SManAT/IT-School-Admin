"""
setup.py setHostname
Usage: sudo pip3 install .
"""
__author__ = 'Mag. Stefan Hagmann'

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="UsermanagementAD",
        description="Manage AD Users on a Windows Server via Powershell",
        author=__author__,
        maintainer=__author__,
        license="GPLv3",
        install_requires=[
            'pyyaml',
            'click',
            'pandas',
        ],
        python_requires='>=3.8',
    )
