"""
Tests for PyPoE.poe.file.shared.keyvalues

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/file/test_keyvalues.py                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------



Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd-party
import pytest

# self
from PyPoE.poe.file.shared import keyvalues

# =============================================================================
# Setup
# =============================================================================

data_dir = os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], '_data')

data = {
    'Append': {
        'key': set([1, 2, 3]),
    },
    'Override': {
        'key': 42,
        'warning': 42,
    },
    'OverrideGeneric': {
        'key': 42,
        'no_warning': 42,
    },
    'Extra': {
        'key': 42,
        'key_inherited': 1337,
    },
}

class KeyValuesSectionAppend(keyvalues.AbstractKeyValueSection):
    NAME = 'Append'
    APPEND_KEYS = ['key']


class KeyValuesSectionOverride(keyvalues.AbstractKeyValueSection):
    NAME = 'Override'
    OVERRIDE_KEYS = ['key']


class KeyValuesSectionOverrideGeneric(keyvalues.AbstractKeyValueSection):
    NAME = 'OverrideGeneric'
    OVERRIDE_WARNING = False


class KeyValuesFile(keyvalues.AbstractKeyValueFile):

    EXTENSION = '.kv'

    SECTIONS = dict((s.NAME, s) for s in [
        KeyValuesSectionAppend,
        KeyValuesSectionOverride,
        KeyValuesSectionOverrideGeneric,
    ])


# =============================================================================
# Fixtures
# =============================================================================

# =============================================================================
# Tests
# =============================================================================

class TestKeyValuesFile(object):

    data = [(section, key, value) for section, keyvalues in data.items() for key, value in keyvalues.items()]

    @pytest.fixture
    def kf_file(self):
        kf = KeyValuesFile(parent_or_base_dir_or_ggpk=data_dir)
        kf.read(os.path.join(data_dir, 'test.kv'))
        return kf

    def test_read_attrs(self, kf_file):
        assert kf_file.version == 2
        assert kf_file.extends == 'test_base'

    @pytest.mark.parametrize('section,key,value', data)
    def test_read_keyvalues(self, kf_file, section, key, value):
        assert kf_file[section][key] == value
