"""
setup.py ansible
Usage: sudo pip3 install .
"""
from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="ansible setup",
        install_requires=[
            'ansible',
            'pywinrm',
            'requests-credssp',
            'jmespath',
            'psutil',
            'gputil',
            'tabulate'
        ],
        python_requires='>=3.8',
    )
