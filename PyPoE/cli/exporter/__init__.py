"""
Path     PyPoE/cli/exporter/core.py
Name     GGPK User Interface Classes
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Creates a qt User Interface to browse GGPK files.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# self
from PyPoE import APP_DIR
from PyPoE.cli.config import ConfigHelper

# =============================================================================
# Globals
# =============================================================================

__all__ = ['CONFIG_PATH', 'config']

CONFIG_PATH = os.path.join(APP_DIR, 'exporter.conf')

config = ConfigHelper(infile=CONFIG_PATH)