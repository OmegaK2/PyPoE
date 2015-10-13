"""
Path     PyPoE/tests/PyPoE/cli/exporter/wiki/parser/test_parser.py
Name     Tests for parser.py
Version  1.0.0a0
Revision $Id$
Author   [#OMEGA]- K2

INFO

Tests for PyPoE.cli.exporter.wiki.parser


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd-party
import pytest

# self
from PyPoE.cli.exporter.wiki import parser

# =============================================================================
# Setup
# =============================================================================

# TODO extract files
path = 'C:/Temp'
data_path = os.path.join(path, 'Data')
desc_path = os.path.join(path, 'Metadata')

# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope='module')
def parserobj():
    return parser.BaseParser(base_path=path, data_path=data_path, desc_path=desc_path)

# =============================================================================
# Tests
# =============================================================================

data = (
    # Mod ID, expected results
    (
        'Strength1',
        [
            '(8 to 12) to Strength',
        ],
    ),
    (
        'MonsterCriticals1',
        [
            '<abbr title="300% increased Global Critical Strike Chance">Powerful Crits</abbr>',
            '50% increased Global Critical Strike Multiplier (Hidden)',
        ],
    ),

)

class TestBaseParser():
    @pytest.mark.parametrize('mod_id,result', data)
    def test_get_stats(self, parserobj, mod_id, result):
        mods = parserobj.rr['Mods.dat']
        for mod in mods:
            if mod['Id'] == mod_id:
                break

        assert parserobj._get_stats(mod) == result