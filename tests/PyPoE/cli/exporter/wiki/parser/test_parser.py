"""
Tests for parser.py

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/cli/exporter/wiki/parser/test_parser.py              |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Tests for PyPoE.cli.exporter.wiki.parser

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
    return parser.BaseParser(base_path=path)

# =============================================================================
# Tests
# =============================================================================

data = (
    # Mod ID, expected results
    (
        'Strength1',
        [
            '(8 to 12) to [[Strength]]',
        ],
    ),
    (
        'MonsterCriticals1',
        [
            '<abbr title="Powerful Crits">300% increased Global [[Critical Strike Chance]]</abbr>',
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