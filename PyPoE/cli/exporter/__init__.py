"""
GGPK User Interface Classes

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/__init__.py                                   |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Creates a qt User Interface to browse GGPK files.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
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
    from . import pywikibot_setup
except:
    pass

init()
OutputHook(_orig_show_warning)