"""
setup.py setHostname
Usage: sudo pip3 install .
"""
from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="setHostname setup",
        install_requires=[
            'PyYAML',
            'mysql.connector',
        ],
        python_requires='>=3.8',
    )
