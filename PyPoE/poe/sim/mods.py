"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/sim/mods.py                                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Utilities for dealing with Mods.dat.

This module implements some generic functions to simplify dealing with Mods.dat
and perform several common tasks.

.. warning::
    This module is intended to be used with
    :class:`PyPoE.poe.file.dat.RelationalReader`.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

.. autoclass:: SpawnChanceCalculator
    :special-members: __init__

.. autofunction:: get_translation
.. autofunction:: get_translation_file_from_domain
.. autofunction:: get_mod_from_id
.. autofunction:: get_spawn_weight
.. autofunction:: generate_spawnable_mod_list

"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party

# self
from PyPoE.poe.file.dat import DatRecord
from PyPoE.poe.file.translations import TranslationFileCache
from PyPoE.poe.constants import MOD_DOMAIN, MOD_GENERATION_TYPE, MOD_STATS_RANGE

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'SpawnChanceCalculator',
    'generate_spawnable_mod_list',
    'get_mod_from_id',
    'get_spawn_weight',
    'get_translation',
    'get_translation_file_from_domain',
]

_translation_map = {
    MOD_DOMAIN.MONSTER: 'monster_stat_descriptions.txt',
    MOD_DOMAIN.CHEST: 'chest_stat_descriptions.txt',
    MOD_DOMAIN.AREA: 'map_stat_descriptions.txt',
    MOD_DOMAIN.ATLAS: 'atlas_stat_descriptions.txt',
    MOD_DOMAIN.LEAGUESTONE: 'leaguestone_stat_descriptions.txt',
    MOD_DOMAIN.DELVE_AREA: 'map_stat_descriptions.txt',
    MOD_DOMAIN.MAP_DEVICE: 'map_stat_descriptions.txt',
    # To properly support zana's innate IIQ
    MOD_DOMAIN.CRAFTED: 'map_stat_descriptions.txt',
}

# =============================================================================
# Classes
# =============================================================================


class SpawnChanceCalculator:
    """
    Class to calculate spawn chances.
    """
    def __init__(self, mod_list, tags):
        """
        Parameters
        ----------
        mod_list : list[DatRecord]
            The mod list to base the calculations on
        tags : list[str]
            List of tag identifiers
        """
        self.mod_list = mod_list
        self.tags = tags
        self.total_spawn_weight = self.get_total_spawn_weight()

    def get_total_spawn_weight(self):
        """
        Calculate the total spawn weight based on the stored modifier list

        Returns
        -------
        int
            Sum of spawn weights
        """
        total_spawn_weight = 0
        for mod in self.mod_list:
            total_spawn_weight += self.get_spawn_weight(mod)

        return total_spawn_weight

    def get_mod(self, mod_id):
        """
        Returns the mod for the specified mod id based on the stored modifier
        list or None if it isn't found.

        Parameters
        ----------
        mod_id : str
            The mod identifier to look for

        Returns
        -------
        DatRecord or None
            Returns the mod if found, None otherwise

        See Also
        --------
        :func:`get_mod_from_id`
        """
        return get_mod_from_id(mod_id, self.mod_list)

    def get_spawn_weight(self, mod):
        """
        Calculates the spawn weight of the given mod based on the stored list
        of tags.

        Parameters
        ----------
        mod : DatRecord
            The mod to calculate the spawn weight for.
        tags : list[str]
            List of applicable tag identifiers.


        Returns
        -------
        int
            Calculated spawn weight

        See Also
        --------
        :func:`get_spawn_weight`

        """
        return get_spawn_weight(mod, self.tags)

    def spawn_chance(self, mod_or_id, remove=True):
        """
        Calculates the spawn chance for the given mod based on the tags and the
        mod list given to this instance.

        If remove is specified the mod is also removed from the mod list.
        It is recommended to leave this option enabled, as it will take care of
        updating tags and mods of the same grouping, which will guarantee
        that future mods rolled on this instance will be calculated properly.

        Parameters
        ----------
        mod_or_id : str | DatRecord
            Id of the mod or the instance of the mod row
        remove : bool
            Remove the mod from the list once the chance has been calculated


        Returns
        -------
        float
            The calculated spawn chance for the mod


        Raises
        ------
        TypeError
            if mod_or_id has an invalid type
        ValueError
            if mod_or_id not found
        """
        if isinstance(mod_or_id, str):
            mod = self.get_mod(mod_or_id)
            if mod is None:
                return 0
        elif isinstance(mod_or_id, DatRecord):
            mod = mod_or_id
        else:
            raise TypeError(
                'mod_or_id is of invalid type "%s"' % type(mod_or_id)
            )

        weight = self.get_spawn_weight(mod)
        chance = weight/self.total_spawn_weight

        if remove:
            mods = []

            for m in self.mod_list:
                if m['CorrectGroup'] == mod['CorrectGroup']:
                    continue

                mods.append(m)

            self.mod_list = mods

            for tag in mod['TagsKeys']:
                self.tags.append(tag['Id'])

            self.total_spawn_weight = self.get_total_spawn_weight()
        return chance


# =============================================================================
# Functions
# =============================================================================

def get_translation_file_from_domain(domain):
    """
    Returns the likely stat translation file for a given mod domain.

    Parameters
    ----------
    domain : int
        Id of the domain

    Returns
    -------
    str
        name of the stat translation file
    """
    try:
        return _translation_map[domain]
    except KeyError:
        return 'stat_descriptions.txt'


def get_translation(mod, translation_cache, translation_file=None, **kwargs):
    """
    Returns the Translation result of the stats found on the specified mod
    using the specified TranslationFileCache.

    Parameters
    ----------
    mod : DatRecord

    translation_cache : TranslationFileCache
        :class:`PyPoE.poe.file.TranslationCache` instance to retrieve the
        translation file from.

    translation_file : str
        Name of the translation file to use. If left empty, it will be
        automatically determined based on the mod domain.

    Returns
    -------
    TranslationResult

    """
    stats = []
    for i in MOD_STATS_RANGE:
        stat = mod['StatsKey%s' % i]
        if stat:
            stats.append(stat)

    ids = []
    values = []
    for i, stat in enumerate(stats):
        j = i + 1
        values.append([mod['Stat%sMin' % j], mod['Stat%sMax' % j]])
        ids.append(stat['Id'])

    if translation_file is None:
        tf_name = get_translation_file_from_domain(mod['Domain'])
    else:
        tf_name = translation_file

    return translation_cache[tf_name].get_translation(
        ids, values, full_result=True, **kwargs
    )


def get_mod_from_id(mod_id, mod_list):
    """
    Returns the mod for given mod or None if it isn't found.

    Parameters
    ----------
    mod_id : str
        The mod identifier to look for
    mod_list : list[DatRecord]
        List of mods to search in (or dat file)


    Returns
    -------
    DatRecord or None
        Returns the mod if found, None otherwise
    """
    for mod in mod_list:
        if mod['Id'] == mod_id:
            return mod
    return None


def get_spawn_weight(mod, tags):
    """
    Calculates the spawn weight of the given mod for the given tags.

    Parameters
    ----------
    mod : DatRecord
        The mod to calculate the spawn weight for.
    tags : list[str]
        List of applicable tag identifiers.


    Returns
    -------
    int
        Calculated spawn weight
    """
    current_weight = 0
    for i, tag in enumerate(mod['SpawnWeight_TagsKeys']):
        weight = mod['SpawnWeight_Values'][i]
        if tag['Id'] in tags:
            current_weight = weight
            break

    return current_weight


def generate_spawnable_mod_list(
        mod_dat_file,
        domain,
        generation_type,
        level=1,
        tags=['default', ]
        ):
    """
    Generates a list of modifiers that can be spawned for the specified
    parameters, i.e. mods that can not spawn will be removed.

    TODO: Certain generation types/domains may have different rules.

    Parameters
    ----------
    mod_dat_file : `DatFile`

    domain : MOD_DOMAIN
        The mod domain
    generation_type : MOD_GENERATION_TYPE
        The mod generation type
    level : int
        The level of object to the mod would be spawned on
    tags : list[str]
        List of tags for this object


    Returns
    -------
    list[DatRecord]
        Returns a list of applicable mod rows that have a spawn weighting
        above 0.


    Raises
    ------
    TypeError
        if domain is not a valid MOD_DOMAIN constant
        if generation_type is not a valid MOD_GENERATION_TYPE constant
    """
    if not isinstance(domain, MOD_DOMAIN):
        raise TypeError('domain must be a MOD_DOMAIN instance.')

    if not isinstance(generation_type, MOD_GENERATION_TYPE):
        raise TypeError(
            'generation_type must be a MOD_GENERATION_TYPE instance.'
        )

    mods = []
    for mod in mod_dat_file:
        if level < mod['Level']:
            continue

        if mod['Domain'] != domain:
            continue

        if mod['GenerationType'] != generation_type:
            continue

        # Mod can't spawn
        if get_spawn_weight(mod, tags) == 0:
            continue

        mods.append(mod)

    return mods



