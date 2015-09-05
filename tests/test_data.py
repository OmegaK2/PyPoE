"""
Path     PyPoE/tests/test_data
Name     Tests for dat.py
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Tests for dat.py


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os.path
import traceback
import warnings
from tempfile import TemporaryDirectory

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

    contents = ggpk.GGPKFile(os.path.join(path, 'content.ggpk'))
    contents.read()
    root = contents.directory_build()

    file_set = set()

    for node in root['Data'].files:
        name = node.record.name
        if not name.endswith('.dat'):
            continue

        file_set.add(name)

    return root, file_set

# =============================================================================
# Tests
# =============================================================================

root, file_set = read_ggpk()

@pytest.mark.parametrize("node",
    [root['Data'][fn] for fn in file_set],
)
def test_definitions(node):
    opt = {
        'use_dat_value': False,
    }
    # Will raise errors accordingly if it fails
    df = dat.DatFile(node.name, options=opt)
    df.read_from_raw(node.record.extract())



