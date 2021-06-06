__author__ = 'Mag. Stefan Hagmann'

from distutils.core import setup

if __name__ == '__main__':

    setup(
        name="MySQLBackup",
        description="MySQLBackup",
        author=__author__,
        maintainer=__author__,
        license="GPLv3",
        install_requires=[
            'PyYAML',
        ],
        python_requires='>=3.8',
    )
