"""
Tests for _data/dat.specification.ini

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | tests/test_data.py                                               |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Tests for for the specifications found in dat.specification.ini.
Running this test is relatively time-consuming, so it may be a good idea to
avoid it unless a PoE update has been released to locate broken or unsupported
.dat files.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os.path
import warnings

# 3rd Party
import pytest

# self
from PyPoE.poe.constants import DISTRIBUTOR, VERSION
from PyPoE.poe.path import PoEPath
from PyPoE.poe.file import dat, ggpk

# =============================================================================
# Functions
# =============================================================================


def read_ggpk():
    path = PoEPath(
        version=VERSION.STABLE,
        distributor=DISTRIBUTOR.INTERNATIONAL,
    ).get_installation_paths()
    if path:
        path = path[0]
    else:
        warnings.warn('PoE not found, skipping test.')
        return

    contents = ggpk.GGPKFile()
    contents.read(os.path.join(path, 'content.ggpk'))
    contents.directory_build()

    file_set = set()

    for node in contents['Data'].files:
        name = node.record.name
        if not name.endswith('.dat'):
            continue

        file_set.add(name)

    file_set = list(file_set)
    file_set.sort()

    return contents, file_set


def get_pk_validate_fields():
    tests = []
    for file_name, file_section in dat.load_spec().items():
        for field_name, field_section in file_section['fields'].items():
            if not field_section['primary_key']:
                continue
            tests.append((file_name, field_name))
    return tests

# =============================================================================
# Setup
# =============================================================================

ggpk, file_set = read_ggpk()
nodes = [ggpk['Data'][fn] for fn in file_set]
rr = dat.RelationalReader(path_or_ggpk=ggpk, read_options={'use_dat_value': False})

# =============================================================================
# Tests
# =============================================================================


# Kind of testing the reading of the files twice, but whatever.
@pytest.mark.parametrize("node", nodes)
def test_definitions(node):
    opt = {
        'use_dat_value': False,
    }
    # Will raise errors accordingly if it fails
    df = dat.DatFile(node.name)
    df.read(node.record.extract(), **opt)


'''@pytest.mark.parametrize("file_name", file_set)
def test_relations(file_name):
    df = rr[file_name]


@pytest.mark.parametrize("file_name, field_name", get_pk_validate_fields())
def test_primary_key_uniqueness(file_name, field_name):
    df = rr[file_name]
    index = df.table_columns[field_name]['index']

    data = [row[index] for row in df]

    assert len(data) == len(set(data))'''

