"""
Path     PyPoE/tests/poe/file/test_translations.py
Name     Tests for PyPoE.poe.file.translations
Version  1.0.0a0
Revision $Id$
Author   [#OMEGA]- K2

INFO

Tests for translations.py


AGREEMENT

See PyPoE/LICENSE


TODO

- Tests for the individual classes and functions, not just the results
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd Party
import pytest

# self
from PyPoE.poe.file import translations

# =============================================================================
# Setup
# =============================================================================

cur_dir = os.path.split(os.path.realpath(__file__))[0]
data_dir = os.path.join(cur_dir, '_data')
dbase_path = os.path.join(data_dir, 'Metadata', 'descriptions_base.txt')
dextended_path = os.path.join(data_dir, 'Metadata', 'descriptions_extended.txt')

data = {
    'base': (
        # Size, Unique ID,  values
        (1, 1, ((1, ), )),
        (1, 2, ((40, ), (1, ))),
        (2, 1, ((1, 99), (99, 1), (99, 99))),
        (3, 1, ((50, 1, 1), (100, 1, 1))),
    ),
    'quantifier': (

    ),
}

# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def dbase():
    return translations.TranslationFile(dbase_path)

@pytest.fixture
def dextended():
    return translations.TranslationFile(dextended_path, base_dir=data_dir)

@pytest.fixture
def tcache():
    return translations.TranslationFileCache(data_dir)

def get_test(size, unid, nresults, values):
    tags = ['tag_size%s_uq%s_no%s' % (size, unid, i) for i in range(1, size+1)]
    results = ['tag_size%s_uq%s_v%s:%s' % (size, unid, i, ' %s'*size) for i in range(1, nresults+1)]

    for i, v in enumerate(results):
        results[i] = v % values[i]

    return tags, results

# =============================================================================
# Tests
# =============================================================================

class TestTranslation:
    def build_base_string_data(self):
        test_data = []
        for size, unique_id, values in data['base']:
            tags, results = get_test(size, unique_id, len(values), values)
            for i, v in enumerate(values):
                test_data.append((tags, v, results[i]))

        return test_data

    def test_read(self, dbase):
        pass

    def test_read_with_include(self, dextended):
        pass

    @pytest.mark.parametrize('tags,values,result', build_base_string_data(None))
    def test_base_strings(self, dbase, tags, values, result):
        assert dbase.get_translation(tags, values)[0] == result

class TestTranslationFileCache:
    def test_init(self, tcache):
        pass

    def test_get_file(self, tcache, dbase, dextended):
        assert tcache.get_file('Metadata/descriptions_base.txt') == dbase, 'Files should be identical'
        assert tcache.get_file('Metadata/descriptions_extended.txt') == dextended, 'Files should be identical'

    def test_getitem(self, tcache, dbase, dextended):
        assert tcache['descriptions_base.txt'] == dbase, 'Files should be identical'
        assert tcache['descriptions_extended.txt'] == dextended, 'Files should be identical'

    def test_is_cache_working(self, tcache):
        a = tcache['descriptions_extended.txt']
        # Should have cached the included file
        tcache._files['Metadata/descriptions_base.txt']

        assert tcache['descriptions_extended.txt'] is a, 'Cache should return identical object'


'''def test_tag1_value1():
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
    _expected_result_assert(t, values)'''