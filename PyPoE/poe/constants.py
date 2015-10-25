"""
Path     PyPoE/poe/constants.py
Name     Constants
Version  1.0.0a0
Revision $Id$
Author   Omega_K2

INFO

Global constants for Path of Exile, such as version or distributor for use in
the functions.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python

from enum import IntEnum

# 3rd-party

# self

# =============================================================================
# Globals
# =============================================================================

__all__ = ['DISTRIBUTOR', 'VERSION', 'MOD_DOMAIN', 'MOD_GENERATION_TYPE']

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
