"""
Path     PyPoE/tests/poe/file/test_ggpk.py
Name     Tests for PyPoE.poe.file.ggpk
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Tests for ggpk.py


AGREEMENT

See PyPoE/LICENSE


TODO

- Tests for the individual classes and functions, not just the results
- Make a fake description/dat file for testing purposes instead of using real
one
"""

# =============================================================================
# Imports
# =============================================================================

# self
from PyPoE.poe.file import translations

# =============================================================================
# Setup
# =============================================================================

s = translations.DescriptionFile('C:/Temp/stat_descriptions.txt')

# =============================================================================
# Tests
# =============================================================================

def _expected_result_assert(t, values):
    for k in values:
        v = values[k]
        assert k != s.get_translation(t, v)

def test_tag1_value1():
    t = ['life_regeneration_rate_+%']
    values = {
        'life_regeneration_rate_+%': [-2, ],
    }
    _expected_result_assert(t, values)

def test_tag2_value2():
    t = ['minimum_added_fire_damage_per_active_buff', 'maximum_added_fire_damage_per_active_buff']
    values = {
        'Adds 1 maximum Fire Damage per Buff on You': [0, 1],
        'Adds 1 minimum Fire Damage per Buff on You': [1, 0],
        'Adds 1-1 Fire Damage per Buff on You': [1, 1],
    }
    _expected_result_assert(t, values)

def test_tag2_value1():
    t = ['base_chance_to_freeze_%']
    values = {
        '50% chance to Freeze': [50, ],
        '99% chance to Freeze': [99,],
        'Always Freeze': [100,],
    }
    _expected_result_assert(t, values)