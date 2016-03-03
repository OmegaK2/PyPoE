"""
Wiki gems exporter

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/gems.py                          |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

http://pathofexile.gamepedia.com

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import sys
import warnings
from collections import defaultdict, OrderedDict

# Self
from PyPoE.poe.sim.formula import gem_stat_requirement, GemTypes
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki.handler import *
from PyPoE.cli.exporter.wiki.parser import BaseParser

# =============================================================================
# Data
# =============================================================================

# Abbreviations
abbreviations = {
    'Adds an additional Projectile': 'Extra<br>Projectiles',
    'Adds x-y Cold Damage to Attacks': 'Attack<br>Cold<br>Damage',
    'Adds x-y Cold Damage to Spells': 'Spell<br>Cold<br>Damage',
    'Adds x-y Lightning Damage to Attacks': 'Attack<br>Lightning<br>Damage',
    'Adds x-y Lightning Damage to Spells': 'Spell<br>Lightning<br>Damage',
    'Aftershock deals x% more Damage': 'more<br>Damage',
    'Attacks with x to Melee range': 'Range',
    'Base duration is x seconds': 'Base<br>Duration',
    'Can deal x-y base Cold damage': 'Cold<br>Damage',
    'Can deal x-y base Fire damage': 'Fire<br>Damage',
    'Can deal x-y base Lightning damage': 'Lightning<br>Damage',
    'Can have up to x additional Totem summoned at a time':
        'extra<br>Totems',
    'Can summon up to x Skeletons at a time': '# Skeletons',
    'Can use Items requiring up to level x': 'max.<br>Item<br>Level',
    'Chain x Times': '# Chains',
    'Chains x Times': '# Chains',
    'Creates Corpses up to Level x': 'Corpse<br>Level',
    'Cursed enemies are x% slower': '% slower',
    'Cursed enemies deal x% less Damage': 'less<br>Damage',
    'Cursed enemies grant x Life when Hit by Attacks':
        'Life per Hit<br>with Attacks',
    'Cursed enemies grant x Life when Killed': 'Life<br>per Kill',
    'Cursed enemies grant x Mana when Hit by Attacks':
        'Mana per Hit<br>with Attacks',
    'Cursed enemies grant x Mana when Killed': 'Mana<br>per Kill',
    'Cursed enemies grant x% increased Attack Speed on Melee hit':
        'Attack Speed<br>per Melee hit',
    'Cursed enemies grant x% more Physical Melee Damage on Melee hit':
        'more<br>Physical Damage<br>per Melee hit',
    'Cursed enemies have a x% chance to grant a Frenzy Charge when slain':
        'Frenzy<br>Charge<br>Chance',
    'Cursed enemies have a x% chance to grant a Power Charge when slain':
        'Power<br>Charge<br>Chance',
    'Cursed enemies have a x% chance to grant an Endurance Charge when slain':
        'Endurance<br>Charge<br>Chance',
    'Cursed enemies have an additional x% chance to be Stunned':
        'Stun<br>Chance',
    'Cursed enemies have an additional x% chance to receive a Critical Strike':
        'Crit<br>Chance',
    'Cursed enemies have x% chance to be Frozen by Cold Damage':
        'Freeze<br>Chance',
    'Cursed enemies have x% chance to be Ignited by Fire Damage':
        'Ignite<br>Chance',
    'Cursed enemies have x% chance to be Shocked by Lightning Damage':
        'Shock<br>Chance',
    'Cursed enemies have x% less Evasion': 'less<br>Evasion',
    'Cursed enemies have x% reduced Accuracy Rating': 'reduced<br>Accuracy',
    'Cursed enemies have x% reduced Stun Recovery': 'reduced<br>Stun Recover<',
    'Cursed enemies lose x% Cold Resistance': 'reduced<br>Cold<br>Resistance',
    'Cursed enemies lose x% Elemental Resistances':
        'reduced<br>Elemental<br>Resistance',
    'Cursed enemies lose x% Fire Resistance': 'reduced<br>Fire<br>Resistance',
    'Cursed enemies lose x% Lightning Resistance':
        'reduced<br>Lightning<br>Resistance',
    'Cursed enemies take x% increased Damage from Projectiles':
        'increased<br>Projectile<br>Damage',
    'Cursed enemies take x% increased Physical damage':
        'increased<br>Physical<br>Damage',
    'Cursed enemies take x% more extra damage from Critical Strikes':
        'more<br>Critical<br>Damage',
    'Deals x Base Chaos Damage per second': 'Chaos<br>Damage<br>per sec',
    'Deals x Fire Damage per second': 'Fire<br>Damage<br>per sec',
    'Deals x% of Base Damage': '% Base<br>Damage',
    'Deals x-y Chaos Damage': 'Chaos<br>Damage',
    'Deals x-y Cold Damage': 'Cold<br>Damage',
    'Deals x-y Fire Damage': 'Fire<br>Damage',
    'Deals x-y Lightning Damage': 'Lightning<br>Damage',
    'Deals x-y Physical Damage': 'Physical<br>Damage',
    'Deals x-y base Cold Damage per Frenzy Charge':
        'Cold<br>Damage<br>per Frenzy<br>Charge',
    'Deals x-y base Fire Damage per Endurance Charge':
        'Fir<br>Damage<br>per Endurance<br>Charge',
    'Deals x-y base Lightning Damage per Power Charge':
        'Lightning<br>Damage<br>per Power<br>Charge',
    'Enemy Block Chance reduced by x% against this Skill':
        'reduced<br>Block<br>Chance',
    'Enemy Dodge Chance reduced by x% against this Skill':
        'reduced<br>Dodge<br>Chance',
    'Explosion deals x-y Base Fire damage per Fuse Charge':
        'Fire<br>Damage<br>per Fuse',
    'Freezes enemies as though dealing x% more Damage': '% more<br>Damage',
    'Gain Onslaught for x seconds on Killing a Shocked Enemy':
        'Onslaught<br>Duration',
    'Gain x% of Cold Damage as Extra Fire Damage':
        '+% of Cold<br>Damage<br>as Fire',
    'Gain x% of Physical Damage as Extra Chaos Damage':
        '% of Physical<br>Damage<br>as Chaos',
    'Gain x% of Physical Damage as Extra Lightning Damage':
        '% of Physical<br>Damage<br>as Lightning',
    'Gain x% of your Physical Damage as Extra Fire Damage':
        '% of Physical<br>Damage<br>as Fire',
    'Golems Grant x% increased Accuracy': 'increased<br>Accuracy',
    'Golems Grant x% increased Critical Strike Chance':
        'increased<br>Critical<br>Chance',
    'Golems Grant x% increased Damage': 'increased<br>Damage',
    'Golems grant x% additional Physical Damage Reduction':
        'Physical<br>Reduction',
    'Golems grant x Life Regenerated per second': 'Life<br>Regen',
    'Ignites for x% of Overkill Damage':
        'Ignites for x%<br> of Overkill<br>Damage',
    'Leeches x Life to you for each corpse consumed':
        'Life leeched<br>per Corpse',
    'Leeches x Mana to you for each corpse consumed':
        'Mana leeched<br>per Corpse',
    'Minions deal x% increased Physical Damage with Melee Attacks':
        'increased<br>Physical<br>Damage',
    'Minions deal x% less Damage': 'less<br>Damage',
    'Minions deal x% more Damage': 'more<br>Damage',
    'Minions have x% increased Attack Speed': 'increased<br>Attack<br>Speed',
    'Minions have x% increased Cast Speed': 'increased<br>Cast<br>Speed',
    'Minions have x% increased Movement Speed': 'increased<br>Movement<br>Speed',
    'Minions have x% less Energy Shield': 'less<br>Energy<br>Shield',
    'Minions have x% less Life': 'less<br>Life',
    'Minions have x% more Energy Shield': 'more<br>Energy<br>Shield',
    'Minions have x% more Life': 'more<br>Life',
    'Minions recover x Life when they Block': 'Life<br>on Block',
    'Minions\' Attacks deal x-y additional Physical Damage':
        'additional<br>Physical<br>Damage',
    'Penetrates x% Cold Resistance': '% Cold<br>Penetration',
    'Penetrates x% Fire Resistance': '% Fire<br>Penetration',
    'Penetrates x% Lightning Resistance': '% Lightning<br>Penetration',
    'Projectiles Split into x on hit': 'Projectiles<br>split into',
    'Shields break after x total Damage is prevented': 'Damage<br>absorbed',
    'Spell has x% less Cast Speed': 'less<br>Cast<br>Speed',
    'Summons x Skeleton Archers': '# Skeleton<br>Archers',
    'Summons x Skeleton Mages': '# Skeleton<br>Mages',
    'Summons x Skeleton Warriors': '# Skeleton<br>Warriors',
    'Supported Triggered Spells have x% increased Spell Damage':
        'increased<br>Spell<br>Damage',
    'Supported skills deal x% less Damage': 'less<br>Damage',
    'This Gem can only Support Skill Gems requiring Level x or lower':
        'maximum<br>Item<br>Level',
    'Totem lasts x seconds': 'Totem<br>Duration',
    'Totems and Minions summoned by this Skill have x% Cold Resistance':
        'Cold<br>Resistance',
    'Totems and Minions summoned by this Skill have x% Fire Resistance':
        'Fire<br>Resistance',
    'Totems and Minions summoned by this Skill have x% Lightning Resistance':
        'Lightning<br>Resistance',
    'Wall will be x units long': 'Length',
    'You and nearby allies deal x% more Lightning Damage with Spells':
        'more<br>Lightning<br>Damage',
    'You and nearby allies deal x-y additional Fire Damage with Attacks':
        'Fire Damage<br>with Attacks',
    'You and nearby allies deal x-y additional Fire Damage with Spells':
        'Fire Damage<br>with Spells',
    'You and nearby allies deal x-y additional Lightning Damage with Attacks':
        'Lightning Damage<br>with Attacks',
    'You and nearby allies gain x additional Energy Shield': 'Energy<br>Shield',
    'You and nearby allies gain x additional Evasion Rating': 'Evasion',
    'You and nearby allies gain x% additional Cold Resistance':
        'Cold<br>Resistance',
    'You and nearby allies gain x% additional Fire Resistance':
        'Fire<br>Resistance',
    'You and nearby allies gain x% additional Lightning Resistance':
        'Lightning<br>Resistance',
    'You and nearby allies gain x% additional maximum Cold Resistance':
        'max. Cold<br>Resistance',
    'You and nearby allies gain x% additional maximum Fire Resistance':
        'max. Fire<br>Resistance',
    'You and nearby allies gain x% additional maximum Lightning Resistance':
        'max. Lightning<br>Resistance',
    'You and nearby allies gain x% increased Attack Speed': 'Attack<br>Speed',
    'You and nearby allies gain x% increased Cast Speed': 'Cast<br>Speed',
    'You and nearby allies gain x% increased Movement Speed':
        'Movement<br>Speed',
    'You and nearby allies gain x% more Armour': 'more<br>Armour',
    'You and nearby allies gain x% of Physical Damage as Extra Cold Damage':
        '% of Physical<br>Damage<br>as Cold',
    'You and nearby allies gain x% to all Elemental Resistances':
        'Elemental<br>Resistance',
    'You and nearby allies regenerate x Mana per second':
        'Mana<br>regenerated',
    'You and nearby allies regenerate x% Life per second':
        '% Life<br>regenerated',
    'x Endurance Charges granted per one hundred nearby enemies':
        'Charge<br>per enemies',
    'x Life gained for each enemy hit by Supported Attack': 'Life<br>on hit',
    'x Life regenerated per second': 'Life<br>regenerated',
    'x Mana Regenerated per second': 'Mana<br>regenerated',
    'x additional Accuracy Rating': 'Accuracy',
    'x additional Armour': 'Armour',
    'x additional Arrows': 'extra<br>Arrows',
    'x additional Projectiles': '# Projectiles',
    'x to Melee Weapon Range': 'Range',
    'x to Level of Supported Active Skill Gems': '+Gem<br>Level',
    'x% Chance to Block': 'Block<br>Chance',
    'x% Chance to Block Spells': 'Spell Block<br>Chance',
    'x% Chance to Dodge Attacks': 'Dodge<br>Chance',
    'x% Chance to Dodge Spell Damage': 'Spell Dodge<br>Chance',
    'x% chance of Projectiles Piercing': 'Pierce<br>Chance',
    'x% chance to Cast linked Spells when you Crit an Enemy': 'Cast<br>Chance',
    'x% chance to Cast this Spell when Stunned': 'Cast<br>Chance>',
    'x% chance to Cast this Spell when you take a total of y Damage': 'Cast<br>Chance',
    'x% chance to Ignite enemies': 'Ignite<br>Chance',
    'x% chance to Knock Enemies Back on hit': 'Knockback<br>Chance',
    'x% chance to Shock enemies': 'Shock<br>Chance',
    'x% chance to cause Monsters to Flee when hit': 'Flee<br>Chance',
    'x% chance to gain a Frenzy Charge on Killing a Frozen Enemy':
        'Frenzy<br>Charge<br>Chance',
    'x% chance to gain a Power Charge on Critical Strike':
        'Power<br>Charge<br>Chance',
    'x% increased Area of Effect radius': 'increased<br>AoE Radius',
    'x% increased Attack Speed': 'increased<br>Attack Speed',
    'x% increased Blinding duration': 'increased<br>Blind<br>Duration',
    'x% increased Buff Duration per Endurance Charge':
        'increased<br>Duration<br>per Endurance<br>Charge',
    'x% increased Burning Damage': 'increased<br>Burning<br>Damage',
    'x% increased Cast Speed': 'increased<br>Cast<br>Speed',
    'x% increased Character Size': 'increased<br>Character<br>Size',
    'x% increased Chill Duration on enemies': 'increased<br>Chill<br>Duration',
    'x% increased Cooldown Recovery Speed for throwing Traps':
        'Cooldown<br>Recovery',
    'x% increased Critical Strike Chance': 'increased<br>Critical<br>Chance',
    'x% increased Curse Duration': 'Curse<br>Duration',
    'x% increased Damage': 'increased<br>Damage',
    'x% increased Damage per one hundred nearby Enemies':
        'increased<br>Damage<br>per enemy',
    'x% increased Damage with Poison': 'Poison<br>Damage',
    'x% increased Duration ': 'increased<br>Duration',
    'x% increased Life Leeched per second': 'increased<br>Life<br>leeched',
    'x% increased Life Leech rate': 'increased<br>Life<br>Leech<br>Rate',
    'x% increased Mana Leeched per second': 'increased<br>Mana<br>leeched',
    'x% increased Mana Leech rate': 'increased<br>Mana<br>Leech<br>Rate',
    'x% increased Melee Physical Damage':
        'increased<br>Melee<br>Physical<br>Damage',
    'x% increased Minion Damage': 'increased<br>Minion<br>Damage',
    'x% increased Minion Maximum Life': 'increased<br>Minion<br>Life',
    'x% increased Minion Movement Speed':
        'increased<br>Minion<br>Movement<br>Speed',
    'x% increased Movement Speed': 'increased<br>Movement<br>Speed',
    'x% increased Projectile Damage': 'increased<br>Projectile<br>Damage',
    'x% increased Projectile Speed': 'increased<br>Projectile<br>Speed',
    'x% increased Quantity of Items Dropped by Slain Enemies':
        'increased<br>Quantity',
    'x% increased Radius of Curses': 'Curse<br>Radius',
    'x% increased Rarity of Items Dropped by Slain Enemies':
        'increased<br>Rarity',
    'x% increased Spell Damage': 'increased<br>Spell<br>Damage',
    'x% increased Totem Placement speed': 'Placement<br>Speed',
    'x% increased effect of Aura': 'increased<br>Aura<br>Effect',
    'x% increased effect of Non-Curse Auras you Cast': 'Curse<br>effect',
    'x% increased maximum Life': 'increased<br>maximum<br>Life',
    'x% increased totem life': 'increased<br>Totem Life',
    'x% less Attack Speed': 'less<br>Attack<br>Speed',
    'x% less Damage': 'less<br>Damage',
    'x% less Damage to main target': 'less<br>Damage<br>(main)',
    'x% less Damage to other targets': 'less<br>Damage<br>(other)',
    'x% less Duration ': 'less<br>Duration',
    'x% less Fire Damage taken when Hit': 'less<br>Fire<br>Damage taken',
    'x% less Mine Damage': 'less<br>Mine<br>Damage',
    'x% less Physical Damage taken when Hit': 'less<br>Physical<br>Damage taken',
    'x% less Projectile Damage': 'less<br>Projectile<br>Damage',
    'x% less Projectile Speed': 'less<br>Projectile<br>Speed',
    'x% less Skill Effect Duration': 'less<br>Duration',
    'x% less Trap Damage': 'less<br>Trap<br>Damage',
    'x% more Area Damage': 'more<br>Area<br>Damage',
    'x% more Attack Speed while Totem is Active': 'more<br>Attack<br>Speed',
    'x% more Cast Speed': 'more<br>Cast<br>Speed',
    'x% more Chaos Damage': 'more<br>Chaos<br>Damage',
    'x% more Damage': 'more<br>Damage',
    'x% more Damage against Chilled Enemies': 'more<br>Damage<br>vs. chilled',
    'x% more Damage at Maximum Charge Distance':
        'more<br>Damage<br>at max. distance',
    'x% more Damage over Time': 'more DoT',
    'x% more Damage per Repeat': 'more<br>Damage<br>per repeat',
    'x% more Damage while Dead': 'more<br>Damage<br>while dead',
    'x% more Elemental Damage': 'more<br>Elmental<br>Damage',
    'x% more Melee Attack Speed': 'more<br>Melee<br>Attack<br>Speed',
    'x% more Melee Splash Radius': 'more<br>Radius',
    'x% more Melee Physical Damage': 'more<br>Melee<br>Physical<br>Damage',
    'x% more Melee Physical Damage against Bleeding Enemies':
        'more<br>Melee<br>Physical<br>Damage<br>vs. bleeding',
    'x% more Melee Physical Damage when on Full Life':
        'more<br>Melee<br>Physical<br>Damage<br>on full Life',
    'x% more Mine Damage': 'more<br>Mine<br>Damage',
    'x% more Physical Projectile Attack Damage':
        'more<br>Physical<br>Projectile<br>Attack<br>Damage',
    'x% more Projectile Damage': 'more<br>Projectile<br>Damage',
    'x% more Spell Damage': 'more<br>Spell<br>Damage',
    'x% more Trap Damage': 'more<br>Trap<br>Damage',
    'x% more Trap and Mine Damage': 'more<br>Trap & Mine<br>Damage',
    'x% more Weapon Elemental Damage': 'more<br>Weapon<br>Elemental<br>Damage',
    'x% reduced Curse Duration': 'reduced<br>Curse<br>Duration',
    'x% reduced Duration ': 'reduced<br>Duration',
    'x% reduced Enemy Stun Threshold': 'reduced<br>Stun<br>Threshold',
    'x% reduced Mana Cost': 'reduced<br>Mana<br>Cost',
    'x% reduced Movement Speed': 'reduced<br>Movement<br>Speed',
    'x% reduced Movement Speed per Nearby Enemy':
        'reduced<br>Movement<br>Speed<br>per nearby enemy',
    'x% reduced Skill Cooldown': 'reduced<br>Cooldown',
    'x% to Quality of Supported Active Skill Gems': '+% Gem<br>Quality',
    'x% to Critical Strike Chance': 'Critical<br>Chance',
    'x% to Critical Strike Multiplier': 'Critical<br>Multiplier',
}

# =============================================================================
# Warnings & Exceptions
# =============================================================================


class MissingAbbreviation(UserWarning):
    pass


# =============================================================================
# Classes
# =============================================================================

class GemWikiHandler(WikiHandler):
    regex_search = re.compile(
        '==gem level progression==',
        re.UNICODE | re.IGNORECASE | re.MULTILINE)

    regex_progression_replace = re.compile(
        '==gem level progression=='
        '.*?(?===[\w ]*==)',
        re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL)

    # This only works as long there aren't nested templates inside the infobox
    regex_infobox_search = re.compile(
        '\{\{Gem Infobox\n'
        '(?P<data>[^\}]*)'
        '\n\}\}',
        re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    regex_infobox_split = re.compile(
        '\|(?P<key>[\S]+)[\s]*=[\s]*(?P<value>[^|]*)',
        re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    def _find_page(self, page_name):
        page = self.pws.pywikibot.Page(self.site, page_name)

        if self.regex_search.search(page.text):
            return page
        else:
            console('Failed to find the progression on wiki page "%s"' % page_name, msg=Msg.warning)
            return None

    def handle_page(self, *a, row):
        page_name = row['wiki_page']
        console('Editing gem "%s"...' % page_name)
        page = self._find_page(page_name)
        if page is None:
            page = self._find_page('%s (support gem)' % page_name)

        if page is None:
            console('Can\'t find working wikipage. Skipping.', Msg.error)
            return

        infobox = self.regex_infobox_search.search(page.text)
        if not infobox:
            console('Can\'t find gem infobox on wikipage "%s"' % page_name,
                    msg=Msg.error)
            return

        for match in self.regex_infobox_split.finditer(infobox.group('data')):
            k = match.group('key')
            if k not in row['infobox'] and k != 'quality':
                row['infobox'][k] = match.group('value').strip('\n')

        infobox_text = ['{{Gem Infobox\n', ]
        for k, v in row['infobox'].items():
            infobox_text.append('|%s=%s\n' % (k, v))
        infobox_text.append('}}\n')

        new_text = page.text[:infobox.start()] + ''.join(infobox_text) + \
                   page.text[infobox.end():]

        row['lines'].insert(0, '==Gem level progression==\n\n')

        new_text = self.regex_progression_replace.sub(''.join(row['lines']), new_text)

        self.save_page(
            page=page,
            text=new_text,
            message='Gem export',
        )


class GemsHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser('gems', help='Gems Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        sub = self.parser.add_subparsers()

        parser = sub.add_parser(
            'export',
            help='Extracts the gem information'
        )
        self.add_default_parsers(
            parser=parser,
            cls=GemsParser,
            func=GemsParser.export,
            wiki_handler=GemWikiHandler(name='Gem Export'),
        )

        parser.add_argument(
            'gem',
            help='Name of the skill gem; can be specified multiple times',
            nargs='+',
        )


class GemsParser(BaseParser):
    _summon_map = {
        # Minions
        'Blink Arrow': [
            'Metadata/Monsters/Clone/MarauderClone',
        ],
        'Mirror Arrow': [
            'Metadata/Monsters/Double/DoubleMarauder',
        ],
        'Summon Chaos Golem': [
            'Metadata/Monsters/ChaosElemental/ChaosElementalSummoned',
        ],
        'Summon Flame Golem': [
            'Metadata/Monsters/FireElemental/FireElementalSummoned',
        ],
        'Summon Ice Golem': [
            'Metadata/Monsters/IceElemental/IceElementalSummoned',
        ],
        'Summon Stone Golem': [
            'Metadata/Monsters/RockGolem/RockGolemSummoned',
        ],
        'Raise Zombie': [
            'Metadata/Monsters/RaisedZombies/RaisedZombieStandard',
        ],
        'Summon Raging Spirit': [
            'Metadata/Monsters/SummonedSkull/SummonedSkull',
        ],
        'Summon Skeletons': [
            'Metadata/Monsters/RaisedSkeletons/RaisedSkeletonStandard',
        ],
        'Vaal Summon Skeletons': [
            'Metadata/Monsters/RaisedSkeletons/RaisedSkeletonMelee1Army',
            'Metadata/Monsters/RaisedSkeletons/RaisedSkeletonSpellcaster1Army',
            'Metadata/Monsters/RaisedSkeletons/RaisedSkeletonRanged1Army',
            'Metadata/Monsters/RaisedSkeletons/RaisedSkeletonGeneral2Army',
        ],
        # Totems
        # Compare: SkillTotemVariations.dat
        'Ancestral Protector': [
            'Metadata/Monsters/Totems/AncestorTotemTest',
        ],
        'Decoy Totem': [
            'Metadata/Monsters/Totems/TauntTotem',
        ],
        'Devouring Totem': [
            'Metadata/Monsters/Totems/ConsumeCorpseTotem',
        ],
        'Flame Totem': [
            'Metadata/Monsters/Totems/FireSprayTotem',
        ],
        'Rejuvenation Totem': [
            'Metadata/Monsters/Totems/LifeRegenTotem',
        ],
        'Searing Bond': [
            'Metadata/Monsters/Totems/SearingBondTotem',
        ],
        'Shockwave Totem': [
            'Metadata/Monsters/Totems/EarthquakeTotem',
        ],
        'Siege Ballista': [
            'Metadata/Monsters/Totems/SnipeTotem',
        ],
        # Support Totems
        'Ranged Attack Totem': [
            'Metadata/Monsters/Totems/StrengthTotem',
        ],
        'Spell Totem': [
            'Metadata/Monsters/Totems/StrengthTotem',
        ],
        # Animations
        'Animate Guardian': [
            'Metadata/Monsters/AnimatedItem/AnimatedArmour',
        ],
        'Animate Weapon': [
            'Metadata/Monsters/AnimatedItem/',
        ],
    }

    _regex_summon = re.compile('(summon|summoned|raise|raised) ', re.IGNORECASE)
    _regex_format = re.compile(
        '(?P<index>x|y|z)'
        '(?:[\W]*)'
        '(?P<tag>%|second)',
        re.IGNORECASE
    )
    
    # Core files we need to load
    _files = [
        'BaseItemTypes.dat',
        'SkillGems.dat',
        'Stats.dat',
    ]
    
    # Core translations we need
    _translations = [
        'stat_descriptions.txt',
        'gem_stat_descriptions.txt',
        'skill_stat_descriptions.txt',
        'active_skill_gem_stat_descriptions.txt',
    ]

    _cp_columns = (
        'Level', 'LevelRequirement', 'ManaMultiplier', 'CriticalStrikeChance',
        'ManaCost', 'DamageMultiplier', 'VaalSouls', 'VaalStoredUses',
        'Cooldown', 'StoredUses'
    )

    _column_map = OrderedDict((
        ('ManaCost', {
            'template': None, #'mana_cost',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('ManaMultiplier', {
            'template': 'mana_cost_multiplier',
            'default': 100,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('StoredUses', {
            'template': 'stored_uses',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('Cooldown', {
            'template': 'cooldown',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v/1000),
        }),
        ('VaalSouls', {
            'template': 'souls_per_use',
            'default': 0,
            'format': lambda v: '{0:n} / {1:n} / {2:n}'.format(v, v*1.5, v*2),
        }),
        ('VaalStoredUses', {
            'template': 'stored_uses',
            'default': 0,
            'format': lambda v: '{0:n}'.format(v),
        }),
        ('CriticalStrikeChance', {
            'template': 'critical_strike_chance',
            'default': None,
            'format': lambda v: '{0:n}%'.format(v/100),
        }),
        ('DamageEffectiveness', {
            'template': 'damage_effectiveness',
            'default': 0,
            'format': lambda v: '{0:n}%'.format(v+100),
        }),
        ('DamageMultiplier', {
            'template': None,
            'default': 0,
            'format': lambda v: '{0:n}%'.format(v/100+100),
        }),
    ))

    _monster_level_stats = (
        'display_minion_monster_level',
        'base_active_skill_totem_level',
        'totem_support_gem_level',
    )

    _attribute_map = {
        'Str': 'Strength',
        'Dex': 'Dexterity',
        'Int': 'Intelligence',
    }

    def _get_monster_data(self, gem_name):
        """
        Returns the first monster varieties info for the given gem name.

        Currently this is band-aid solution that depends on manually defining
        the monster type the gem summons.

        TODO / Known Issues:
        - Find out where in the game files the monster varieties is defined.

        :param gem_name: Name of the gem to find the monster for
        :type gem_name: str
        :return: List of MonsterVarieties.dat rows
        """

        if gem_name not in self._summon_map:
            console('No mapping defined for "%s" - fix me' % gem_name,
                    msg=Msg.error)
            return

        result = []

        for metaid in self._summon_map[gem_name]:
            try:
                result.append(
                    self.rr['MonsterVarieties.dat'].index['Id'][metaid]
                )
            except KeyError:
                console('Mapping "%s" invalid for "%s" - fix me' % (
                    metaid, gem_name), msg=Msg.error)
                return

        return result

    def _get_monster_stats(self, mv, minion_level):
        """
        Returns base damage, aspd and life for the given minion and level.

        :param mv: MonsterVarieties.dat row
        :param minion_level: Level of the minion
        :return: (damage_min, damage_max), aspd, life
        """
        default = self.rr['DefaultMonsterStats.dat'][minion_level-1]

        life = default['Life'] * mv['LifeMultiplier'] // 100
        damage_min = default['Damage'] * mv['DamageMultiplier'] // 100
        damage_max = damage_min * 7 // 3
        aspd = 1500 / mv['AttackSpeed']

        return (int(damage_min), int(damage_max)), aspd, life

    def _get_gem(self, name):
        """
        Attempts to find the skill gem and the corresponding base item.

        :param name: Name of the gem
        :return: BaseItemTypes.dat row, SkillGems.dat row
        """
        base_item_type = None
        for row in self.rr['BaseItemTypes.dat']:
            if row['Name'] == name:
                base_item_type = row
                break

        if base_item_type is None:
            console('The item "%s" was not found.' % name, msg=Msg.error)
            return

        skill_gem = None
        for row in self.rr['SkillGems.dat']:
            if row['BaseItemTypesKey'] == base_item_type:
                skill_gem = row
                break

        if skill_gem is None:
            console('The skill gem "%s" was not found. Is the item a skill?' % gem, msg=Msg.error)
            return

        return base_item_type, skill_gem

    def export(self, parsed_args):
        gems = {}
        for gem in parsed_args.gem:
            g = self._get_gem(gem)
            if g is not None:
                gems[gem] = g

        if not gems:
            console('No gems found. Exiting...')
            sys.exit(-1)

        console('Loading additional files...')
        self.rr['GrantedEffects.dat']
        self.rr['GrantedEffectsPerLevel.dat']
        self.rr['ItemExperiencePerLevel.dat']
        #self.rr['MonsterTypes.dat']
        #self.rr['MonsterVarieties.dat']

        console('Processing information...')

        r = ExporterResult()

        for gem in gems:
            # Unpack the references
            base_item_type, skill_gem = gems[gem]

            # TODO: Maybe catch empty stuff here?
            exp = 0
            exp_level = []
            exp_total = []
            for row in self.rr['ItemExperiencePerLevel.dat']:
                if row['BaseItemTypesKey'] == base_item_type:
                    exp_new = row['Experience']
                    exp_level.append(exp_new - exp)
                    exp_total.append(exp_new)
                    exp = exp_new

            if not exp_level:
                console('No experience progression found for "%s". Skipping.' % gem, msg=Msg.error)
                continue

            ge = skill_gem['GrantedEffectsKey']

            gepl = []
            for row in self.rr['GrantedEffectsPerLevel.dat']:
                if row['GrantedEffectsKey'] == ge:
                    gepl.append(row)

            if not gepl:
                console('No level progression found for "%s". Skipping.' % gem, msg=Msg.error)
                continue

            gepl.sort(key=lambda x:x['Level'])

            max_level = len(exp_total)-1

            is_aura = False
            is_minion = False
            is_totem = False
            is_bow = False
            tf = self.tc['skill_stat_descriptions.txt']
            for tag in skill_gem['GemTagsKeys']:
                if tag['Id'] == 'aura':
                    is_aura = True
                    tf = self.tc['aura_skill_stat_descriptions.txt']
                elif tag['Id'] == 'minion':
                    is_minion = True
                    #TODO one of?
                    #tf = self.tc['minion_skill_stat_descriptions.txt']
                    tf = self.tc['minion_attack_skill_stat_descriptions.txt']
                    tf = self.tc['minion_spell_skill_stat_descriptions.txt']
                elif tag['Id'] == 'curse':
                    tf = self.tc['curse_skill_stat_descriptions.txt']
                elif tag['Id'] == 'totem':
                    is_totem = True
                elif tag['Id'] == 'bow':
                    is_bow = True

            stat_ids = []
            stat_indexes = []
            for index, stat in enumerate(gepl[0]['StatsKeys']):
                stat_ids.append(stat['Id'])
                stat_indexes.append(index+1)

            # Handle special stats. Can only have one
            minion_stat = None
            for stat in self._monster_level_stats:
                if stat in stat_ids:
                    minion_stat = stat
                    break

            # Special case: SRS
            if gem == 'Summon Raging Spirit':
                minion_stat = -1

            if minion_stat:
                monster_varieties = self._get_monster_data(gem)
                # No result->skip
                # message will be handled by _get_monster_data
                if monster_varieties is None:
                    continue

            # reformat the datas we need
            level_data = []
            stat_key_order = {
                'stats': OrderedDict(),
                'qstats': OrderedDict(),
            }

            for i, row in enumerate(gepl):
                data = defaultdict()

                tr = tf.get_translation(
                    tags=[r['Id'] for r in row['StatsKeys']],
                    values=row['StatValues'],
                    full_result=True,
                )
                data['_tr'] = tr

                qtr = tf.get_translation(
                    tags=[r['Id'] for r in row['Quality_StatsKeys']],
                    values=row['Quality_Values'],
                    full_result=True,
                )
                data['_qtr'] = qtr

                data['stats'] = {}
                data['qstats'] = {}

                for result, key in (
                        (tr, 'stats'),
                        (qtr, 'qstats'),
                ):
                    for j, stats in enumerate(result.found_ids):
                        k = '__'.join(stats)
                        stat_key_order[key][k] = None
                        data[key]['__'.join(stats)] = {
                            'line': result.found_lines[j],
                            'stats': stats,
                            'values': result.values[j],
                        }
                    for stat, value in result.missing:
                        warnings.warn('Missing translation for %s' % stat)
                        stat_key_order[key][k] = None
                        data[key][stat] = {
                            'line': '',
                            'stats': [stat, ],
                            'values': [value, ],
                        }

                try:
                    data['exp'] = exp_level[i]
                    data['exp_total'] = exp_total[i]
                except IndexError:
                    pass

                if minion_stat:
                    mindata = {}
                    for mv in monster_varieties:
                        if minion_stat == -1:
                            mindata['minion_level'] = row['LevelRequirement']
                        else:
                            try:
                                mindata['minion_level'] = tr.values[
                                     tr.found_ids.index(minion_stat)]
                            except (IndexError, ValueError):
                                mindata['minion_level'] = tr.missing_values[
                                     tr.missing_ids.index(minion_stat)]

                        stats = self._get_monster_stats(mv, mindata['minion_level'])
                        mindata['minion_dmg'] = stats[0]
                        mindata['minion_aspd'] = stats[1]
                        mindata['minion_life'] = stats[2]

                for column in self._cp_columns:
                    data[column] = row[column]

                level_data.append(data)

            # Find static & dynamic stats..

            static = {
                'columns': set(self._cp_columns),
                'stats': OrderedDict(stat_key_order['stats']),
                'qstats': OrderedDict(stat_key_order['qstats']),
            }
            dynamic = {
                'columns': set(),
                'stats': OrderedDict(),
                'qstats': OrderedDict(),
            }
            last = level_data[0]
            for data in level_data[1:]:
                for key in list(static['columns']):
                    if last[key] != data[key]:
                        static['columns'].remove(key)
                        dynamic['columns'].add(key)
                for stat_key in ('stats', 'qstats'):
                    for key in list(static[stat_key]):
                        # Remove monster level stats
                        if key in self._monster_level_stats:
                            del static[stat_key][key]
                        if key not in last[stat_key]:
                            continue
                        if key not in data[stat_key]:
                            continue

                        if last[stat_key][key]['values'] != data[stat_key][key]['values']:
                            del static[stat_key][key]
                            dynamic[stat_key][key] = None

                last = data

            # Remove columns that are zero/default
            for key in list(static['columns']):
                if level_data[0][key] == 0:
                    static['columns'].remove(key)


            #
            # Output handling for gem infobox
            #
            infobox = OrderedDict()

            infobox['name'] = base_item_type['Name']

            infobox['type'] = base_item_type['ItemClassesKey']['Id']

            attrs = [(text, skill_gem[k]) for k, text in
                     self._attribute_map.items() if skill_gem[k]]
            attrs.sort(key=lambda row: row[1])
            infobox['attributes'] = ', '.join(['[[%s]]' % a[0] for a in attrs])

            infobox['keywords'] = ', '.join(
                ['[[%s]]' % gtag['Tag'] for gtag in
                 skill_gem['GemTagsKeys'] if gtag['Tag']]
            )

            infobox['required_level'] = level_data[0]['LevelRequirement']

            ae = gepl[0]['ActiveSkillsKey']
            if ae:
                infobox['cast_time'] = '{0:n}s'.format(ae['CastTime'] / 1000)
                infobox['description'] = ae['Description']
            else:
                infobox['cast_time'] = ''
                infobox['description'] = ''

            def infobox_set_range(key, column):
                cdata = self._column_map[column]

                if key is None:
                    infobox[key] = ''
                    return

                if column in dynamic['columns']:
                    infobox[key] = '%s to %s' % (
                        cdata['format'](level_data[0][column]),
                        cdata['format'](level_data[max_level][column])
                    )
                elif column in static['columns']:
                    if level_data[0][column] == cdata['default']:
                        infobox[key] = ''
                        return

                    infobox[key] = cdata['format'](level_data[0][column])

            if is_aura:
                infobox_set_range('mana_reserved', 'ManaCost')
                infobox['mana_cost'] = ''
            else:
                infobox['mana_reserved'] = ''
                infobox_set_range('mana_cost', 'ManaCost')

            for column, data in self._column_map.items():
                infobox_set_range(data['template'], column)

            # Quality stats
            lines = []
            for key in static['qstats']:
                stat_dict = level_data[0]['qstats'][key]
                values = []
                for v in stat_dict['values']:
                    v /= 50
                    values.append(int(v) if v.is_integer() else v)
                lines.extend(tf.get_translation(stat_dict['stats'], values))


            infobox['quality20'] = '<br>'.join(lines)

            # Normal stats
            lines = []
            for key in stat_key_order['stats']:
                if key in static['stats']:
                    line = level_data[0]['stats'][key]['line']
                elif key in dynamic['stats']:
                    stat_dict = level_data[0]['stats'][key]
                    stat_dict_max = level_data[max_level]['stats'][key]
                    values = []
                    for j, value in enumerate(stat_dict['values']):
                        values.append((value, stat_dict_max['values'][j]))

                    # Should only be one
                    line = tf.get_translation(stat_dict['stats'], values)[0]

                if line:
                    lines.append(line)

            for j, line in enumerate(lines):
                infobox['modifier' + str(j+1)] = line

            # Offset one because wiki starts 1
            # And offset another one to avoid overriding the last modifier
            for j in range(j+2, 9):
                infobox['modifier' + str(j)] = ''

            #print([(c, gepl[0][c]) for c in self.rr['GrantedEffectsPerLevel.dat'].columns_data if c.startswith('Un')])

            #
            # Output handling for progression
            #
            out = []

            if minion_stat and is_minion:
                out.append('Please help to verify the monster stats. In particar maximum base damage and base attack speed.')

            #
            # Header
            #
            out.append('{{GemLevelTable\n')
            attributes = ['Str', 'Dex', 'Int']
            for attr in tuple(attributes):
                if skill_gem[attr]:
                    out.append('| %s=yes\n' % attr.lower())
                else:
                    attributes.remove(attr)

            offset = 0
            def add_column(text):
                nonlocal offset
                offset += 1
                out.append('| c%s=%s\n' % (offset, text))

            # Column handling
            if 'ManaCost' in dynamic['columns']:
                text = 'Mana<br>Reserved' if is_aura else 'Mana<br>Cost'
                add_column(text)

            for key, text in {
                'CriticialStrikeChance': 'Critical<br>Strike<br>Chance',
                'ManaMultiplier': 'Mana<br>Multiplier',
                'DamageMultiplier': 'Damage<br>Multiplier',
            }.items():
                if key in dynamic['columns']:
                    add_column(text)

            # Stat handling
            formatting_indexes = {'stats': {}, 'qstats': {}}
            for stat_key in ('stats', 'qstats'):
                for key in list(dynamic[stat_key]):
                    for row in reversed(level_data):
                        if key not in row[stat_key]:
                            continue

                        data = row[stat_key][key]

                        line = tf.get_translation(
                            data['stats'],
                            data['values'],
                            use_placeholder=True
                        )
                        if not line:
                            # Remove missing translation
                            del dynamic[stat_key][key]
                            continue
                        else:
                            line = line[0]

                        formatting_indexes[stat_key][key] = [{
                            '%': False,
                            'second': False,
                        } for i in range(0, 3)]

                        for match in self._regex_format.finditer(line):
                            index = 'xyz'.index(match.group('index'))
                            formatting_indexes[stat_key][key][index][match.group('tag')] = True

                        if line in abbreviations:
                            abbr = abbreviations[line]
                            if abbr:
                                line = '{{Abbr|%s|%s}}' % (abbr, line)
                            else:
                                warnings.warn(line, MissingAbbreviation)
                        else:
                            warnings.warn(line, MissingAbbreviation)

                        add_column(line)
                        break

            # Monster handling
            if minion_stat:
                if is_minion:
                    text = 'Minion<br>Level'
                elif is_totem:
                    text = 'Totem<br>Level'
                else:
                    text = 'Monster<br>Level'
                add_column(text)
                for mv in monster_varieties:
                    # Shorten the name
                    name = self._regex_summon.sub('', mv['Name'])
                    name = name.replace(' ', '<br>')
                    # Only hp for totems and clone/mirror arrow
                    if is_minion and not is_bow:
                        add_column('%s<br>Base<br>Damage' % name)
                        add_column('%s<br>Base<br>Attack Speed' % name)
                    offset += 1
                    add_column('%s<br>Base<br>Life' % name)

            out.append('}}\n')

            # Body

            def add_line(text=''):
                out.append('| %s\n' % text)

            if base_item_type['ItemClassesKey']['Name'] == 'Active Skill Gems':
                gtype = GemTypes.active
            elif base_item_type['ItemClassesKey']['Name'] == 'Support Skill Gems':
                gtype = GemTypes.support

            for i, row in enumerate(level_data):
                out.append('|- \n')
                out.append('! %s\n' % row['Level'])
                add_line(row['LevelRequirement'])

                for attr in attributes:
                    # Gems with base level > 21 are not possible
                    if row['Level'] > 21:
                        add_line()
                    else:
                        add_line(gem_stat_requirement(
                            level=row['LevelRequirement'],
                            gtype=gtype,
                            multi=skill_gem[attr],
                        ))

                # Column handling
                for column in ('ManaCost', 'CriticialStrikeChance',
                               'ManaMultiplier', 'DamageMultiplier'):
                    if column in dynamic['columns']:
                        add_line(self._column_map[column]['format'](row[column]))

                # Stat handling
                for stat_key in ('stats', 'qstats'):
                    for key in stat_key_order[stat_key]:
                        if key not in dynamic[stat_key]:
                            continue

                        values_formatted = []
                        for j, value in enumerate(row[stat_key][key]['values']):
                            if isinstance(value, float):
                                #if value_fmt.is_integer():
                                #    value_fmt = '{0:n}'.format(value_fmt)
                                value_fmt = '{0:.2f}'.format(value)
                            else:
                                value_fmt = '{0:n}'.format(value)


                            fmt = formatting_indexes[stat_key][key]

                            if fmt[j]['%']:
                                value_fmt += '%'
                            elif fmt[j]['second']:
                                value_fmt += 's'

                            values_formatted.append(value_fmt)

                        add_line('&ndash;'.join(values_formatted))


                # Monster handling
                if minion_stat:
                    if minion_stat != -1:
                        minion_level = row['stats'][minion_stat]['values'][0]
                    else:
                        minion_level = row['LevelRequirement']
                    add_line(minion_level)
                    for mv in monster_varieties:
                        dmg, aspd, life = self._get_monster_stats(mv, minion_level)
                        if is_minion and not is_bow:
                            add_line('{0:,d}&ndash;{1:,d}'.format(*dmg))
                            add_line('{0:.2f}'.format(aspd))
                        add_line('{0:,d}'.format(life))

                for exp in (exp_level, exp_total):
                    try:
                        # Format in a readable manner
                        add_line('{0:,d}'.format(exp[i]))
                    except IndexError:
                        add_line('{{n/a}}')

            out.append('|}\n')

            r.add_result(
                lines=out,
                out_file='level_progression_%s.txt' % gem,
                wiki_page=base_item_type['Name'],
                infobox=infobox,
            )

        return r