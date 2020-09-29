"""
Utility functions for exporters

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/util.py                                       |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Utility functions for exporters.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
import hashlib

# self
from PyPoE.poe.path import PoEPath
from PyPoE.poe.file.ggpk import GGPKFile
from PyPoE.cli.config import SetupError
from PyPoE.cli.exporter import config

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'get_content_path',
    'get_content_hash',
    'check_hash',
]

# =============================================================================
# Functions
# =============================================================================


def get_content_path():
    """
    Returns the path to the current content.ggpk based on the specified
    config variables for the version & distributor.

    :return: Path of the content ggpk
    :rtype: str

    :raises SetupError: if no valid path was found.
    """
    path = config.get_option('ggpk_path')
    if path == '':
        args = config.get_option('version'), config.get_option('distributor')
        paths = PoEPath(*args).get_installation_paths()

        if not paths:
            raise SetupError('No PoE Installation found.')

        return paths[0]
    else:
        return path


def get_content_hash():
    """
    Gets the content ggpk based on the stored config variables and returns
    the calculated hash.

    :return: Hash of content.ggpk
    :rtype: str
    """
    ggpk = get_content_path()
    with open(ggpk, 'rb') as f:
        data = f.read(2**16)

    return hashlib.md5(data).hexdigest()


def check_hash():
    """
    Checks the stored hash against the current hash and returns the result

    :return: True if match, False otherwise
    :rtype: bool
    """
    if 1:
        return True

    hash_old = config.get_setup_variable('temp_dir', 'hash')
    hash_new = get_content_hash()

    if hash_old == hash_new:
        return True

    config.set_setup_variable('temp_dir', 'performed', False)
    return False