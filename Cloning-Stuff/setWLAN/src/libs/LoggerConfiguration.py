#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
from pathlib import Path

import logging.config

path_to_yml = "%s/%s" % (Path(__file__).parent.as_posix(),
                         'logger_config.yaml')
loggin_path = Path(__file__).parent.parent.as_posix()


def load_yml():
    """
    Handle the yaml file an add the logging path to filenames
    """
    with open(path_to_yml, 'rt') as f:
        yml_config = yaml.safe_load(f.read())

    # Dateiname mit Pfad anpassen
    for item in yml_config['handlers']:
        part = yml_config['handlers'][item]
        if 'filename' in part:
            filename = yml_config['handlers'][item]['filename']
            yml_config['handlers'][item]['filename'] = '%s/%s' % (
                loggin_path, filename)
    return yml_config


def configure_logging():
    """
    Initialize logging defaults
    """
    logger = logging.getLogger(__name__)
    if os.path.exists(path_to_yml):
        config = load_yml()
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logger.INFO)
