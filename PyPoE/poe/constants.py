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

.. autoclass:: WORDLISTS

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
    'MOD_GENERATION_TYPE',
    'WORDLISTS',

    'MOD_MAX_STATS',
    'MOD_STATS_RANGE',
]

MOD_MAX_STATS = 6
MOD_STATS_RANGE = range(1, MOD_MAX_STATS+1)

# =============================================================================
# Classes
# =============================================================================


'''class ACTIVE_SKILL_TARGET_TYPES(IntEnum):
    """

    Attributes
    ----------
    TARGETABLE_GROUND
        Can target the ground as long it's targetable
    ENEMY
        Can target an enemy
    WALKABLE_GROUND
        Can/must target ground that is walkable (seems to be used for teleport
        skills)
    ANYWHERE_SELF_TARGET
        Targets anywhere; used for aura/self-targeting skills
    ITEM
        Targets an item
    CORPSE
        Targets a corpse
    NO_LINE_OF_SIGHT
        Targets even without line of sight
    BEHIND_MONSTER
        Targets behind monster
    SELF_ORIGIN
        Treats the entity as origin for the skill
    ROTATE_TO_TARGET
        Rotates to the target while using the skill (i.e. for channeled skills)
    """
    TARGETABLE_GROUND = 1
    ENEMY = 2
    WALKABLE_GROUND = 3
    ANYWHERE_SELF_TARGET = 4
    ITEM = 5
    CORPSE = 6
    UNUSED1 = 7
    NO_LINE_OF_SIGHT = 8
    BEHIND_MONSTER = 9
    SELF_ORIGIN = 10
    ROTATE_TO_TARGET = 11
    # Shrine and totem npc stuff
    UNKNOWN1 = 12
    # Animate Weapon only
    UNKNOWN2 = 13
    # Proximity Shield
    UNKNOWN3 = 14
    # Some monster skills
    UNKNOWN4 = 15
    # Jump to target? Monster skills.
    UNKNOWN5 = 16
    UNUSED2 = 17
    # 18 and 19 both Scorching Ray only
    UNKNOWN6 = 18
    UNKNOWN7 = 19


class ACTIVE_SKILL_TYPES(IntEnum):
    """
    Attributes
    ----------
    ATTACK
        Is an attack and uses the weapons on the entity
    CAST
        Is casted and does not use the weapon
    PROJECTILE
        Creates an projectile
    DUALWIELD_ONLY
        Uses both hand slots
    BUFF_SELF
        Buff that applies to the entity itself
    """
    ATTACK = 1
    CAST = 2
    PROJECTILE = 3
    # Why is a monster being dual-wield only?
    DUALWIELD_ONLY = 4
    BUFF_SELF = 5
    #DUALWIELD_POSSIBLE = 6'''
    

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


class SHOP_PACKAGE_PLATFORM(IntEnum):
    """
    ShopPackagePlatform.dat

    Attributes
    ----------
    PC
        PC
    XBOX
        Microsoft XBox
    """
    PC = 1
    XBOX = 2


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

    def __new__(cls, char, id):
        obj = object.__new__(cls)
        obj._value_ = char
        obj.char = char
        obj.id = id

        return obj


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
    ANY : RARITY
        Any rarity
    id : int
        When accessing a :class:`RARITY` instance (e.x. :attr:`RARITY.NORMAL`)
        the id attribute denotes the integer that is sometimes used in the game
        files to represent the colour
    name_upper : str
        When accessing a :class:`RARITY` instance (e.x. :attr:`RARITY.NORMAL`)
        the upper attribute represents the textual representation with an upper
        case starting letter
    name_lower : str
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
    ANY = (5, 'Any', 'any', 'any')

    def __new__(cls, id, upper, lower, colour):
        obj = object.__new__(cls)
        obj._value_ = id
        obj.id = id
        obj.name_upper = upper
        obj.name_lower = lower
        obj.colour = colour
        return obj


class MAP_ITERATION(IntEnum):
    """
    Representation of map iterations

    Attributes
    ----------
    LEGACY
        Maps prior to Awakening (2.0)
    SQUARE
        Maps after Awakening (2.0), but before Atlas of Worlds (2.4)
    ATLAS
        Maps since Atlas of Worlds update (2.4)
    """

    LEGACY = 1
    SQUARE = 2
    ATLAS = 3

    ROUND = ATLAS


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
        Jewel domain for modifiers that appear on jewel items
    ATLAS
        Atlas domain for modifiers that appear when using a sextant orb on the
        atlas
    LEAGUESTONE
        Leaguestone domain for modifiers that appear on league stones
    ABYSS_JEWEL
        Domain for modifiers that appear on Abyss jewels
    MAP_DEVICE
        For implicit modifiers that can be applied through the map device
        For example, vaal fragments or soul flasks
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
    ATLAS = 12
    LEAGUESTONE = 13
    ABYSS_JEWEL = 14
    MAP_DEVICE = 15


class MOD_GENERATION_TYPE(IntEnum):
    """
    Representation of mod generation types.

    This constant is primarily used in relation to Mods.dat.

    Attributes
    ----------
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
    ESSENCE
        For 'essence' mods that can appear on monsters

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
    ESSENCE = 11
    BESTIARY = 13


class WORDLISTS(IntEnum):
    """
    Representation of words lists ( Wordlists.dat )

    This constant is primarily used in relation to Words.dat

    Attributes
    ----------
    ITEM_PREFIX
        Prefix word of a randomly generated item name
    ITEM_SUFFIX
        Suffix word of a randomly generated item name; separate from the prefix
    MONSTER_PREFIX
        Prefix word of a randomly generated monster name.
    MONSTER_SUFFIX
        Suffix word of a randomly generated monster name; composite with the
        prefix
    MONSTER_TITLE
        Title ("the xxx") of a randomly generated monster name
    UNIQUE_ITEM
        Name of a unique item
    STRONGBOX_PREFIX
        Prefix word of a randomly generated strongbox name
    STRONGBOG_SUFFIX
        Suffix word of a randomly generated strongbox name; separate from the
        prefix
    ESSENCE
        Name of an essence
    """
    ITEM_PREFIX = 1
    ITEM_SUFFIX = 2
    MONSTER_PREFIX = 3
    MONSTER_SUFFIX = 4
    MONSTER_TITLE = 5
    UNIQUE_ITEM = 6
    STRONGBOX_PREFIX = 7
    STRONGBOX_SUFFIX = 8
    ESSENCE = 9

# =============================================================================
# Functions
# =============================================================================
