"""
Tests for parsers/item.py

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/cli/exporter/wiki/parser/test_wiki_item_parser.py    |
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

# 3rd-party
import pytest

# self
from PyPoE.cli.exporter.core import config
from PyPoE.cli.exporter.wiki.parsers import item

# =============================================================================
# Globals
# =============================================================================

ERR = 'Test relies on the cli client being setup properly to run.'

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope='module')
def item_parser(poe_version, cli_config):
    #TODO: A bit of hacky bandaid
    try:
        path = config['Config']['temp_dir']
    except KeyError:
        pytest.skip(ERR)

    if not os.path.exists(path):
        pytest.skip(ERR)

    return item.ItemsParser(base_path=path)

# =============================================================================
# Tests
# =============================================================================


class TestBaseParser():
    items = (
        # =====================================================================
        # Flasks
        # =====================================================================
        #('Colossal Life Flask', None),
        #('Colossal Mana Flask', None),
        #('Colossal Hybrid Flask', None),
        #('Silver Flask', None),
        # Diamond flask has it's own item class
        #('Diamond Flask', None),

        # =====================================================================
        # Accessory
        # =====================================================================

        #
        # Amulets
        #

        ('Jade Amulet', None),
        # Conflict testing
        ('Monkey Paw Talisman', None),
        ('Avian Twins Talisman', None),

        #
        # Rings
        #

        ('Gold Ring', None),

        #
        # Belts
        #

        ('Rustic Sash', None),

        #
        # Jewels
        #

        ('Prismatic Jewel', None),

        # =====================================================================
        # Equipment
        # =====================================================================

        # Gloves
        ('Assassin\'s Mitts', None),

        # Boots
        ('Soldier Boots', None),

        # Body Armours
        ('Oiled Coat', None),

        # Helmets
        ('Sallet', None),

        # Shields
        ('Steel Kite Shield', None),

        # Quivers
        ('Sharktooth Arrow Quiver', None),

        # =====================================================================
        # Weapons
        # =====================================================================

        # Claws
        ('Gemini Claw', None),

        # Daggers
        ('Sai', None),

        # Wands
        ('Tornado Wand', None),

        # One Hand Swords
        ('Gladius', None),

        # Thrusting One Hand Swords
        ('Vaal Rapier', None),

        # One Hand Axes
        ('Vaal Hatchet', None),

        # One Hand Maces
        ('Auric Mace', None),

        # Bows
        ('Harbinger Bow', None),

        # Staves
        ('Foul Staff', None),

        # Two Hand Swords
        ('Reaver Sword', None),

        # Two Hand Axes
        ('Vaal Axe', None),

        #
        # Two Hand Maces
        #
        ('Terror Maul', None),

        #
        # Sceptres
        #
        ('Void Sceptre', None),

        #
        # Fishing Rods
        #
        ('Fishing Rod', None),

        # =====================================================================
        # Active Skill Gems
        # =====================================================================
        # Projectile gems with a mapping will be automatically added
        # A few gems from speciality categories are needed

        ('Vortex', None),
        ('Summon Stone Golem', None),
        ('Vaal Haste', None),
        ('Riposte', None),
        ('Lightning Trap', None),
        ('Fire Nova Mine', None),

        # =====================================================================
        # Support Skill Gems
        # =====================================================================
        # Again, we should have some speciality gems that do things like
        # adding cooldowns, etc
        ('Poison Support', None),
        ('Cast On Critical Strike Support', None),
        ('Trap Support', None),

        # =====================================================================
        # Currency-like items
        # =====================================================================

        #
        # Currency
        #
        ('Vaal Orb', None),

        #
        # Divination Cards
        #

        ('The Void', None),

        #
        # Hideout Doodads
        #

        # Multiple variants, test for conflicts
        ('Mat', ('Hideout Doodads', )),
        ('Challenger Trophy', None),

        #
        # Microtransactions
        #
        ('Wolf Pet', None),

        # =====================================================================
        # Map-like items
        # =====================================================================

        #
        # Maps
        #

        # Should hit the conflict resolver
        ('Gorge Map', None),

        #
        # Fragments
        #
        ('Mortal Grief', None),

        #
        # Lab thingy
        #
        ('Offering to the Goddess', None),

        # =====================================================================
        # Misc
        # =====================================================================

        #
        # Quest items
        #

        #('The Eye of Fury', None),
        # Test conflict resolver
        #('Book of Skill', None),

        #
        # Lab items
        #

        ('Golden Key', None),

        #
        # Lab trinkets
        #

        ('Bane of the Loyal', None),
    )

    # Also test all the skill gems with a projectile mapping
    items += tuple([(v, None) for v in
                    item.ItemsParser._SKILL_ID_TO_PROJECTILE_MAP.keys()])

    @pytest.mark.parametrize('item_name,cls', items)
    def test_for_errors(self, item_name, cls, item_parser):
        args = type('Args', (object, ), {
            'item_class': cls,
            'is_metadata_id': False,
            'item': [item_name, ],
            'store_images': False,
        })
        item_parser.export(parsed_args=args)

