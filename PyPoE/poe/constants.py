"""
Constants

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/constants.py                                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Global constants for Path of Exile, such as version or distributor for use in
the functions.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python

from enum import IntEnum, Enum

# 3rd-party

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'DISTRIBUTOR',
    'VERSION',
    'SOCKET_COLOUR',
    'ITEM_RARITY',
    'MOD_DOMAIN',
    'MOD_GENERATION_TYPE'
]

# =============================================================================
# Classes
# =============================================================================


class VERSION(IntEnum):
    STABLE = 1
    BETA = 2

    ALL = STABLE | BETA

    DEFAULT = STABLE


class DISTRIBUTOR(IntEnum):
    GGG = 1
    STEAM = 2
    GARENA = 4

    INTERNATIONAL = GGG | STEAM

    ALL = GGG | STEAM | GARENA

    DEFAULT = ALL

class SOCKET_COLOUR(Enum):
    """
    Representation of socket colours
    """
    R = 'R'
    G = 'G'
    B = 'B'
    W = 'W'
    RED = R
    GREEN = G
    BLUE = B
    WHITE = W


class ITEM_RARITY(Enum):
    """
    Representation of the possible item rarities.
    """
    NORMAL = (1, 'Normal', 'normal')
    MAGIC = (2, 'Magic', 'magic')
    RARE = (3, 'Rare', 'rare')
    UNIQUE = (4, 'Unique', 'unique')

    def __init__(self, id, upper, lower):
        self.id = id
        self.name_upper = upper
        self.name_lower = lower

class MOD_DOMAIN(IntEnum):
    """
    Representation of mod domains.
    """
    ITEM = 1
    FLASK = 2
    MONSTER = 3
    CHEST = 4
    AREA = 5
    UNKNOWN1 = 6
    UNKNOWN2 = 7
    UNKNOWN3 = 8
    STANCE = 9
    MASTER = 10
    JEWEL = 11


class MOD_GENERATION_TYPE(IntEnum):
    """
    Representation of mod generation types.
    """
    PREFIX = 1
    SUFFIX = 2
    UNIQUE = 3
    NEMESIS = 4
    CORRUPTED = 5
    BLOODLINES = 6
    TORMENT = 7
    TEMPEST = 8

# =============================================================================
# Functions
# =============================================================================
