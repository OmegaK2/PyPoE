"""
Tests for PyPoE.poe.file.shared.keyvalues

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/file/test_keyvalues.py                           |
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
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from collections import OrderedDict
from tempfile import TemporaryDirectory

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
        'key': [1, 2, 3],
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
        'key': -42,
        'key_+': 42,
        'key_-': 42,
        'key_%': 42,
        'key_inherited': 1337,
    },
    'Hash': {
        'key': OrderedDict(((1, True), (2, True), (3, True))),
    }
}


class KeyValuesSectionAppend(keyvalues.AbstractKeyValueSection):
    NAME = 'Append'
    APPEND_KEYS = {'key'}


class KeyValuesSectionOverride(keyvalues.AbstractKeyValueSection):
    NAME = 'Override'


class KeyValuesSectionOverrideGeneric(keyvalues.AbstractKeyValueSection):
    NAME = 'OverrideGeneric'


class KeyValuesSectionHash(keyvalues.AbstractKeyValueSection):
    NAME = 'Hash'
    ORDERED_HASH_KEYS = {'key'}


class KeyValuesFile(keyvalues.AbstractKeyValueFile):

    EXTENSION = '.kv'

    SECTIONS = dict((s.NAME, s) for s in [
        KeyValuesSectionAppend,
        KeyValuesSectionOverride,
        KeyValuesSectionOverrideGeneric,
        KeyValuesSectionHash,
    ])


class KeyValuesFileCache(keyvalues.AbstractKeyValueFileCache):
    FILE_TYPE = KeyValuesFile

_read_file_name = 'keyvalues.kv'
_write_file_name = 'keyvalues_write.kv'

# =============================================================================
# Fixtures
# =============================================================================

# =============================================================================
# Tests
# =============================================================================

class TestKeyValuesFile:

    data = [(section, key, value) for section, keyvalues in data.items() for key, value in keyvalues.items()]

    @pytest.fixture
    def kf_file(self):
        kf = KeyValuesFile(parent_or_base_dir_or_ggpk=data_dir)
        kf.read(os.path.join(data_dir, _read_file_name))
        return kf

    @pytest.fixture
    def kf_memory_file(self):
        kf = KeyValuesFile()
        kf.version = 2
        kf.extends = None
        kf['Section1'] = keyvalues.AbstractKeyValueSection(
            parent=kf, name='Section'
        )
        kf['Section2'] = keyvalues.AbstractKeyValueSection(
            parent=kf, name='Section'
        )
        kf['Section1']['key'] = 42
        kf['Section2']['key'] = 42

        return kf

    def test_read_attrs(self, kf_file):
        assert kf_file.version == 2
        assert kf_file.extends == 'keyvalues_base'

    @pytest.mark.parametrize('section,key,value', data)
    def test_read_keyvalues(self, kf_file, section, key, value):
        assert kf_file[section][key] == value

    def test_write(self, kf_memory_file):
        with TemporaryDirectory() as d:
            tmp_path = os.path.join(d, _write_file_name)
            kf_memory_file.write(tmp_path)

            kf_should = KeyValuesFile()
            kf_should.read(os.path.join(data_dir, _write_file_name))

            kf_target = KeyValuesFile()
            kf_target.read(tmp_path)

            assert kf_target == kf_should


class TestKeyValuesFileCache:
    @pytest.fixture
    def kf_cache(self):
        kfc = KeyValuesFileCache(path_or_ggpk=data_dir)

        return kfc

    def test_cache_get_file(self, kf_cache):
        kf = kf_cache.get_file(_read_file_name)
        assert kf is kf_cache.get_file(_read_file_name)


