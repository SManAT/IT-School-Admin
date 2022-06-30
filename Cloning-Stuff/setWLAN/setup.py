"""
setup.py setHostname
Usage: sudo pip3 install .
"""
__author__ = 'Mag. Stefan Hagmann'

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="setHostname",
        description="set the hostname of a windows client via MySQL",
        author=__author__,
        maintainer=__author__,
        license="GPLv3",
        install_requires=[
            'PyYAML',
            'mysql-connector-python',
            'cryptography',
            'click',
            'psutil',
            'cx_Freeze',
        ],
        python_requires='>=3.8',
    )
