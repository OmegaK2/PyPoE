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
from PyPoE.poe.path import PoEPath
from PyPoE.poe.file import dat, ggpk

# =============================================================================
# Functions
# =============================================================================

def test_definitions():
    path = PoEPath(version=PoEPath.VERSION_STABLE).get_installation_paths()
    if path:
        path = path[0]
    else:
        warnings.warn('PoE not found, skipping test.')
        return

    contents = ggpk.GGPKFile(os.path.join(path, 'content.ggpk'))
    contents.read()
    root = contents.directory_build()
    spec_set = set(dat._default_spec.keys())
    file_set = set()

    for node in root['Data'].files:
        name = node.record.name
        if not name.endswith('.dat'):
            continue

        file_set.add(name)

        # assert that later with a whole set
        if name not in spec_set:
            continue

        opt = {
            'use_dat_value': False,
        }
        df = dat.DatFile(name, options=opt)
        try:
            df.read_from_raw(node.record.extract())
        except Exception as e:
            pytest.fail("%s failed with unexpected error:\n%s" % (name, traceback.format_exc()))

    # Make the output easier to read
    diff = sorted(list(file_set.difference(spec_set)))
    assert not bool(diff), "%s not in specification" % diff



