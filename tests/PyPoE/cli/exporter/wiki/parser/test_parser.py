"""
Tests for parser.py

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/cli/exporter/wiki/parser/test_parser.py              |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Tests for PyPoE.cli.exporter.wiki.parser

Agreement
===============================================================================

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
from PyPoE.cli.exporter import config

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope='module')
def parserobj():
    try:
        path = config.option['temp_dir']
        fail = os.path.exists(path)
    except KeyError:
        fail = True
    if fail:
        pytest.skip('temp dir from pypoe_exporter not found')
    return parser.BaseParser(base_path=path)

# =============================================================================
# Tests
# =============================================================================

# List of strings that are prone to breaking and difficult
iwdata = (
    # Purity of Fire vs Fire Skill, capital vs lower case spelling
    (
        'Grants level 15 Purity of Fire Skill',
        'Grants [[Level|level]] 15 [[Purity of Fire]] [[Skill]]',
    ),
    # Good for testing the nesting issue
    (
        '1 to Maximum Frenzy Charges',
        '1 to Maximum [[Frenzy Charge|Frenzy Charges]]',
    ),
    (
        '(11 to 28)% increased Armour and Energy Shield',
        '(11 to 28)% increased [[Armour]] and [[Energy Shield]]'
    ),
    # Skill vs Kill
    (
        '10% reduced Mana Cost of Skills if you\'ve been Hit Recently',

        '10% reduced [[Mana]] Cost of [[Skill|Skills]] if you\'ve been [[Hit]] '
        '[[Recently]]',
    ),
    # Support gem in string match
    (
        'Socketed Gems are supported by level 6 Stun',

        '[[Item socket|Socketed]] Gems are supported by '
        '[[Stun (support gem)|level 6 Stun]]',
    ),
    #
    (
        'Socketed Gems are Supported by level 10 Faster Casting',

        '[[Item socket|Socketed]] Gems are Supported by '
        '[[Faster Casting|level 10 Faster Casting]]',
    ),
)


# =============================================================================
# Tests
# =============================================================================


class TestBaseParser():
    data = (
        # Mod ID, expected results
        (
            'Strength1',
            [
                '+(8 to 12) to [[Strength]]',
            ],
        ),
        (
            'MonsterCriticals1',
            [
                '<abbr title="Powerful Crits">300% increased Global [[Critical Strike Chance]]</abbr>',
                '+65% to Global [[Critical Strike Multiplier]] (Hidden)',
            ],
        ),
    )
    @pytest.mark.parametrize('mod_id,result', data)
    def test_get_stats(self, parserobj, mod_id, result):
        mods = parserobj.rr['Mods.dat']
        for mod in mods:
            if mod['Id'] == mod_id:
                break

        assert parserobj._get_stats(mod) == result


@pytest.mark.parametrize('string,result', iwdata)
def test_interwiki_linker(string, result):
    assert parser.make_inter_wiki_links(string) == result