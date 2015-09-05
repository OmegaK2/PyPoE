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

__all__ = ['DISTRIBUTOR', 'VERSION']

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

# =============================================================================
# Functions
# =============================================================================
