#!/usr/bin/env python
import os
import logging

from .rules import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'logs/download.log'),
    filemode='a',
    format=logging_format,
    level=logging.DEBUG
)
LOGGER = logging.getLogger()


def load_config():
    """
    Load a config class
    """
    from .config import Config
    return Config


CONFIG = load_config()
