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
import warnings

# 3rd-Party
from colorama import init

# self
from PyPoE import APP_DIR
from PyPoE.cli.config import ConfigHelper
from PyPoE.cli.core import OutputHook

# =============================================================================
# Globals
# =============================================================================

__all__ = ['CONFIG_PATH', 'config']

CONFIG_PATH = os.path.join(APP_DIR, 'exporter.conf')

config = ConfigHelper(infile=CONFIG_PATH)

# =============================================================================
# Bugfixes / Init
# =============================================================================
# pywikibot hooks into the output and we really don't want that
_orig_show_warning = warnings.showwarning
try:
    import pywikibot
except:
    pass

init()
OutputHook(_orig_show_warning)