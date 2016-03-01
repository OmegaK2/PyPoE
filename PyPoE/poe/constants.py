"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/constants.py                                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Global constants for Path of Exile, such as version or distributor for use in
the functions.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

.. autoclass:: VERSION

.. autoclass:: DISTRIBUTOR

.. autoclass:: SOCKET_COLOUR

.. autoclass:: RARITY

.. autoclass:: MOD_DOMAIN

.. autoclass:: MOD_GENERATION_TYPE

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
    'RARITY',
    'MOD_DOMAIN',
    'MOD_GENERATION_TYPE'
]

# =============================================================================
# Classes
# =============================================================================


class VERSION(IntEnum):
    """
    Used to differentiate between the different release versions of the game,
    i.e. between delpoyment (live/stable) version and temporary betas for
    example.

    This constant is primarily virtual and has no direct relevance to the game
    files, but it is used in context of accounting for differences between the
    released versions of available Path of Exile clients.

    Attributes
    ----------
    STABLE
        The stable version of Path of Exile. This will refer to the currently
        playable, public version.
    BETA
        Beta version of Path of Exile.
        As of currently, there is no beta running and this was only used
        for the Awakening Beta.
    ALPHA
        Alpha version of Path of Exile.
    ALL
        All registered version types.
    DEFAULT
        Default version (i.e. stable variants). For most use cases this is the
        preferred and default selection.

    """
    STABLE = 1
    BETA = 2
    ALPHA = 4

    ALL = STABLE | BETA | ALPHA

    DEFAULT = STABLE


class DISTRIBUTOR(IntEnum):
    """
    Used to differentiate between the different distributors of the clients.

    This constant is primarily virtual and has no direct relevance to the game
    files, but it is used in context of accounting for differences between the
    released versions of available Path of Exile clients.

    Attributes
    ----------
    GGG
        The standalone client
    STEAM
        The international steam client
    GARENA
        Garena client
    INTERNATIONAL
        The international client(s). This generally refers to the clients
        GGG is maintaining itself and share the same realm (i.e. currently
        the standalone and steam client)
    ALL
        All clients
    DEFAULT
        Default selection for clients, i.e. all.
    """
    GGG = 1
    STEAM = 2
    GARENA = 4

    INTERNATIONAL = GGG | STEAM

    ALL = GGG | STEAM | GARENA

    DEFAULT = ALL


class SOCKET_COLOUR(Enum):
    """
    Representation of item socket colours.

    In some places in the game files these colours are referenced either by
    their id or by a character, so make sure to check which and use the
    according attribute.

    Attributes
    ----------
    RED : SOCKET_COLOUR
        Red sockets usually associated with Strength
    GREEN : SOCKET_COLOUR
        Green sockets usually associated with Dexterity
    BLUE : SOCKET_COLOUR
        Blue sockets usually associated with Intelligence
    WHITE : SOCKET_COLOUR
        White sockets
    char : str
        When accessing a :class:`SOCKET_COLOUR` instance (i.e.
        :attr:`SOCKET_COLOUR.BLUE`) the char attribute denotes the character
        that is sometimes used in the game files to represent the colour
    id : int
        When accessing a :class:`SOCKET_COLOUR` instance (i.e.
        :attr:`SOCKET_COLOUR.BLUE`) the id attribute denotes the integer
        that is sometimes used in the game files to represent the colour
    """
    # IDs are from CharacterStarItems.dat->Sockets and game testing
    R = ('R', 1)
    G = ('G', 2)
    B = ('B', 3)
    # I can't actually confirm this id=4, but seems logical
    W = ('W', 4)
    RED = R
    GREEN = G
    BLUE = B
    WHITE = W

    def __init__(self, char, id):
        self.char = char
        self.id = id


class RARITY(Enum):
    """
    Representation of the possible rarities for items and monsters.

    Attributes
    ----------
    NORMAL : RARITY
        Normal rarity ("white" colour)
    MAGIC : RARITY
        Magic rarity ("blue" colour)
    RARE : RARITY
        Rare rarity ("yellow" colour)
    UNIQUE : RARITY
        Unique rarity ("brown" colour)
    id : int
        When accessing a :class:`RARITY` instance (e.x. :attr:`RARITY.NORMAL`)
        the id attribute denotes the integer that is sometimes used in the game
        files to represent the colour
    upper : str
        When accessing a :class:`RARITY` instance (e.x. :attr:`RARITY.NORMAL`)
        the upper attribute represents the textual representation with an upper
        case starting letter
    lower : str
        When accessing a :class:`RARITY` instance (e.x. :attr:`RARITY.NORMAL`)
        the lower attribute represents the textual representation with an lower
        case starting letter
    colour : str
        When accessing a :class:`RARITY` instance (e.x. :attr:`RARITY.NORMAL`)
        the colour attribute represents the textual representation of the
        associated colour
    """
    NORMAL = (1, 'Normal', 'normal', 'white')
    MAGIC = (2, 'Magic', 'magic', 'blue')
    RARE = (3, 'Rare', 'rare', 'yellow')
    UNIQUE = (4, 'Unique', 'unique', 'brown')

    def __init__(self, id, upper, lower, colour):
        self.id = id
        self.name_upper = upper
        self.name_lower = lower
        self.colour = colour


class MOD_DOMAIN(IntEnum):
    """
    Representation of mod domains.

    This constant is primarily used in relation to Mods.dat.

    Attributes
    ----------
    ITEM
        Generic item domain (but excluding items that have their own domain)
    FLASK
        Flask domain
    MONSTER
        Monster domain
    CHEST
        Chest domain, i.e. strongboxes or other type of chest-like
        containers
    AREA
        Area domain, i.e. for the various zones of Path of Exile
    UNKNOWN1
    UNKNOWN2
    UNKNOWN3
    STANCE
        Stance domain, i.e. animation related stance of objects
    MASTER
        Master domain for Forsaken Master related mods, in particular for
        master crafting mods
    JEWEL
        Jewel domain for things that appear on jewel items
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

    This constant is primarily used in relation to Mods.dat.

    PREFIX
        Prefix generation type
    SUFFIX
        Suffix generation type
    UNIQUE
        Whether the mod is directly given to an entity and not generanted by
        normal means.
        Commonly this can be found on unique monsters/items for example, but
        also as innate/implicit modifiers for example
    NEMESIS
        For 'nemesis' mods that can appear on monsters
    CORRUPTED
        For mods that are generated though item corruption
    BLOODLINES
        For 'bloodlines' mods that can appear on monsters
    TORMENT
        For 'torment' mods that can appear on monsters
    TEMPEST
        For 'tempest' mods that can appear on areas
    TALISMAN
        For 'talisman' mods that can appear on monsters
    ENCHANTMENT
        For the ascendancy/labyrinth enchantment mods that can appear on items

    """
    PREFIX = 1
    SUFFIX = 2
    UNIQUE = 3
    NEMESIS = 4
    CORRUPTED = 5
    BLOODLINES = 6
    TORMENT = 7
    TEMPEST = 8
    TALISMAN = 9
    ENCHANTMENT = 10

# =============================================================================
# Functions
# =============================================================================
