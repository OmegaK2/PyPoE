"""
Tests for PyPoE.poe.sim.mods

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/sim/test_mods.py                                 |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================



Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================

- Test for translation
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party
import pytest

# self
from PyPoE.poe.constants import MOD_DOMAIN, MOD_GENERATION_TYPE
from PyPoE.poe.file.dat import DatRecord
from PyPoE.poe.sim import mods

# =============================================================================
# Setup
# =============================================================================


class DatRecordOverride(DatRecord):
    keys = {
        'Id': '',
        'Level': 1,
        'Domain': 0,
        'GenerationType': 0,
        'CorrectGroup': '',
        'TagsKeys': [],
        'SpawnWeight_TagsKeys': [{'Id': 'default'}],
        'SpawnWeight_Values': [1000],
    }

    def __init__(self, **kwargs):

        self.data = {}

        self.data.update(self.keys)
        self.data.update(kwargs)

    def __getitem__(self, item):
        return self.data[item]

# =============================================================================
# Fixtures
# =============================================================================

# =============================================================================
# Tests
# =============================================================================


class TestGetModFromId:
    mod_list = [
        DatRecordOverride(
            Id='0',
        ),
    ]
    def test(self):
        assert self.mod_list[0] == mods.get_mod_from_id('0', self.mod_list)
        assert None == mods.get_mod_from_id('does_not_exist', self.mod_list)


class TestGetSpawnChanceCalculator:
    mod_list = [
        DatRecordOverride(
            Id='0',
            CorrectGroup='A',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.PREFIX.value,
        ),
        DatRecordOverride(
            Id='1',
            CorrectGroup='A',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.PREFIX.value,
        ),
        DatRecordOverride(
            Id='2',
            CorrectGroup='A',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.PREFIX.value,
        ),
        DatRecordOverride(
            Id='3',
            CorrectGroup='B',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.PREFIX.value,
        ),
        DatRecordOverride(
            Id='4',
            CorrectGroup='B',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.PREFIX.value,
            SpawnWeight_TagsKeys=[
                {'Id': 'nope'},
                {'Id': 'half'},
                {'Id': 'default'},
            ],
            SpawnWeight_Values=[
                0,
                500,
                1000,
            ]
        ),
    ]

    @pytest.fixture
    def scc(self):
        return {
            'nope': mods.SpawnChanceCalculator(self.mod_list, tags=['default', 'nope']),
            'half': mods.SpawnChanceCalculator(self.mod_list, tags=['default', 'half']),
            'default': mods.SpawnChanceCalculator(self.mod_list, tags=['default']),
        }

    def test_total_weight(self, scc):
        assert 5000 == scc['default'].get_total_spawn_weight()
        assert 4500 == scc['half'].get_total_spawn_weight()
        assert 4000 == scc['nope'].get_total_spawn_weight()

    def test_spawn_chance_no_remove(self, scc):
        assert 1000/5000 == scc['default'].spawn_chance('0', remove=False)
        assert 1000/4500 == scc['half'].spawn_chance('0', remove=False)
        assert 500/4500 == scc['half'].spawn_chance('4', remove=False)

    def test_spawn_chance_remove(self, scc):
        assert 1000/5000 == scc['default'].spawn_chance('0', remove=True)
        assert 1000/2000 == scc['default'].spawn_chance('3', remove=True)
        assert 0 == scc['default'].spawn_chance('0', remove=False)


class TestGetSpawnWeight:
    data = DatRecordOverride(
        SpawnWeight_TagsKeys=[
            {'Id': 'a'},
            {'Id': 'b'},
            {'Id': 'c'},
            {'Id': 'default'},
        ],
        SpawnWeight_Values=[
            1,
            2,
            3,
            1000,
        ],
    )
    
    def test_basic(self):
        assert 1000 == mods.get_spawn_weight(self.data, ['default', ])
        assert 1 == mods.get_spawn_weight(self.data, ['a', ])

    def test_order(self):
        assert 1 == mods.get_spawn_weight(self.data, ['a', 'default'])
        assert 1 == mods.get_spawn_weight(self.data, ['default', 'a'])
        assert 2 == mods.get_spawn_weight(self.data, ['b', 'c', 'default'])


class TestGenerateSpawnableModList:
    mod_list = [
        DatRecordOverride(
            Id='0',
            CorrectGroup='0',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.PREFIX.value,
        ),
        DatRecordOverride(
            Id='1',
            CorrectGroup='1',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.SUFFIX.value,
        ),
        DatRecordOverride(
            Id='2',
            CorrectGroup='2',
            Level=50,
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.PREFIX.value,
        ),
        # should never appear in any of the lists
        DatRecordOverride(
            Id='3',
            CorrectGroup='3',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.SUFFIX.value,
            SpawnWeight_Values=[0],
        ),
        # Should not appear unless specifically asked for
        DatRecordOverride(
            Id='4',
            CorrectGroup='4',
            Domain=MOD_DOMAIN.ITEM.value,
            GenerationTYpe=MOD_GENERATION_TYPE.SUFFIX.value,
            SpawnWeight_TagsKeys=[{'Id': 'different'}],
        ),
    ]
    
    def test_domain_and_generation_type(self):
        assert [] == mods.generate_spawnable_mod_list(
            self.mod_list,
            domain=MOD_DOMAIN.AREA,
            generation_type=MOD_GENERATION_TYPE.PREFIX,
        ), 'Got a list for something should not match anything'
        assert self.mod_list[1] == mods.generate_spawnable_mod_list(
            self.mod_list,
            domain=MOD_DOMAIN.ITEM,
            generation_type=MOD_GENERATION_TYPE.SUFFIX,
        ), 'Should have found only one match'

    def test_level(self):
        assert self.mod_list[2] == mods.generate_spawnable_mod_list(
            self.mod_list,
            domain=MOD_DOMAIN.ITEM,
            generation_type=MOD_GENERATION_TYPE.PREFIX,
            level=30,
        ), 'Should have found only one match'

    def test_tags(self):
        assert [] == mods.generate_spawnable_mod_list(
            self.mod_list,
            domain=MOD_DOMAIN.AREA,
            generation_type=MOD_GENERATION_TYPE.PREFIX,
            tags=['different'],
        ), 'Should have found only one match'