"""
Path     PyPoE/poe/sim/mods.py
Name     Utilities for Mods.dat
Version  1.0.0a0
Revision $Id$
Author   Omega_K2

IMPORTANT

This module is intended to be used with RelationReader.

INFO

Utilities for dealing with Mods.dat.


This module implements some generic functions to simplify dealing with Mods.dat
and perform several common tasks.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party

# self
from PyPoE.poe.file.dat import RecordList
from PyPoE.poe.file.translations import TranslationFileCache
from PyPoE.poe.constants import MOD_DOMAIN, MOD_GENERATION_TYPE

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'SpawnChanceCalculator',
    'generate_spawnable_mod_list',
    'get_mod_from_id',
    'get_spawn_weight',
    'get_translation',
]

_translation_map = {
    MOD_DOMAIN.MONSTER: 'monster_stat_descriptions.txt',
    MOD_DOMAIN.CHEST: 'chest_stat_descriptions.txt',
    MOD_DOMAIN.AREA: 'map_stat_descriptions.txt',
}

# =============================================================================
# Classes
# =============================================================================


class SpawnChanceCalculator(object):
    """
    Class to calculate spawn chances.
    """
    def __init__(self, mod_list, tags):
        """
        :param mod_list: The mod list to base the calculations on
        :type mod_list: list[RecordList]

        :param tags: List of tag identifiers
        :type tags: list[str]
        """
        self.mod_list = mod_list
        self.tags = tags
        self.total_spawn_weight = self.get_total_spawn_weight()

    def get_total_spawn_weight(self):
        total_spawn_weight = 0
        for mod in self.mod_list:
            total_spawn_weight += self.get_spawn_weight(mod)

        return total_spawn_weight

    def get_mod(self, modid):
        return get_mod_from_id(modid, self.mod_list)

    def get_spawn_weight(self, mod):
        return get_spawn_weight(mod, self.tags)

    def spawn_chance(self, mod_or_id, remove=True):
        """
        Calculates the spawn chance for the given mod based on the tags and the
        mod list given to this instance.

        If remove is specified the mod is also removed from the mod list.
        It is recommended to leave this option enabled, as it will take care of
        updating tags and mods of the same grouping, which will guarantee
        that future mods rolled on this instance will be calculated properly.

        :param mod_or_id: Id of the mod or the instance of the mod row
        :type mod_or_id: str or RecordList

        :param remove: Remove the mod from the list once the chance has been
        calcuated
        :type remove: bool

        :return: The calcuated spawn chance for the mod
        :rtype: float

        :raises TypeError: if mod_or_id has an invalid type
        :raises ValueError: if mod_or_id not found
        """
        if isinstance(mod_or_id, str):
            mod = self.get_mod(mod_or_id)
            if mod is None:
                return 0
        elif isinstance(mod_or_id, RecordList):
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

            for tag in mod['Tags']:
                self.tags.append(tag['Id'])

            self.total_spawn_weight = self.get_total_spawn_weight()
        return chance


# =============================================================================
# Functions
# =============================================================================


def get_translation(mod, translation_cache, translation_file=None):
    """
    Returns the Translation result of the stats found on the specified mod
    using the specified TranslationFileCache.

    :param mod:
    :type mod: RecordList

    :param translation_cache:
    :type translation_cache: TranslationFileCache

    :param translation_file:
    :type translation_file: str

    :return:
    :rtype: TranslationResult
    """
    stats = []
    for i in range(1, 6):
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
        try:
            tf_name = _translation_map[mod['Domain']]
        except KeyError:
            tf_name = 'stat_descriptions.txt'
    else:
        tf_name = translation_file

    return translation_cache[tf_name].get_translation(
        ids, values, full_result=True
    )


def get_mod_from_id(mod_id, mod_list):
    """
    Returns the mod for given mod or None if it isn't found.

    :param mod_id: The mod identifier to look for
    :type mod_id: str

    :param mod_list: List of mods to search in (or dat file)
    :type mod_list: list[RecordList]

    :return: Returns the mod if found, None otherwise
    :rtype: RecordList or None
    """
    for mod in mod_list:
        if mod['Id'] == mod_id:
            return mod
    return None


def get_spawn_weight(mod, tags):
    """
    Calculates the spawn weight of the given mod for the given tags.

    :param mod: The mod to calculate the spawn weight for.
    :type mod: RecordList

    :param tags: List of applicable tag identifiers.
    :type tags: list[str]

    :return: Calculated spawn weight
    :rtype: int
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

    :param mod_dat_file:
    :type mod_dat_file: `DatFile`

    :param domain: The mod domain
    :type domain: MOD_DOMAIN

    :param generation_type: The mod generation type
    :type generation_type: MOD_GENERATION_TYPE

    :param level: The level of object to the mod would be spawned on
    :type level: int

    :param tags: List of tags for this object
    :type tags: list[str]

    :return: Returns a list of applicable mod rows that have a spawn weighting
    above 0.
    :rtype: list[RecordList]

    :raises TypeError: if domain is not a valid MOD_DOMAIN constant
    :raises TypeError: if generation_type is not a valid MOD_GENERATION_TYPE
    constant
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



