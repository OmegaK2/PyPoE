"""
Abstract Cache

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/shared/cache.py                                   |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Abstract Cache

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party

# self
from PyPoE.poe.file.ggpk import GGPKFile

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================

class AbstractFileCache(object):
    """
    Abstract File Cache

    :ivar _ggpk:
    :type _ggpk: GGPKFile

    :ivar _path:
    :type _path: str
    """
    def __init__(self, path_or_ggpk=None):
        """
        :param path_or_ggpk: The path where the dat files are stored or a
        GGPKFile instance
        :type path_or_ggpk: :class:`GGPKFile` or str

        :raises TypeError: if path_or_ggpk not specified or invalid type
        :raises ValueError: if a GGPKFile was passed, but it was not parsed
        """
        if isinstance(path_or_ggpk, GGPKFile):
            if not path_or_ggpk.is_parsed:
                raise ValueError('The GGPK File must be parsed.')
            self._ggpk = path_or_ggpk
            self._path = None
        elif isinstance(path_or_ggpk, str):
            self._ggpk = None
            self._path = path_or_ggpk
        else:
            raise TypeError('path_or_ggpk must be a valid directory or GGPKFile')

# =============================================================================
# Functions
# =============================================================================