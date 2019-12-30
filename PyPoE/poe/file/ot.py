"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/ot.py                                             |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Support for .ot file format.

.ot file seem to be generally used for server-side settings related to abstract
objects.

Generally make sure to consider the context of the file when interpreting the
contents; there is a chance they're extended or embedded though .dat files and
the key/value pairs found are in relevance to the context.

Usually they're accompanied by .otc files which handle client-side settings.

See also:

* :mod:`PyPoE.poe.file.otc`
* :mod:`PyPoE.poe.file.dat`

Agreement
===============================================================================

See PyPoE/LICENSE


Documentation
===============================================================================

.. autoclass:: OTFile
    :exclude-members: clear, copy, default_factory, fromkeys, get, items, keys, pop, popitem, setdefault, update, values

.. autoclass:: OTFileCache

"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party

# self
from PyPoE.shared.decorators import doc
from PyPoE.poe.file.shared.keyvalues import *

# =============================================================================
# Globals
# =============================================================================

__all__ = ['OTFile', 'OTFileCache']

# =============================================================================
# Classes
# =============================================================================


class ActionKeyValueSection(AbstractKeyValueSection):
    NAME = 'Actor'


class AnimatedKeyValueSection(AbstractKeyValueSection):
    NAME = 'Animated'


class BaseKeyValueSection(AbstractKeyValueSection):
    NAME = 'Base'
    ORDERED_HASH_KEYS = {'tag'}


class ModsKeyValueSection(AbstractKeyValueSection):
    NAME = 'Mods'
    ORDERED_HASH_KEYS = {'enable_rarity'}


class PathfindingKeyValueSection(AbstractKeyValueSection):
    NAME = 'Pathfinding'


class PositionedKeyValueSection(AbstractKeyValueSection):
    NAME = 'Positioned'


class SocketsKeyValueSection(AbstractKeyValueSection):
    NAME = 'Sockets'


class StatsKeyValueSection(AbstractKeyValueSection):
    NAME = 'Stats'


@doc(append=AbstractKeyValueFile)
class OTFile(AbstractKeyValueFile):
    """
    Representation of a .ot file.
    """

    SECTIONS = dict((s.NAME, s) for s in [
        ActionKeyValueSection,
        AnimatedKeyValueSection,
        BaseKeyValueSection,
        ModsKeyValueSection,
        PathfindingKeyValueSection,
        PositionedKeyValueSection,
        SocketsKeyValueSection,
        StatsKeyValueSection,
    ])

    EXTENSION = '.ot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@doc(append=AbstractKeyValueFileCache)
class OTFileCache(AbstractKeyValueFileCache):
    """
    Cache for OTFile instances.
    """
    FILE_TYPE = OTFile
