"""
Path     PyPoE/cli/exporter/wiki/parser/gems.py
Name     Wiki gems exporter
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO


http://pathofexile.gamepedia.com


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import sys
import warnings

# Self
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.poe.file.translations import TranslationFileCache
from PyPoE.poe.sim.formula import gem_stat_requirement, GemTypes
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki.handler import *

# =============================================================================
# Data
# =============================================================================

# Abbreviations
abbreviations = {
    'Adds an additional Projectile': 'Extra<br>Projectiles',
    'Adds x-y Cold Damage to Attacks': 'Cold<br>Damage',
    'Adds x-y Cold Damage to Spells': 'Cold<br>Damage',
    'Adds x-y Lightning Damage to Attacks': 'Lightning<br>Damage',
    'Adds x-y Lightning Damage to Spells': 'Lightning<br>Damage',
    'Base duration is x seconds': 'Base<br>Duration',
    'Can deal x-y base Cold damage': 'Cold<br>Damage',
    'Can deal x-y base Fire damage': 'Fire<br>Damage',
    'Can deal x-y base Lightning damage': 'Lightning<br>Damage',
    'Can summon up to x Skeletons at a time': '# Skeletons',
    'Can use Items requiring up to level x': 'max.<br>Item<br>Level',
    'Chains x Times': '# Chains',
    'Creates Corpses up to Level x': 'Corpse<br>Level',
    'Cursed enemies are x% slower': '% slower',
    'Cursed enemies deal x% less Damage': 'less<br>Damage',
    'Cursed enemies grant x Life when Hit by Attacks': 'Life per Hit<br>with Attacks',
    'Cursed enemies grant x Life when Killed': 'Life<br>per Kill',
    'Cursed enemies grant x Mana when Hit by Attacks': 'Mana per Hit<br>with Attacks',
    'Cursed enemies grant x Mana when Killed': 'Mana<br>per Kill',
    'Cursed enemies grant x% increased Attack Speed on Melee hit': 'Attack Speed<br>per Melee hit',
    'Cursed enemies grant x% more Physical Melee Damage on Melee hit': 'more<br>Physical Damage<br>per Melee hit',
    'Cursed enemies have a x% chance to grant a Frenzy Charge when slain': 'Frenzy<br>Charge<br>Chance',
    'Cursed enemies have a x% chance to grant a Power Charge when slain': 'Power<br>Charge<br>Chance',
    'Cursed enemies have a x% chance to grant an Endurance Charge when slain': 'Endurance<br>Charge<br>Chance',
    'Cursed enemies have an additional x% chance to be Stunned': 'Stun<br>Chance',
    'Cursed enemies have an additional x% chance to receive a Critical Strike': 'Crit<br>Chance',
    'Cursed enemies have x% chance to be Frozen by Cold Damage': 'Freeze<br>Chance',
    'Cursed enemies have x% chance to be Ignited by Fire Damage': 'Ignite<br>Chance',
    'Cursed enemies have x% chance to be Shocked by Lightning Damage': 'Shock<br>Chance',
    'Cursed enemies have x% less Evasion': 'less<br>Evasion',
    'Cursed enemies have x% reduced Accuracy Rating': 'reduced<br>Accuracy',
    'Cursed enemies have x% reduced Stun Recovery': 'reduced<br>Stun Recover<',
    'Cursed enemies lose x% Cold Resistance': 'reduced<br>Cold<br>Resistance',
    'Cursed enemies lose x% Elemental Resistances': 'reduced<br>Elemental<br>Resistance',
    'Cursed enemies lose x% Fire Resistance': 'reduced<br>Fire<br>Resistance',
    'Cursed enemies lose x% Lightning Resistance': 'reduced<br>Lightning<br>Resistance',
    'Cursed enemies take x% increased Damage from Projectiles': 'increased<br>Projectile<br>Damage',
    'Cursed enemies take x% increased Physical damage': 'increased<br>Physical<br>Damage',
    'Cursed enemies take x% more extra damage from Critical Strikes': 'more<br>Critical<br>Damage',
    'Deals x Base Chaos Damage per second': 'Chaos<br>Damage<br>per sec',
    'Deals x Fire Damage per second': 'Fire<br>Damage<br>per sec',
    'Deals x% of Base Damage': '% Base<br>Damage',
    'Deals x-y Chaos Damage': 'Chaos<br>Damage',
    'Deals x-y Cold Damage': 'Cold<br>Damage',
    'Deals x-y Fire Damage': 'Fire<br>Damage',
    'Deals x-y Lightning Damage': 'Lightning<br>Damage',
    'Deals x-y Physical Damage': 'Physical<br>Damage',
    'Deals x-y base Cold Damage per Frenzy Charge': 'Cold<br>Damage<br>per Frenzy<br>Charge',
    'Deals x-y base Fire Damage per Endurance Charge': 'Fir<br>Damage<br>per Endurance<br>Charge',
    'Deals x-y base Lightning Damage per Power Charge': 'Lightning<br>Damage<br>per Power<br>Charge',
    'Enemy Block Chance reduced by x% against this Skill': 'reduced<br>Block<br>Chance',
    'Enemy Dodge Chance reduced by x% against this Skill': 'reduced<br>Dodge<br>Chance',
    'Explosion deals x-y Base Fire damage per Fuse Charge': 'Fire<br>Damage<br>per Fuse',
    'Freezes enemies as though dealing x% more Damage': '% more<br>Damage',
    'Gain Onslaught for x seconds on Killing a Shocked Enemy': 'Onslaught<br>Duration',
    'Gain x% of Cold Damage as Extra Fire Damage': '+% of Cold<br>Damage<br>as Fire',
    'Gain x% of Physical Damage as Extra Chaos Damage': '% of Physical<br>Damage<br>as Chaos',
    'Gain x% of Physical Damage as Extra Lightning Damage': '% of Physical<br>Damage<br>as Lightning',
    'Gain x% of your Physical Damage as Extra Fire Damage': '% of Physical<br>Damage<br>as Fire',
    'Golems Grant x% increased Accuracy': 'increased<br>Accuracy',
    'Golems Grant x% increased Critical Strike Chance': 'increased<br>Critical<br>Chance',
    'Golems Grant x% increased Damage': 'increased<br>Damage',
    'Golems grant x% additional Physical Damage Reduction': 'Physical<br>Reduction',
    'Ignites for x% of Overkill Damage': 'Ignites for x%<br> of Overkill<br>Damage',
    'Leeches x Life to you for each corpse consumed': 'Life leeched<br>per Corpse',
    'Leeches x Mana to you for each corpse consumed': 'Mana leeched<br>per Corpse',
    'Minions deal x% increased Physical Damage with Melee Attacks': 'increased<br>Physical<br>Damage',
    'Minions deal x% less Damage': 'less<br>Damage',
    'Minions deal x% more Damage': 'more<br>Damage',
    'Minions have x% increased Attack Speed': 'increased<br>Attack<br>Speed',
    'Minions have x% increased Cast Speed': 'increased<br>Cast<br>Speed',
    'Minions have x% increased Movement Speed': 'increased<br>Movement<br>Speed',
    'Minions have x% less Energy Shield': 'less<br>Energy<br>Shield',
    'Minions have x% less Life': 'less<br>Life',
    'Minions recover x Life when they Block': 'Life<br>on Block',
    'Minions\' Attacks deal x-y additional Physical Damage': 'additional<br>Physical<br>Damage',
    'Penetrates x% Cold Resistance': '% Cold<br>Penetration',
    'Penetrates x% Fire Resistance': '% Fire<br>Penetration',
    'Penetrates x% Lightning Resistance': '% Lightning<br>Penetration',
    'Shields break after x total Damage is prevented': 'Damage<br>absorbed',
    'Summons x Skeleton Archers': '# Skeleton<br>Archers',
    'Summons x Skeleton Mage': '# Skeleton<br>Mages',
    'Summons x Skeleton Warriors': '# Skeleton<br>Warriors',
    'Supported Triggered Spells have x% increased Spell Damage': 'increased<br>Spell<br>Damage',
    'Supported skills deal x% less Damage': 'less<br>Damage',
    'This Gem can only Support Skill Gems requiring Level x or lower': 'maximum<br>Item<br>Level',
    'Totem lasts x seconds': 'Totem<br>Duration',
    'Totems and Minions summoned by this Skill have x% Cold Resistance': 'Cold<br>Resistance',
    'Totems and Minions summoned by this Skill have x% Fire Resistance': 'Fire<br>Resistance',
    'Totems and Minions summoned by this Skill have x% Lightning Resistance': 'Lightning<br>Resistance',
    'Wall will be x units long': 'Length',
    'You and nearby allies deal x% more Lightning Damage with Spells': 'more<br>Lightning<br>Damage',
    'You and nearby allies deal x-y additional Fire Damage with Attacks': 'Fire Damage<br>with Attacks',
    'You and nearby allies deal x-y additional Fire Damage with Spells': 'Fire Damage<br>with Spells',
    'You and nearby allies deal x-y additional Lightning Damage with Attacks': 'Lightning Damage<br>with Attacks',
    'You and nearby allies gain x additional Energy Shield': 'Energy<br>Shield',
    'You and nearby allies gain x additional Evasion Rating': 'Evasion',
    'You and nearby allies gain x% additional Cold Resistance': 'Cold<br>Resistance',
    'You and nearby allies gain x% additional Fire Resistance': 'Fire<br>Resistance',
    'You and nearby allies gain x% additional Lightning Resistance': 'Lightning<br>Resistance',
    'You and nearby allies gain x% additional maximum Cold Resistance': 'max. Cold<br>Resistance',
    'You and nearby allies gain x% additional maximum Fire Resistance': 'max. Fire<br>Resistance',
    'You and nearby allies gain x% additional maximum Lightning Resistance': 'max. Lightning<br>Resistance',
    'You and nearby allies gain x% increased Attack Speed': 'Attack<br>Speed',
    'You and nearby allies gain x% increased Cast Speed': 'Cast<br>Speed',
    'You and nearby allies gain x% increased Movement Speed': 'Movement<br>Speed',
    'You and nearby allies gain x% more Armour': 'more<br>Armour',
    'You and nearby allies gain x% of your Physical Damage as Extra Cold Damage': '% of Physical<br>Damage<br>as Cold',
    'You and nearby allies gain x% to all Elemental Resistances': 'Elemental<br>Resistance',
    'You and nearby allies regenerate x Mana per second': 'Mana<br>regenerated',
    'You and nearby allies regenerate x% Life per second': '% Life<br>regenerated',
    'x Endurance Charges granted per one hundred nearby enemies': 'Charge<br>per enemies',
    'x Life gained for each enemy hit by Supported Attack': 'Life<br>on hit',
    'x Life regenerated per second': 'Life<br>regenerated',
    'x Mana Regenerated per second': 'Mana<br>regenerated',
    'x additional Accuracy Rating': 'Accuracy',
    'x additional Armour': 'Armour',
    'x additional Arrows': 'extra<br>Arrows',
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
    'x% chance to gain a Frenzy Charge on Killing a Frozen Enemy': 'Frenzy<br>Charge<br>Chance',
    'x% chance to gain a Power Charge on Critical Strike': 'Power<br>Charge<br>Chance',
    'x% increased Area of Effect radius': 'increased<br>AoE Radius',
    'x% increased Attack Speed': 'increased<br>Attack Speed',
    'x% increased Blinding duration': 'increased<br>Blind<br>Duration',
    'x% increased Buff Duration Per Endurance Charge': 'increased<br>Duration<br>per Endurance<br>Charge',
    'x% increased Burning Damage': 'increased<br>Burning<br>Damage',
    'x% increased Cast Speed': 'increased<br>Cast<br>Speed',
    'x% increased Character Size': 'increased<br>Character<br>Size',
    'x% increased Chill Duration on enemies': 'increased<br>Chill<br>Duration',
    'x% increased Critical Strike Chance': 'increased<br>Critical<br>Chance',
    'x% increased Critical Strike Multiplier': 'increased<br>Critical<br>Multiplier',
    'x% increased Damage': 'increased<br>Damage',
    'x% increased Damage per one hundred nearby Enemies': 'increased<br>Damage<br>per enemy',
    'x% increased Duration ': 'increased<br>Duration',
    'x% increased Life Leeched per second': 'increased<br>Life<br>leeched',
    'x% increased Mana Leeched per second': 'increased<br>Mana<br>leeched',
    'x% increased Melee Physical Damage': 'increased<br>Melee<br>Physical<br>Damage',
    'x% increased Minion Damage': 'increased<br>Minion<br>Damage',
    'x% increased Minion Maximum Life': 'increased<br>Minion<br>Life',
    'x% increased Minion Movement Speed': 'increased<br>Minion<br>Movement<br>Speed',
    'x% increased Movement Speed': 'increased<br>Movement<br>Speed',
    'x% increased Projectile Damage': 'increased<br>Projectile<br>Damage',
    'x% increased Projectile Speed': 'increased<br>Projectile<br>Speed',
    'x% increased Quantity of Items Dropped by Slain Enemies': 'increased<br>Quantity',
    'x% increased Rarity of Items Dropped by Slain Enemies': 'increased<br>Rarity',
    'x% increased Spell Damage': 'increased<br>Spell<br>Damage',
    'x% increased effect of Aura': 'increased<br>Aura<br>Effect',
    'x% increased maximum Life': 'increased<br>maximum<br>Life',
    'x% increased totem life': 'increased<br>Totem Life',
    'x% less Damage': 'less<br>Damage',
    'x% less Damage to main target': 'less<br>Damage<br>(main)',
    'x% less Damage to other targets': 'less<br>Damage<br>(other)',
    'x% less Fire Damage taken when Hit': 'less<br>Fire<br>Damage taken',
    'x% less Physical Damage taken when Hit': 'less<br>Physical<br>Damage taken',
    'x% less Projectile Damage': 'less<br>Projectile<br>Damage',
    'x% less Projectile Speed': 'less<br>Projectile<br>Speed',
    'x% less Skill Effect Duration': 'less<br>Duration',
    'x% more Area Damage': 'more<br>Area<br>Damage',
    'x% more Cast Speed': 'more<br>Cast<br>Speed',
    'x% more Damage against Chilled Enemies': 'more<br>Damage<br>vs. chilled',
    'x% more Damage at Maximum Charge Distance': 'more<br>Damage<br>at max. distance',
    'x% more Damage per Repeat': 'more<br>Damage<br>per repeat',
    'x% more Damage while Dead': 'more<br>Damage<br>while dead',
    'x% more Melee Attack Speed': 'more<br>Melee<br>Attack<br>Speed',
    'x% more Melee Physical Damage': 'more<br>Melee<br>Physical<br>Damage',
    'x% more Melee Physical Damage against Bleeding Enemies': 'more<br>Melee<br>Physical<br>Damage<br>vs. bleeding',
    'x% more Melee Physical Damage when on Full Life': 'more<br>Melee<br>Physical<br>Damage<br>on full Life',
    'x% more Mine Damage': 'more<br>Mine<br>Damage',
    'x% more Physical Projectile Attack Damage': 'more<br>Physical<br>Projectile<br>Attack<br>Damage',
    'x% more Projectile Damage': 'more<br>Projectile<br>Damage',
    'x% more Spell Damage': 'more<br>Spell<br>Damage',
    'x% more Trap Damage': 'more<br>Trap<br>Damage',
    'x% more Trap and Mine Damage': 'more<br>Trap & Mine<br>Damage',
    'x% more Weapon Elemental Damage': 'more<br>Weapon<br>Elemental<br>Damage',
    'x% reduced Curse Duration': 'reduced<br>Curse<br>Duration',
    'x% reduced Enemy Stun Threshold': 'reduced<br>Stun<br>Threshold',
    'x% reduced Mana Cost': 'reduced<br>Mana<br>Cost',
    'x% reduced Movement Speed': 'reduced<br>Movement<br>Speed',
    'x% reduced Movement Speed per Nearby Enemy': 'reduced<br>Movement<br>Speed<br>per nearby enemy',
    'x% to Quality of Supported Active Skill Gems': '+% Gem<br>Quality',
}

# =============================================================================
# Warnings & Exceptions
# =============================================================================


class MissingAbbreviation(UserWarning):
    pass


# =============================================================================
# Classes
# =============================================================================

class GemsHandler(ExporterHandler):

    regex_search = re.compile(
        '==gem level progression==',
        re.UNICODE | re.IGNORECASE | re.MULTILINE)

    regex_replace = re.compile(
        '==gem level progression=='
        '.*?(?===[\w ]*==)',
        re.UNICODE | re.IGNORECASE | re.MULTILINE | re.DOTALL)

    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser('gems', help='Gems Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        sub = self.parser.add_subparsers()

        parser = sub.add_parser(
            'level_progression',
            help='Extracts the level progression'
        )
        self.add_default_parsers(
            parser=parser,
            cls=GemsParser,
            func=GemsParser.level_progression,
            wiki_handler=self.wiki_handler,
        )
        self.add_gem_arg(parser)

        '''parser = sub.add_parser(
            'graph',
            help='Extract the warbands movement graph.',
        )
        self.add_default_parsers(
            parser=parser,
            cls=GemsParser,
            handler=GemsParser.graph,
        )
        self.add_gem_arg(parser)
        parser.add_argument(
            'type',
            choices=('map', 'normal'),
            help='The type of the graph file to extract.',
        )
        parser.add_argument(
            '-f', '--format',
            choices=('svg', 'pdf', 'png'),
            default='svg',
            help='File format to use when extracting.',
        )'''

    def _find_page(self, pws, page_name, site):
        page = pws.pywikibot.Page(site, page_name)

        if self.regex_search.search(page.text):
            return page
        else:
            console('Failed to find the progression on wiki page "%s"' % page_name, msg=Msg.warning)
            return None

    def add_gem_arg(self, parser):
        parser.add_argument(
            'gem',
            help='Name of the skill gem; can be specified multiple times',
            nargs='+',
        )

    def wiki_handler(self, pws, result):
        site = pws.get_site()
        for row in result:
            page_name = row['wiki_page']
            console('Editing gem "%s"...' % page_name)
            page = self._find_page(pws, page_name, site)
            if page is None:
                page = self._find_page(pws, '%s (support gem)' % page_name, site)

            if page is None:
                console('Can\'t find working wikipage. Skipping.', Msg.error)
                continue

            row['lines'].insert(0, '==Gem level progression==\n\n')

            page.text = self.regex_replace.sub(''.join(row['lines']), page.text)
            page.save(pws.get_edit_message('Gem level progression'))


class GemsParser(object):

    _summon_map = {
        # Minions
        'Raise Zombie': ['RaisedZombie', ],
        'Blink Arrow': ['Clone', ],
        'Mirror Arrow': ['Double', ],
        'Summon Chaos Golem': ['ChaosGolemSummoned', ],
        'Summon Flame Golem': ['FlameGolemSummoned', ],
        'Summon Ice Golem': ['IceGolemSummoned', ],
        'Summon Raging Spirit': ['SummonedSkull', ],
        'Summon Skeletons': ['RaisedSkeleton', ],
        'Vaal Summon Skeletons': [
            'RaisedSkeletonMeleeVaal',
            'RaisedSkeletonRangedVaal',
            'RaisedSkeletonSpellcasterVaal',
            'RaisedSkeletonGeneralVaal',
            'RaisedSkeletonGeneralRangedVaal',
        ],
        # Totems
        'Decoy Totem': ['TauntTotem', ],
        'Devouring Totem': ['Totem', ],
        'Flame Totem': ['Totem', ],
        'Rejuvenation Totem': ['Totem', ],
        'Searing Bond': ['Totem', ],
        'Shockwave Totem': ['Totem', ],
        # Other
        'Animate Guardian': ['AnimatedArmour', ],
        'Animate Weapon': ['AnimatedWeapon', ],
    }

    _regex_summon = re.compile('(summon|summoned|raise|raised) ', re.IGNORECASE)
    _regex_format = re.compile(
        '(?P<index>x|y|z)'
        '(?:[\W]*)'
        '(?P<tag>%|second)',
        re.IGNORECASE
    )

    def __init__(self, **kwargs):
        self.desc_path = kwargs['desc_path']
        self.data_path = kwargs['data_path']

        self.opt = {
            'use_dat_value': False,
        }

        self.reader = RelationalReader(
            self.data_path,
            files=[
                'BaseItemTypes.dat',
                'SkillGems.dat',
                'Stats.dat'
            ],
            options=self.opt,
        )

        self.translation_cache = TranslationFileCache(kwargs['base_path'])
        # Touch files we'll need
        self.translation_cache.get_file('Metadata/stat_descriptions.txt')
        self.translation_cache.get_file('Metadata/gem_stat_descriptions.txt')
        self.translation_cache.get_file('Metadata/skill_stat_descriptions.txt')
        self.translation_cache.get_file('Metadata/active_skill_gem_stat_descriptions.txt')

        '''self.descriptions = DescriptionFile(self.desc_path + '/stat_descriptions.txt')
        self.descriptions.merge(DescriptionFile(self.desc_path + '/gem_stat_descriptions.txt'))
        self.descriptions.merge(DescriptionFile(self.desc_path + '/skill_stat_descriptions.txt'))
        self.descriptions.merge(DescriptionFile(self.desc_path + '/aura_skill_stat_descriptions.txt'))
        self.descriptions.merge(DescriptionFile(self.desc_path + '/active_skill_gem_stat_descriptions.txt'))
        self.descriptions.merge(DescriptionFile(self.desc_path + '/minion_skill_gem_stat_descriptions.txt'))'''
        #self.stat_descriptions = DescriptionFile(glob(desc_path + '/*_descriptions.txt'))

    def _get_monster_data(self, gem_name):
        if gem_name not in self._summon_map:
            console('No mapping defined for "%s" - fix me' % gem_name, msg=Msg.error)
            return

        mtypes = []
        worker = list(self._summon_map[gem_name])
        for row in self.reader['MonsterTypes.dat']:
            found = False
            for types_name_index in worker:
                if types_name_index == row['Index0']:
                    found = True
                    break

            if found:
                worker.remove(types_name_index)
                mtypes.append(row)

                # Found everything, stop early
                if not worker:
                    break

        if not mtypes:
            console('Failed to find the index for "%s" in MonsterTypes.dat' % gem_name, msg=Msg.error)
            return

        result = []
        for row in self.reader['MonsterVarieties.dat']:
            found = False
            for mt in mtypes:
                # There is more then one variety, but we only need one
                if row['MonsterTypesKey'] == mt:
                    found = True
                    break

            if found:
                mtypes.remove(mt)
                result.append(row)

                # Found everything, stop early
                if not mtypes:
                    break

        return result

    def _get_monster_stats(self, mv, minion_level):
        default = self.reader['DefaultMonsterStats.dat'][minion_level-1]

        life = default['Life'] * mv['LifeMultiplier'] // 100
        damage_min =  default['Damage'] * mv['DamageMultiplier'] // 100
        damage_max = damage_min * 7 // 3
        aspd = 1500 / mv['AttackSpeed']

        return (damage_min, damage_max), aspd, life

    def _get_gem(self, name):
        base_item_type = None
        for row in self.reader['BaseItemTypes.dat']:
            if row['Name'] == name:
                base_item_type = row
                break

        if base_item_type is None:
            console('The item "%s" was not found.' % name, msg=Msg.error)
            return

        skill_gem = None
        for row in self.reader['SkillGems.dat']:
            if row['BaseItemTypesKey'] == base_item_type:
                skill_gem = row
                break

        if skill_gem is None:
            console('The skill gem "%s" was not found. Is the item a skill?' % gem, msg=Msg.error)
            return

        return base_item_type, skill_gem

    def level_progression(self, parsed_args):
        gems = {}
        for gem in parsed_args.gem:
            g = self._get_gem(gem)
            if g is not None:
                gems[gem] = g

        if not gems:
            console('No gems found. Exiting...')
            sys.exit(-1)

        console('Loading additional files...')
        self.reader.read_file('GrantedEffects.dat')
        self.reader.read_file('GrantedEffectsPerLevel.dat')
        self.reader.read_file('ItemExperiencePerLevel.dat')
        self.reader.read_file('MonsterTypes.dat')
        self.reader.read_file('MonsterVarieties.dat')

        console('Processing information...')

        r = ExporterResult()

        for gem in gems:
            # Unpack the references
            base_item_type, skill_gem = gems[gem]

            # TODO: Maybe catch empty stuff here?
            exp = 0
            exp_level = []
            exp_total = []
            for row in self.reader['ItemExperiencePerLevel.dat']:
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
            for row in self.reader['GrantedEffectsPerLevel.dat']:
                if row['GrantedEffectsKey'] == ge:
                    gepl.append(row)

            if not gepl:
                console('No level progression found for "%s". Skipping.' % gem, msg=Msg.error)
                continue

            is_aura = False
            is_minion = False
            is_totem = False
            tf = self.translation_cache.get_file('Metadata/skill_stat_descriptions.txt')
            for tag in skill_gem['GemTagsKeys']:
                if tag['Id'] == 'aura':
                    is_aura = True
                    tf = self.translation_cache.get_file('Metadata/aura_skill_stat_descriptions.txt')
                elif tag['Id'] == 'minion':
                    is_minion = True
                    #TODO one of?
                    #tf = self.translation_cache.get_file('Metadata/minion_skill_stat_descriptions.txt')
                    tf = self.translation_cache.get_file('Metadata/minion_attack_skill_stat_descriptions.txt')
                    tf = self.translation_cache.get_file('Metadata/minion_spell_skill_stat_descriptions.txt')
                elif tag['Id'] == 'curse':
                    tf = self.translation_cache.get_file('Metadata/curse_skill_stat_descriptions.txt')
                elif tag['Id'] == 'totem':
                    is_totem = True

            attributes = ['Str', 'Dex', 'Int']

            stat_ids = []
            stat_indexes = []
            for index, stat in enumerate(gepl[0]['StatsKeys']):
                stat_ids.append(stat['Id'])
                stat_indexes.append(index+1)


            has_monster_stats = False
            monster_stat_index = 0
            # Handle special stats. Can only have one
            for stat in ('display_minion_monster_level', 'base_active_skill_totem_level'):
                if stat in stat_ids:
                    index = stat_ids.index(stat)
                    monster_stat_index = stat_indexes[index]
                    has_monster_stats = True
                    del stat_ids[index]
                    del stat_indexes[index]
                    break

            if has_monster_stats:
                monster_varieties = self._get_monster_data(gem)
                # No result->skip
                # message will be handled by _get_monster_data
                if monster_varieties is None:
                    continue

            # Find fixed stats
            fixed = []
            fixed_indexes = []
            for i in range(1, len(stat_ids)+1):
                is_static = True
                val = gepl[0]['Stat%sValue' % i]
                for row in gepl[1:]:
                    if val != row['Stat%sValue' % i]:
                        is_static = False
                        break

                if is_static:
                    fixed.append(stat_ids[i-1])
                    fixed_indexes.append(i)

            # First translation probe
            values_result = [gepl[1]['Stat%sValue' % i] for i in stat_indexes]
            trans_result = tf.get_translation(stat_ids, values_result, full_result=True, use_placeholder=True)

            # Make a copy
            # Remove fixed stats that are not required for translation
            for tr in trans_result.found:
                all_fixed = True
                required_ids = []
                for trans_id in tr.ids:
                    if trans_id in fixed:
                        required_ids.append(trans_id)
                    else:
                        all_fixed = False

                if not all_fixed:
                    for required_id in required_ids:
                        fixed.remove(required_id)

            for item in fixed:
                i = stat_ids.index(item)
                del stat_ids[i]
                del stat_indexes[i]

            # Get the real translation string...
            values_result = [gepl[1]['Stat%sValue' % i] for i in stat_indexes]
            trans_result = tf.get_translation(stat_ids, values_result, full_result=True, use_placeholder=True)

            # Find percentages & seconds and their indexes
            formatting_indexes = []
            for i, line in enumerate(trans_result.lines):
                formatting_indexes.append([{'%': False, 'second': False}]*3)

                for match in self._regex_format.finditer(line):
                    index = 'xyz'.index(match.group('index'))
                    formatting_indexes[i][index][match.group('tag')] = True

            # Find out which columns actually change so we don't add unnecessary
            # data
            has_damage = False
            has_multiplier = False
            has_mana_cost = False
            damage = gepl[0]['DamageMultiplier']
            multiplier = gepl[0]['ManaMultiplier']
            mana_cost = gepl[0]['ManaCost']
            for row in gepl[1:]:
                if damage != row['DamageMultiplier']:
                    has_damage = True
                if multiplier != row['ManaMultiplier']:
                    has_multiplier = True
                if mana_cost != row['ManaCost']:
                    has_mana_cost = True

            #
            # Out put processing
            #
            out = []
            out.append('{{GemLevelTable\n')
            for attr in tuple(attributes):
                if skill_gem[attr]:
                    out.append('| %s=yes\n' % attr.lower())
                else:
                    attributes.remove(attr)

            offset = 0
            if has_mana_cost:
                offset += 1
                if is_aura:
                    out.append('| c%s=Mana<br>Reserved\n' % offset)
                else:
                    out.append('| c%s=Mana<br>Cost\n' % offset)

            if has_multiplier:
                offset += 1
                out.append('| c%s=Mana<br>Multiplier\n' % offset)

            if has_damage:
                offset += 1
                out.append('| c%s=Base<br>Damage\n' % offset)

            for index, item in enumerate(trans_result.lines):
                if item in abbreviations:
                    abbr = abbreviations[item]
                    if abbr:
                        item = '{{Abbr|%s|%s}}' % (abbr, item)
                    else:
                        warnings.warn(item, MissingAbbreviation)
                else:
                    warnings.warn(item, MissingAbbreviation)
                line = '| c%s=%s\n' % (index+offset+1, item)
                out.append(line)
            offset += len(trans_result.lines)

            for index, item in enumerate(trans_result.missing_ids):
                line = '| c%s=%s\n' % (index+offset+1, item)
                out.append(line)
            offset += len(trans_result.missing_ids)

            if has_monster_stats:
                offset += 1
                out.append('| c%s=' % offset)
                if is_minion:
                    out.append('Minion')
                elif is_totem:
                    out.append('Totem')
                out.append('<br>Level\n')
                for mv in monster_varieties:
                    # Shorten the name
                    name = self._regex_summon.sub('', mv['Name'])
                    name = name.replace(' ', '<br>')
                    # Only hp for totems
                    if is_minion:
                        out.append('| c%s=%s<br>Base Damage\n' % (offset+1, name))
                        out.append('| c%s=%s<br>Base Attack Speed\n' % (offset+2, name))
                        offset += 2
                    offset += 1
                    out.append('| c%s=%s<br>Base Life\n' % (offset, name))

            out.append('}}\n')

            if base_item_type['ItemClass'] == 19:
                gtype = GemTypes.active
            elif base_item_type['ItemClass'] == 20:
                gtype = GemTypes.support

            # Is sorted already, but just in case..
            gepl.sort(key=lambda row: row['Level'])
            for i, row in enumerate(gepl):
                out.append('|- \n')
                out.append('! %s\n' % row['Level'])
                out.append('| %s\n' % row['LevelRequirement'])

                for attr in attributes:
                    # Gems with base level > 21 are not possible
                    if row['Level'] > 21:
                        out.append('| \n')
                    else:
                        out.append('| %i\n' % gem_stat_requirement(
                            level=row['LevelRequirement'],
                            gtype=gtype,
                            multi=skill_gem[attr],
                        ))

                if has_mana_cost:
                    out.append('| %s\n' % row['ManaCost'])

                if has_multiplier:
                    out.append('| {0:n}%\n'.format(row['ManaMultiplier']))

                if has_damage:
                    out.append('| {0:n}%\n'.format(row['DamageMultiplier']/100+100))

                fmt_values = [row['Stat%sValue' % i] for i in stat_indexes]
                values_result = tf.get_translation(stat_ids, fmt_values, full_result=True, only_values=True)
                for j in range(0, len(values_result.values)):
                    try:
                        values_result.lines[j]
                    except IndexError:
                        values_result.lines.append([])

                    for k in range(0, len(values_result.values[j])):
                        value_real = values_result.values[j][k]
                        try:
                            value_fmt = values_result.lines[j][k]
                        except IndexError:
                            values_result.lines[j].append(0)
                            value_fmt = value_real

                        if isinstance(value_fmt, float):
                            #if value_fmt.is_integer():
                            #    value_fmt = '{0:n}'.format(value_fmt)
                            value_fmt = '{0:.2f}'.format(value_fmt)
                        else:
                            value_fmt = '{0:n}'.format(value_fmt)

                        if formatting_indexes[j][k]['%']:
                            value_fmt += '%'
                        elif formatting_indexes[j][k]['second']:
                            value_fmt += 's'

                        values_result.lines[j][k] = value_fmt

                for item in values_result.lines:
                    out.append('| %s\n' % '&ndash;'.join(item))

                for trans_id in trans_result.missing_ids:
                    out.append('| %s\n' % fmt_values[stat_ids.index(trans_id)])

                if has_monster_stats:
                    minion_level = row['Stat%sValue' % monster_stat_index]
                    out.append('| %s\n' % minion_level)
                    for mv in monster_varieties:
                        dmg, aspd, life = self._get_monster_stats(mv, minion_level)
                        if is_minion:
                            out.append('| {0:d}&ndash;{1:d}\n'.format(*dmg))
                            out.append('| {0:.2f}\n'.format(aspd))
                        out.append('| {0:,d}\n'.format(life))

                for exp in (exp_level, exp_total):
                    try:
                        # Format in a readable manner
                        out.append('| {0:,d}\n'.format(exp[i]))
                    except IndexError:
                        out.append('| {{n/a}}\n')

            out.append('|}\n')
            r.add_result(
                lines=out,
                out_file='level_progression_%s.txt' % gem,
                wiki_page=base_item_type['Name'],
            )

        return r