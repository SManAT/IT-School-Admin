#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) Mag. Stefan Hagmann 2021

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
from pathlib import Path

import yaml
import logging
from libs.LoggerConfiguration import configure_logging


class setHostname():
    """
    After a fresh Cloning session, this tool will do
    - rename to Hostname via MAC Address from a MySQL Database
    - will join a defined domain
    - will activate KMS and will contact it
    - when finished, client will shut down
    """

    _debug = False

    def __init__(self):
        self.rootDir = Path(__file__).parent
        self.configFile = os.path.join(self.rootDir, 'config.yaml')

        self.config = self._load_yml()
        
        self.logger = logging.getLogger('setHostname')
        self.start()

    def _load_yml(self):
        """ Load the yaml file config.yaml """
        with open(self.configFile, 'rt') as f:
            yml = yaml.safe_load(f.read())
        return yml

    def start(self):
        self.logger.debug("debug")
        self.logger.info("info")
        self.logger.warning("warn")
        self.logger.critical("critical")
        self.logger.error("error")
        self.logger.error("TEST")


if __name__ == "__main__":
    # load logging Config
    configure_logging()
    sethostname = setHostname()
    sethostname.start()
