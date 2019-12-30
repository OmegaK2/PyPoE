"""
Utilities for dealing with monsters and related calculations.

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/sim/monster.py.                                        |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Utilities for dealing with monsters and related calculations.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

Internal API
-------------------------------------------------------------------------------
"""

# =============================================================================
# Imports
# =============================================================================

# Python
from collections.abc import Iterable

# 3rd-party

# self
from PyPoE.poe.constants import RARITY
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.poe.file.ot import OTFileCache

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class Monster:
    def __init__(self, parent, mv):
        self.parent = parent
        self._mv = mv
        self._mt = self.mv['MonsterTypesKey']
        self._res = self.mt['MonsterResistancesKey']
        self._ge = self.mv['GrantedEffectsKeys']
        self._gepl = [gepl for gepl in parent.rr['GrantedEffectsPerLevel.dat']
                     if gepl['GrantedEffectsKey'] == self._ge]
        self._mods = self.mv['ModsKeys']

        self._level = None

    @property
    def level(self):
        if self._level is None:
            raise ValueError('Set monster level first before performing actions'
                             ' that require monster level')
        return self._level

    @level.setter
    def level(self, value):
        if value < 1 or value > 100:
            raise ValueError('Monster level must be 1-100')
        self._level = value

    def damage(self, map_tier=None):
        base = self.parent.rr['DefaultMonsterStats.dat'][self.level]


class MonsterFactory:
    """
    Handler for monsters.
    """

    _files = [
        'DefaultMonsterStats.dat',
        # Loads mods, stats, granted effects, etc
        'MonsterVarieties.dat',
        'GrantedEffectsPerLevel.dat',
    ]

    rarity_mods = None

    def __init__(self, *args, relational_reader, otfile_cache, **kwargs):
        """

        Parameters
        ----------
        relational_reader : RelationalReader
            info
        otfile_cache : OTFileCache
            info
        """
        if isinstance(relational_reader, RelationalReader):
            self.rr = relational_reader
        else:
            raise ValueError('relational_reader must be a RelationalReader '
                             'instance')
        if isinstance(otfile_cache, OTFileCache):
            self.ot = otcache
        else:
            raise ValueError('otfile_cache must be a OTFileCache instance.')

        # Load files
        for fn in self._files:
            self.rr[fn]

        self.rarity_mods = {
            RARITY.NORMAL: [],
        }
        for mod in self.rr['Mods.dat']:
            if mod['Id'].startswith('MonsterMagic'):
                self.rarity_mods[RARITY.MAGIC] = mod
            elif mod['Id'].startswith('MonsterRare'):
                self.rarity_mods[RARITY.RARE] = mod
            elif mod['Id'].startswith('MonsterUnique'):
                self.rarity_mods[RARITY.UNIQUE] = mod

    def monster(self, rowid=None, metaid=None, name=None, *args, **kwargs):
        """
        Creates a list of Monster instances and returns them based on the
        passed search parameters.

        Parameters
        ----------
        rowid : int or Iterable[int]
            rowid or list of rowids to search for
        metaid : str or Iterable[str]
            Metadata id or list of metadata ids to search for
        name : str or Iterable[str]
            Name or list of monster names to search for
        args : Iterable
            Extra positional arguments to pass to the Monster instance
        kwargs : dict
            Extra keyword arguments to pass to the Monster instance

        Returns
        -------
        list[Monster]
            List of Monster instances.
        """
        if isinstance(rowid, int):
            mv = [self.rr['MonsterVarieties.dat'][rowid], ]
        elif isinstance(rowid, Iterable):
            mv = [self.rr['MonsterVarieties.dat'][rid] for rid in rowid]
        elif isinstance(metaid, str):
            mv = [self.rr['MonsterVarieties.dat'].index['Id'][metaid], ]
        elif isinstance(metaid, Iterable):
            mv = [self.rr['MonsterVarieties.dat'].index['Id'][mid] for mid
                  in metaid]
        elif isinstance(name, str):
            mv = [m for m in self.rr['MonsterVarieties.dat'] if
                  m['Name'] == name]
        elif isinstance(name, Iterable):
            mv = [m for m in self.rr['MonsterVarieties.dat'] if
                  m['Name'] in name]
        else:
            raise ValueError('One of rowid, metaid or name must be specified '
                             'and be of the correct type')

        return [Monster(
            *args,
            parent=self,
            mv=m,
            **kwargs
        ) for m in mv]

# =============================================================================
# Functions
# =============================================================================
