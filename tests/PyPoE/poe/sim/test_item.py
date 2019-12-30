"""
Tests for PyPoE.poe.sim.item

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | tests/PyPoE/poe/sim/test_item.py                                 |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Provides various utility functions for handling items.

The :class:`ItemParser` class can be used to parse the item strings PoE
provides when an item is copied using CTRL-C.


Agreement
===============================================================================

See PyPoE/LICENSE

TODO
===============================================================================

ItemParser
* Divination cards are currently unsupported as there is no reliable way of
  detecting them

"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party
import pytest

# self
from PyPoE.poe.constants import RARITY, SOCKET_COLOUR
from PyPoE.poe.sim import item

# =============================================================================
# Setup
# =============================================================================

# =============================================================================
# Fixtures
# =============================================================================

# =============================================================================
# Tests
# =============================================================================

class TestItemParser:
    data = (
        #
        # Regular items
        #
        ('''Rarity: Normal
Ruby Ring
--------
Requirements:
Level: 11
--------
Item Level: 18
--------
+25% to Fire Resistance''',
             {
                 'rarity': RARITY.NORMAL,
                 'name': 'Ruby Ring',
                 'required_level': 11,
                 'item_level': 18,
                 'implicit_stats': [
                     '+25% to Fire Resistance',
                 ],
             }
         ),
        ('''Rarity: Rare
Ghoul Cry
Abyssal Sceptre
--------
One Handed Mace
Physical Damage: 38-57
Elemental Damage: 24-43 (augmented), 24-44 (augmented), 6-65 (augmented)
Critical Strike Chance: 6.50%
Attacks per Second: 1.25
--------
Requirements:
Level: 53
Str: 83 (unmet)
Int: 99 (unmet)
--------
Sockets: R-G-B
--------
Item Level: 56
--------
15% increased Elemental Damage
--------
Adds 24-43 Fire Damage
Adds 24-44 Cold Damage
Adds 6-65 Lightning Damage
28% increased Global Critical Strike Multiplier''',
            {
                'rarity': RARITY.RARE,
                'name': 'Ghoul Cry',
                'base_item_name': 'Abyssal Sceptre',
                'physical_damage': [38, 57],
                'elemental_damage': [[24, 43], [24, 44], [6, 65]],
                'critical_strike_chance': 6.5,
                'attacks_per_second': 1.25,
                'required_level': 53,
                'required_str': 83,
                'required_int': 99,
                'sockets': [
                    item.ItemSocket(0, SOCKET_COLOUR.RED),
                    item.ItemSocket(1, SOCKET_COLOUR.GREEN),
                    item.ItemSocket(2, SOCKET_COLOUR.BLUE),
                ],
                'links': [
                    [
                        item.ItemSocket(0, SOCKET_COLOUR.RED),
                        item.ItemSocket(1, SOCKET_COLOUR.GREEN),
                        item.ItemSocket(2, SOCKET_COLOUR.BLUE),
                    ]
                ],
                'item_level': 56,
                'implicit_stats': [
                    '15% increased Elemental Damage',
                ],
                'stats': [
                    'Adds 24-43 Fire Damage',
                    'Adds 24-44 Cold Damage',
                    'Adds 6-65 Lightning Damage',
                    '28% increased Global Critical Strike Multiplier',
                ],
            },
        ),
        # Clearly an edge case - it doesn't have flavour text
        ('''Rarity: Unique
Tabula Rasa
Simple Robe
--------
Sockets: W-W-W-W-W-W
--------
Item Level: 73''',
            {
                'rarity': RARITY.UNIQUE,
                'name': 'Tabula Rasa',
                'base_item_name': 'Simple Robe',
                'sockets': [item.ItemSocket(i, SOCKET_COLOUR.W) for i in range(0, 6)],
                'links': [[item.ItemSocket(i, SOCKET_COLOUR.W) for i in range(0, 6)], ],
                'item_level': 73,
            },
        ),
        ('''Rarity: Unique
Iron Ring
--------
Item Level: 18
--------
Adds 1-4 Physical Damage to Attacks
--------
Unidentified''',
             {
                 'rarity': RARITY.UNIQUE,
                 'name': 'Iron Ring',
                 'item_level': 18,
                 'implicit_stats': [
                     'Adds 1-4 Physical Damage to Attacks',
                 ],
                 'stats': [
                     'Unidentified',
                 ],
             }
        ),
        ('''Rarity: Unique
Blackheart
Iron Ring
--------
Item Level: 18
--------
Adds 1-4 Physical Damage to Attacks
--------
5% increased Physical Damage
Adds 1-3 Chaos Damage to Attacks
+26 to maximum Life
3.8 Life Regenerated per second
10% chance to Cause Monsters to Flee
--------
Fear is highly infectious.''',
            {
                'rarity': RARITY.UNIQUE,
                'name': 'Blackheart',
                'base_item_name': 'Iron Ring',
                'item_level': 18,
                'implicit_stats': [
                    'Adds 1-4 Physical Damage to Attacks',
                ],
                'stats': [
                    '5% increased Physical Damage',
                    'Adds 1-3 Chaos Damage to Attacks',
                    '+26 to maximum Life',
                    '3.8 Life Regenerated per second',
                    '10% chance to Cause Monsters to Flee',
                ],
                'flavour_text': 'Fear is highly infectious.',
            },
        ),
        #
        # Maps
        #
        # Special case: Vaal Fragment
        ('''Rarity: Normal
Sacrifice at Dusk
--------
Item Level: 69
--------
The Vaal shall never fear the setting of our sun.
--------
Can be used in the Eternal Laboratory or a personal Map Device.''',
            {
                'rarity': RARITY.NORMAL,
                'name': 'Sacrifice at Dusk',
                'base_item_name': 'Sacrifice at Dusk',
                'item_level': 69,
                'flavour_text': 'The Vaal shall never fear the setting of our sun.',
                'help_text': 'Can be used in the Eternal Laboratory or a personal Map Device.',
            },
        ),
        # Regular maps
        ('''Rarity: Normal
Tropical Island Map
--------
Map Tier: 1
--------
Item Level: 71
--------
Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.''',
            {
                'rarity': RARITY.NORMAL,
                'name': 'Tropical Island Map',
                'base_item_name': 'Tropical Island Map',
                'map_tier': 1,
                'item_level': 71,
                'help_text': 'Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.',
            },
        ),
        ('''Rarity: Magic
Unwavering Tropical Island Map of Commanders
--------
Map Tier: 1
Item Quantity: +15% (augmented)
--------
Item Level: 67
--------
43% more Rare Monsters
Monsters cannot be Stunned
--------
Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.''',
            {
                'rarity': RARITY.MAGIC,
                'name': 'Unwavering Tropical Island Map of Commanders',
                'prefix': 'Unwavering',
                'suffix': 'of Commanders',
                'base_item_name': 'Tropical Island Map',
                'map_tier': 1,
                'item_quantity': 15,
                'item_level': 67,
                'stats': [
                    '43% more Rare Monsters',
                    'Monsters cannot be Stunned',
                ],
                'help_text': 'Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.',
            },
        ),
        ('''Rarity: Rare
Evil Remains
Vaal Pyramid Map
--------
Map Tier: 3
Item Quantity: +41% (augmented)
Monster Pack Size: +31% (augmented)
--------
Item Level: 69
--------
Monsters deal 87% extra Damage as Fire
Monsters' skills Chain 2 additional times
Unique Boss deals 30% increased Damage
Unique Boss has 25% increased Attack and Cast Speed
--------
Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.''',
            {
                'rarity': RARITY.RARE,
                'name': 'Evil Remains',
                'base_item_name': 'Vaal Pyramid Map',
                'map_tier': 3,
                'item_quantity': 41,
                'pack_size': 31,
                'item_level': 69,
                'stats': [
                    'Monsters deal 87% extra Damage as Fire',
                    'Monsters\' skills Chain 2 additional times',
                    'Unique Boss deals 30% increased Damage',
                    'Unique Boss has 25% increased Attack and Cast Speed',
                ],
                'help_text': 'Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.',
            },
        ),
        ('''Rarity: Unique
Strand Map
--------
Map Tier: 6
--------
Item Level: 75
--------
Unidentified
--------
Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.''',
            {
                'rarity': RARITY.UNIQUE,
                'name': 'Strand Map',
                'base_item_name': 'Strand Map',
                'map_tier': 6,
                'item_level': 75,
                'stats': [
                    'Unidentified',
                ],
                'help_text': 'Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.',
            },
        ),
        ('''
Rarity: Unique
Whakawairua Tuahu
Strand Map
--------
Map Tier: 6
Item Quantity: +44% (augmented)
Item Rarity: +160% (augmented)
--------
Item Level: 75
--------
Area contains many Totems
Curses have 50% reduced effect on Monsters
Rare Monsters each have a Nemesis Mod
--------
We all began life in darkness, we shall all end it there.
--------
Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.''',
            {
                'rarity': RARITY.UNIQUE,
                'name': 'Whakawairua Tuahu',
                'base_item_name': 'Strand Map',
                'map_tier': 6,
                'item_quantity': 44,
                'item_rarity': 160,
                'item_level': 75,
                'stats': [
                    'Area contains many Totems',
                    'Curses have 50% reduced effect on Monsters',
                    'Rare Monsters each have a Nemesis Mod',
                ],
                'flavour_text': 'We all began life in darkness, we shall all end it there.',
                'help_text': 'Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once.',
            },
        ),
        #
        # Jewels
        #
        ('''Rarity: Normal
Crimson Jewel
--------
Item Level: 71
--------
Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.''',
            {
                'rarity': RARITY.NORMAL,
                'name': 'Crimson Jewel',
                'item_level': 71,
                'help_text': 'Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.',
            },
        ),
        ('''Rarity: Magic
Viridian Jewel of Order
--------
Item Level: 69
--------
+8% to Chaos Resistance
--------
Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.''',
            {
                'rarity': RARITY.MAGIC,
                'name': 'Viridian Jewel of Order',
                'base_item_name': 'Viridian Jewel',
                'prefix': None,
                'suffix': 'of Order',
                'item_level': 69,
                'stats': [
                    '+8% to Chaos Resistance',
                ],
                'help_text': 'Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.',
            },
        ),
        ('''Rarity: Magic
Resonant Cobalt Jewel
--------
Item Level: 73
--------
4% increased Cast Speed while Dual Wielding
--------
Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.''',
            {
                'rarity': RARITY.MAGIC,
                'name': 'Resonant Cobalt Jewel',
                'base_item_name': 'Cobalt Jewel',
                'prefix': 'Resonant',
                'suffix': None,
                'item_level': 73,
                'stats': [
                    '4% increased Cast Speed while Dual Wielding',
                ],
                'help_text': 'Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.',
            },
        ),
        ('''Rarity: Unique
Conqueror's Potency
Cobalt Jewel
--------
Limited to: 1
--------
Item Level: 1
--------
4% increased Effect of your Curses
8% increased effect of Flasks
3% increased effect of Auras you Cast
--------
What you earn is almost as important as what you take.
--------
Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.
--------
Corrupted''',
            {
                'rarity': RARITY.UNIQUE,
                'name': 'Conqueror\'s Potency',
                'base_item_name': 'Cobalt Jewel',
                'limit': 1,
                'stats': [
                    '4% increased Effect of your Curses',
                    '8% increased effect of Flasks',
                    '3% increased effect of Auras you Cast',
                ],
                'flavour_text': 'What you earn is almost as important as what you take.',
                'help_text': 'Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.',
                'is_corrupted': True,
            },
        ),
        #
        # Gems
        #
        ('''Rarity: Gem
Herald of Thunder
--------
Cast, AoE, Duration, Lightning
Level: 1
Mana Reserved: 25%
Cooldown Time: 1.00 sec
Cast Time: 1.00 sec
Damage Effectiveness: 120%
Experience: 6.773/49.725
--------
Requirements:
Level: 16
Int: 41
--------
Deals 1-34 Lightning Damage
Cannot apply Shock
Base duration is 6.00 seconds
Adds 2-7 Lightning Damage to Spells
Adds 2-7 Lightning Damage to Attacks
--------
Place into an item socket of the right colour to gain this skill. Right click to remove from a socket.''',
            {
                'name': 'Herald of Thunder',
                'gem_tags': ['Cast', 'AoE', 'Duration', 'Lightning'],
                'gem_level': 1,
                'mana_reserved': 25,
                'cooldown_time': 1,
                'cast_time': 1,
                'damage_effectiveness': 1.2,
                'experience': [6773, 49725],
                'required_level': 16,
                'required_int': 41,
                'stats': [
                    'Deals 1-34 Lightning Damage',
                    'Cannot apply Shock',
                    'Base duration is 6.00 seconds',
                    'Adds 2-7 Lightning Damage to Spells',
                    'Adds 2-7 Lightning Damage to Attacks',
                ],
                'help_text': 'Place into an item socket of the right colour to gain this skill. Right click to remove from a socket.',
            },
        ),
        ('''Rarity: Gem
Vaal Molten Shell
--------
Vaal, Spell, AoE, Duration, Fire
Level: 1
Mana Cost: 0
Souls Per Use: 48
Can Store 1 Use
Cast Time: 1.00 sec
Critical Strike Chance: 5.00%
Damage Effectiveness: 200%
Experience: 1/841
--------
Requirements:
Level: 4
Str: 16
--------
Deals 9-14 Fire Damage
Base duration is 10.00 seconds
17 additional Armour
--------
Place into an item socket of the right colour to gain this skill. Right click to remove from a socket.
--------
Corrupted''',
            {
                'name': 'Vaal Molten Shell',
                'gem_tags': ['Vaal', 'Spell', 'AoE', 'Duration', 'Fire'],
                'gem_level': 1,
                'mana_cost': 0,
                'souls_per_use': 48,
                'stored_uses': 1,
                'cast_time': 1,
                'critical_strike_chance': 5,
                'damage_effectiveness': 2,
                'experience': [1, 841],
                'required_level': 4,
                'required_str': 16,
                'stats': [
                    'Deals 9-14 Fire Damage',
                    'Base duration is 10.00 seconds',
                    '17 additional Armour',
                ],
                'help_text': 'Place into an item socket of the right colour to gain this skill. Right click to remove from a socket.',
                'is_corrupted': True,
            },
        ),
        #
        # Currency
        #
        ('''Rarity: Currency
Armourer's Scrap
--------
Stack Size: 4/40
--------
Improves the quality of an armour
--------
Right click this item then left click an armour to apply it. Has greater effect on lower rarity armours. The maximum quality is 20%.
Shift click to unstack.''',
            {
                'name': 'Armourer\'s Scrap',
                'stack_size': [4, 40],
                'description': 'Improves the quality of an armour',
                'help_text': '''Right click this item then left click an armour to apply it. Has greater effect on lower rarity armours. The maximum quality is 20%.
Shift click to unstack.''',
            },
        ),
        #
        # Hideout stuff
        #
        ('''Rarity: Currency
Book Shelf
--------
Stack Size: 1/20
--------
Creates an object in your hideout
--------
Right click this item then left click a location on the ground to create the object.''',
            {
                'name': 'Book Shelf',
                'stack_size': [1, 20],
                'description': 'Creates an object in your hideout',
                'help_text': 'Right click this item then left click a location on the ground to create the object.',
            },
        ),
        #
        # MTX
        #
        ('''Arctic Skull
--------
Helmet Skin
Stack Size: 1/20
--------
Replaces your headdress with an icy skull
--------
Right click this item then left click a head slot item to apply it.''',
            {
                'name': 'Arctic Skull',
                #todo: '': 'Helmet Skin',
                'stack_size': [1, 20],
                'description': 'Replaces your headdress with an icy skull',
                'help_text': 'Right click this item then left click a head slot item to apply it.',
            },
        ),
    )

    @pytest.mark.parametrize('string,tests', data)
    def test_init(self, string, tests):
        i = item.ItemParser(string)
        for k, v in tests.items():
            val = getattr(i, k)
            assert val == v, '%s: %s vs %s' % (k, val, v)