#!/usr/bin/env python
import os


from .rules import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def load_config():
    """
    Load a config class
    """
    from .config import Config
    return Config


CONFIG = load_config()
