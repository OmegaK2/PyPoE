"""
Tests for _data/dat.specification.ini

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/test_data.py                                               |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for for the specifications found in dat.specification.ini.
Running this test is relatively time-consuming, so it may be a good idea to
avoid it unless a PoE update has been released to locate broken or unsupported
.dat files.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd Party
import pytest

# self
from PyPoE.poe.file import dat
from PyPoE.poe.file.specification import load

# =============================================================================
# Functions
# =============================================================================


# =============================================================================
# Setup
# =============================================================================


@pytest.fixture(scope='module')
def files(poe_version):
    return [
        section for section in load(version=poe_version)
    ]

# =============================================================================
# Tests
# =============================================================================

# Kind of testing the reading of the files twice, but whatever.
# dat_file_name is parametrized in conftest.py
@pytest.mark.parametrize('x64', (False, ))
def test_definitions(dat_file_name, file_system, x64):
    opt = {
        'use_dat_value': False,
        'x64': x64
    }
    if x64:
        dat_file_name += '64'
    # Will raise errors accordingly if it fails
    df = dat.DatFile(dat_file_name)
    try:
        df.read(file_system.get_file('Data/' + dat_file_name), **opt)
    # If a file is in the spec, but not in the dat file this is allright
    except FileNotFoundError:
        return


def test_missing(files, file_system):
    file_set = set()

    for fn in file_system.index.get_dir_record('Data/').files:
        if not fn.endswith('.dat'):
            continue

        # Not a regular dat file, ignore
        if fn in ['Languages.dat']:
            continue

        file_set.add(fn)

    # Sorting by name makes this easier to correct when error shows up
    assert sorted(file_set.difference(set(files))) == [], 'ggpk contains unhandled .dat files'
    assert sorted(set(files).difference(file_set)) == [], 'dat specification contains unused dat files'


# unique_dat_file_name & unique_field_name are parametrized in conftest.py
def test_uniqueness(unique_dat_file_name, unique_dat_field_name, rr):
    df = rr[unique_dat_file_name]
    index = df.table_columns[unique_dat_field_name]['index']

    data = []
    for row in df:
        value = row[index] if not isinstance(row[index], dat.DatRecord) else row[index].rowid
        # Duplicate "None" values are acceptable.
        if value is None:
            continue
        data.append(value)

    assert len(data) == len(set(data))

