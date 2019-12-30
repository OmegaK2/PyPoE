"""
Tests for parser.py

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/cli/exporter/wiki/test_parser.py                     |
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
from collections import OrderedDict

# 3rd-party
import pytest

# self
from PyPoE.poe.constants import MOD_STATS_RANGE
from PyPoE.poe.text import parse_description_tags
from PyPoE.cli.exporter.wiki import parser
from PyPoE.cli.exporter import config

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope='module')
def parserobj(poe_version, cli_config):
    try:
        path = config.option['temp_dir']
        fail = not os.path.exists(path)
    except KeyError:
        fail = True
    if fail:
        pytest.skip('temp dir from pypoe_exporter not found')
    return parser.BaseParser(base_path=path)

@pytest.fixture(scope='module')
def tag_handler_obj(rr):
    return parser.TagHandler(rr)

@pytest.fixture(scope='module')
def divination_card_texts(rr):
    return [
        parse_description_tags(row['Description'])
        for row in rr['CurrencyItems.dat']
        if row['BaseItemTypesKey']['ItemClassesKey']['Name'] ==
        'Divination Card']

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
        '[[Stun Support|level 6 Stun]]',
    ),
    #
    (
        'Socketed Gems are Supported by level 10 Faster Casting',

        '[[Item socket|Socketed]] Gems are Supported by '
        '[[Faster Casting Support|level 10 Faster Casting]]',
    ),
)

# Input string, template name, other text, template args, template kwargs
ftdata = (
    # Intended behaviour
    (
        """other{{Test|param=5}}text""",
        'Test',
        ['other', 'text'],
        [],
        OrderedDict((
            ('param', '5'),
        )),
    ),
    (
        """other{{Test}}text""",
        'Test',
        ['other', 'text'],
        [],
        OrderedDict(()),
    ),
    # Shouldn't be matched
    (
        """other{{Test match|param=5}}text""",
        'Test',
        ['other{{Test match|param=5}}text'],
        [],
        OrderedDict(()),
    ),
    (
        """other{{Test match}}text""",
        'Test',
        ['other{{Test match}}text'],
        [],
        OrderedDict(()),
    ),
    # Real life test
    (
        """{{Upcoming content|version=3.0.0}}

{{Item
|rarity                           = Normal
|name                             = Captured Soul of Glace
|drop_level                       = 1
|description                      = {{c|corrupted|Cannot be traded or modified}}
|metadata_id                      = Metadata/Items/PantheonSouls/PantheonSoulBrineKingUpgrade1
|release_version                  = 3.0.0
}}

'''{{PAGENAME}}''' can be given to [[Sin]] to upgrade the [[The Pantheon|Soul of the Brine King]] Pantheon Power.

==Acquisition==
This item can be obtained by using a {{il|Divine Vessel}} with a {{il|Beach Map}} and then killing [[Glace]]; The captured soul will be in whichever map device was used to open the map.""",
        'Item',
        [
            """{{Upcoming content|version=3.0.0}}

""",
    """

'''{{PAGENAME}}''' can be given to [[Sin]] to upgrade the [[The Pantheon|Soul of the Brine King]] Pantheon Power.

==Acquisition==
This item can be obtained by using a {{il|Divine Vessel}} with a {{il|Beach Map}} and then killing [[Glace]]; The captured soul will be in whichever map device was used to open the map.""",
        ],
        [],
        OrderedDict((
            ('rarity', 'Normal'),
            ('name', 'Captured Soul of Glace'),
            ('drop_level', '1'),
            ('description', '{{c|corrupted|Cannot be traded or modified}}'),
            ('metadata_id', 'Metadata/Items/PantheonSouls/PantheonSoulBrineKingUpgrade1'),
            ('release_version', '3.0.0'),
        )),
    ),
)


# =============================================================================
# Tests
# =============================================================================


class TestBaseParser:
    data = (
        # Mod ID, expected results
        (
            'Strength1',
            [
                '+(8-12) to [[Strength]]',
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
        mod = parserobj.rr['Mods.dat'].index['Id'][mod_id]

        stats = []
        values = []
        for i in MOD_STATS_RANGE:
            k = mod['StatsKey%s' % i]
            if k is None:
                continue
            stat = k['Id']
            value = mod['Stat%sMin' % i], mod['Stat%sMax' % i]

            if value[0] == 0 and value[1] == 0:
                continue

            stats.append(stat)
            values.append(value)

        assert parserobj._get_stats(stats, values, mod) == result


class TestTagHandler:
    def test_handlers(self, tag_handler_obj, divination_card_texts):
        missing_handlers = set()
        for tag in divination_card_texts:
            try:
                text = tag.handle_tags(tag_handler_obj.tag_handlers)
            except KeyError as e:
                missing_handlers.add(e.args[0])

        assert missing_handlers == set()


@pytest.mark.parametrize('string,result', iwdata)
def test_interwiki_linker(string, result):
    assert parser.make_inter_wiki_links(string) == result


@pytest.mark.parametrize('string,template,texts,args,kwargs', ftdata)
def test_find_template(string, template, texts, args, kwargs):
    result = parser.find_template(string, template)
    assert result['texts'] == texts
    assert result['args'] == args
    assert result['kwargs'] == kwargs