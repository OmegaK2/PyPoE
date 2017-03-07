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

# =============================================================================
# Functions
# =============================================================================


def get_pk_validate_fields():
    tests = []
    for file_name, file_section in dat.load_spec().items():
        for field_name, field_section in file_section['fields'].items():
            if not field_section['unique']:
                continue
            tests.append((file_name, field_name))
    return tests

# =============================================================================
# Setup
# =============================================================================

files = [section.name for section in dat.load_spec().values()]

# =============================================================================
# Tests
# =============================================================================


# Kind of testing the reading of the files twice, but whatever.
@pytest.mark.parametrize("file_name", files)
def test_definitions(file_name, ggpkfile):
    opt = {
        'use_dat_value': False,
    }
    # Will raise errors accordingly if it fails
    df = dat.DatFile(file_name)
    try:
        node = ggpkfile['Data/' + file_name]
        df.read(node.record.extract(), **opt)
    # If a file is in the spec, but not in the dat file this is allright
    except FileNotFoundError:
        return


def test_missing(ggpkfile):
    file_set = set()

    for node in ggpkfile['Data'].files:
        name = node.record.name
        if not name.endswith('.dat'):
            continue

        # Not a regular dat file, ignore
        if name in ['Languages.dat']:
            continue

        file_set.add(name)

    assert file_set.difference(set(files)) == set(), 'ggpk contains unhandled .dat files'
    assert set(files).difference(file_set) == set(), 'dat specification contains unused dat files'


@pytest.mark.parametrize("file_name, field_name", get_pk_validate_fields())
def test_uniqueness(file_name, field_name, rr):
    df = rr[file_name]
    index = df.table_columns[field_name]['index']

    data = []
    for row in df:
        value = row[index] if not isinstance(row[index], dat.DatRecord) else row[index].rowid
        # Duplicate "None" values are acceptable.
        if value is None:
            continue
        data.append(value)

    assert len(data) == len(set(data))

