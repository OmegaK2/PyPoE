"""
Tests for PyPoE.poe.file.translations

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/file/test_translations.py                        |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for translations.py

Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================

- Tests for the individual classes and functions, not just the results
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from collections import OrderedDict

# 3rd Party
import pytest

# self
from PyPoE.poe.file import translations

# =============================================================================
# Setup
# =============================================================================

cur_dir = os.path.split(os.path.realpath(__file__))[0]
data_dir = os.path.join(cur_dir, '_data')
dbase_path = os.path.join(data_dir, 'Metadata', 'StatDescriptions',
                          'descriptions_base.txt')
dextended_path = os.path.join(data_dir, 'Metadata', 'StatDescriptions',
                              'descriptions_extended.txt')

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope='module')
def dbase():
    tf = translations.TranslationFile()
    tf.read(dbase_path)
    return tf


@pytest.fixture(scope='module')
def dextended():
    tf = translations.TranslationFile(base_dir=data_dir)
    tf.read(dextended_path)
    return tf


@pytest.fixture(scope='module')
def tcache():
    return translations.TranslationFileCache(
        path_or_file_system=data_dir,
    )


@pytest.fixture(scope='module')
def ggpk_tc(file_system):
    return translations.TranslationFileCache(
        path_or_file_system=file_system,
    )


@pytest.fixture(scope='module')
def tf_data(rr):
    translations.install_data_dependant_quantifiers(rr)
    tf = translations.TranslationFile()
    tf.read(dbase_path)
    return tf


@pytest.fixture(scope='module')
def ts(dbase):
    t = dbase.translations_hash['test_multiple_values'][0]
    tl = t.get_language('English')
    # This only has one entry
    return tl.strings[0]


def get_test(size, unid, nresults, values):
    tags = ['tag_size%s_uq%s_no%s' % (size, unid, i) for i in range(1, size+1)]
    results = ['tag_size%s_uq%s_v%s:%s' % (size, unid, i, ' %s'*size)
               for i in range(1, nresults+1)]

    for i, v in enumerate(results):
        results[i] = v % values[i]

    return tags, results

# =============================================================================
# Tests
# =============================================================================


# Move it up here so install_data_dependant_quantifiers doesn't mess this test
# up
class TestTranslationFileCache:
    def test_init(self, tcache):
        pass

    def test_get_file(self, tcache, dbase, dextended):
        assert tcache.get_file(
            'Metadata/StatDescriptions/descriptions_base.txt') == dbase, \
            'Files should be identical'
        assert tcache.get_file(
            'Metadata/StatDescriptions/descriptions_extended.txt') == \
            dextended, 'Files should be identical'

    def test_getitem(self, tcache, dbase, dextended):
        assert tcache['descriptions_base.txt'] == dbase, \
            'Files should be identical'
        assert tcache['descriptions_extended.txt'] == dextended, \
            'Files should be identical'

    def test_is_cache_working(self, tcache):
        a = tcache['descriptions_extended.txt']
        # Should have cached the included file
        tcache.files['Metadata/StatDescriptions/descriptions_base.txt']

        assert tcache['descriptions_extended.txt'] is a, \
            'Cache should return identical object'


class TestTranslationResults:
    #
    # Data for this section
    #
    data = {
        'base': (
            # Size, Unique ID,  values
            (1, 1, ((1, ), )),
            (1, 2, ((40, ), (1, ))),
            (1, 3, ((1, ), )),
            (1, 4, ((1, ), )),
            (2, 1, ((1, 99), (99, 1), (99, 99))),
            (3, 1, ((50, 1, 1), (100, 1, 1))),
        ),
        'quantifier': (

        ),
    }

    functionality_tests = (
        # Tags, values, result, message, trr, reverse keyargs
        (
            ['tag_size1_uq1_no1', ],
            [1.0, ],
            ['tag_size1_uq1_v1: 1'],
            'Test whole float: 1.0 -> 1',
            {},
            {},
        ),
        (
            ['tag_size1_uq1_no1', ],
            [0, ],
            [],
            'Zero stat values',
            {},
            None,
        ),
        (
            ['tag_size1_uq1_no1', ],
            [(0, 30), ],
            ['tag_size1_uq1_v1: (0-30)'],
            'Zero stat value as range minimum',
            {},
            None,
        ),
        (
            ['tag_size1_uq1_no1', ],
            [(-30, 0), ],
            ['tag_size1_uq1_v1: (-30-0)'],
            'Zero stat value as range maximum',
            {},
            None,
        ),
        (
            ['tag_size1_uq1_no1', ],
            [(-40, -30), ],
            ['tag_size1_uq1_v1: -(40-30)'],
            'Test double negative range fixup',
            {},
            None,
        ),
        (
            ['tag_skip_size2_uq1_no1', 'tag_skip_size2_uq1_no2'],
            [1, 50],
            ['tag_skip_size2_uq1_v1: 50'],
            'Value skip',
            {},
            {},
        ),
        (
            ['test_not_body', 'test_not'],
            [50, 0],
            ['Not value fails: 50'],
            'Not test: Testing !0==0',
            {},
            {},
        ),
        (
            ['test_not_body', 'test_not'],
            [50, 1],
            ['Not value succeeds: 50'],
            'Not test: Testing !0==1',
            {},
            {},
        ),
        (
            ['test_plus', ],
            [20, ],
            ['Plus: +20'],
            '$+d format',
            {},
            {},
        ),
        (
            ['test_plus', ],
            [-20, ],
            ['Plus: -20'],
            '$+d format with negative value',
            {},
            {},
        ),
        # Used in skills like hypothermia
        (
            ['test_dollar_d', ],
            [20, ],
            ['Test d: 20'],
            '%1$d format',
            {},
            {},
        ),
        (
            ['test_multiple_values', 'test_multiple_values2'],
            [42, 1337],
            ['Multiple: 42 1337 42 1337'],
            'multiple values',
            {},
            {},
        ),
        (
            ['test_value_not_in_range', ],
            [0, ],
            [],
            'value not in range',
            {},
            None,
        ),
        (
            ['test_placeholder1', 'test_placeholder2', 'test_placeholder3',
             'test_placeholder4'],
            [50, 100, 150, 200],
            ['Placeholder: x y z A'],
            'placeholder',
            {
                'use_placeholder': True,
            },
            None,
        ),
        (
            ['test_placeholder1', 'test_placeholder2', 'test_placeholder3',
             'test_placeholder4'],
            [50, 100, 150, 200],
            ['Placeholder: 2 4 6 8'],
            'placeholder',
            {
                'use_placeholder': lambda i: str(i*2+2),
            },
            None,
        ),
        (
            ['test_leading_value', ],
            [50, ],
            ['50 to value'],
            'string starting with value',
            {},
            {},
        ),
        (
            ['test_uq1_empty_value1', ],
            [50, ],
            ['50 emp1'],
            'Test empty formatter with no positional value, i.e. {}',
            {},
            None,
        ),
        (
            ['test_uq2_empty_value1', 'test_uq2_empty_value2'],
            [50, 100],
            ['50 100 emp2'],
            'Test 2 empty formatters with no positional value, i.e. {} {}',
            {},
            None,
        ),
        (
            ['test_uq3_empty_value1', 'test_uq3_empty_value2',
             'test_uq3_empty_value3'],
            [50, 100, 150],
            ['50 100 150 emp3'],
            'Test 3 empty formatters with no positional value, i.e. {} {} {}',
            {},
            None,
        ),
        (
            ['test_empty_value_d', ],
            [50, ],
            ['50 emp_value_d'],
            'Test empty formatter with no positional value and the d format '
            'type, i.e. {:d}',
            {},
            None,
        ),
        (
            ['test_empty_value_plus_d', ],
            [50, ],
            ['+50 emp_value_plus_d'],
            'Test empty formatter with no positional value and the +d format '
            'type, i.e. {:+d}',
            {},
            None,
        ),
        #
        # Quantifier tests
        #
        (
            ['test_dollar_d_quantifier_divide_by_one_hundred'],
            [150],
            ['Quantifier /100: 1.5'],
            'Test floating point number with $d format and quantifier',
            {},
            {},
        ),
    )

    live_functionality_tests = ()
    '''live_functionality_tests = (
        # File, Tags, values, result, message, trr, reverse keyargs
        (
            'skill_stat_descriptions.txt',
            ['base_number_of_projectiles_in_spiral_nova',
             'projectile_spiral_nova_angle'],
            [32, -720],
            ['Fires Projectiles at all nearby Enemies'],
            'Test partial and order',
            {},
            None,
        ),
    )'''

    test_data = []
    for size, unique_id, values in data['base']:
        tags, results = get_test(size, unique_id, len(values), values)
        for i, v in enumerate(values):
            test_data.append((tags, v, results[i]))

    def functionality(self, tf, tags, values, result, message, kwargs,
                      rkwargs):
        assert tf.get_translation(tags, values, **kwargs) == result, \
            "%s: 'normal failed" % message

        if rkwargs is not None:
            trr = tf.reverse_translation(result[0], **rkwargs)
            assert trr.translations[0].ids == tags, \
                '%s: reverse failed incorrect tags' % message
            assert trr.values[0] == values, \
                '%s: failed reverse incorrect values' % message
    #
    # Actual tests
    #

    def test_read(self, dbase):
        pass

    def test_read_with_include(self, dextended):
        pass

    @pytest.mark.parametrize('tags,values,result', test_data)
    def test_get_translation_simple(self, dbase, tags, values, result):
        assert dbase.get_translation(tags, values)[0] == result

    @pytest.mark.parametrize('tags,values,string', test_data)
    def test_reverse_translation_simple(self, dbase, string, values, tags):
        trr = dbase.reverse_translation(string)
        # Returns a list of matching translations/values, but our test data
        # should be unique
        assert trr.values[0] == list(values)
        assert trr.translations[0].ids == tags

    @pytest.mark.parametrize('tags,values,result,message,kwargs,rkwargs',
                             functionality_tests)
    def test_functionality(self, dbase, tags, values, result, message, kwargs,
                           rkwargs):
        self.functionality(
            dbase, tags, values, result, message, kwargs, rkwargs
        )

    @pytest.mark.parametrize(
        'filename,tags,values,result,message,kwargs,rkwargs',
        live_functionality_tests)
    def test_live_functionality(self, ggpk_tc, filename, tags, values, result,
                           message, kwargs, rkwargs):
        self.functionality(
            ggpk_tc[filename], tags, values, result, message, kwargs, rkwargs
        )

    def test_quantifier_mod_value_to_item_class(self, tf_data, rr):
        rr['ItemClasses.dat'].build_index('Id')
        row = rr['ItemClasses.dat'].index['Id']['Bow']
        tags = ['test_quantifier_mod_value_to_item_class', ]
        values = [row.rowid, ]
        result = ['Item class: %s' % row['Name'], ]

        assert tf_data.get_translation(tags, values) == result, "normal failed"

        trr = tf_data.reverse_translation(result[0])
        assert trr.translations[0].ids == tags, \
            'reverse failed incorrect tags'
        assert trr.values[0] == values, \
            'failed reverse incorrect values'

    def test_quantifier_tempest_mod_text(self, tf_data, rr):
        rr['Mods.dat'].build_index('Id')
        row = rr['Mods.dat'].index['Id']['MapEclipseItemsDropCorrupted']
        tags = ['test_quantifier_tempest_mod_text', ]
        values = [row.rowid, ]
        result = ['Mod: %s' % row['Name'], ]

        assert tf_data.get_translation(tags, values) == result, "normal failed"

        trr = tf_data.reverse_translation(result[0])
        assert trr.translations[0].ids == tags, \
            'reverse failed incorrect tags'
        assert trr.values[0] == values, \
            'failed reverse incorrect values'

    def test_reminderstring(self, tf_data, rr):
        rr['ClientStrings.dat'].build_index('Id')
        row = rr['ClientStrings.dat'].index['Id']['ReminderTextLowLife']
        tags = ['test_quantifier_reminderstring', ]
        values = [1, ]
        result = OrderedDict((('reminderstring', row['Text']), ))

        tr = tf_data.get_translation(tags, values, full_result=True)

        assert tr.extra_strings[0] == result


class TestTranslation:
    pass


class TestTranslationLanguage:
    pass


class TestTranslationString:
    def test_original_string(self, ts):
        assert ts.string == 'Multiple: {0} {1} {0} {1}'

    def test_as_format_string(self, ts):
        assert ts.as_format_string == 'Multiple: {0} {1} {0} {1}'


def test_custom_file():
    translations.get_custom_translation_file()

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