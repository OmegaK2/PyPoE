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
    'x% increased Critical Strike Multiplier': '',
    'Base duration is x seconds': '',
    'You and nearby allies deal x-y additional Lightning Damage with Attacks': '',
    'x% increased Area of Effect radius': '',
    'You and nearby allies deal x% more Lightning Damage with Spells': '',
    'Minions have x% increased Attack Speed': '',
    'Minions have x% increased Movement Speed': '',
    'x% increased Minion Maximum Life': '',
    'Cursed enemies lose x% Elemental Resistances': '',
    'x% increased Character Size': '',
    'Golems grant x% additional Physical Damage Reduction': '',
    'Deals x-y Cold Damage': '',
    'x% increased Rarity of Items Dropped by Slain Enemies': '',
    'x Life gained for each enemy hit by Supported Attack': '',
    'x% more Spell Damage': '',
    'Totems and Minions summoned by this Skill have x% Fire Resistance': '',
    'Totems and Minions summoned by this Skill have x% Cold Resistance': '',
    'Totems and Minions summoned by this Skill have x% Lightning Resistance': '',
    'x% reduced Curse Duration': '',
    'Golems Grant x% increased Critical Strike Chance': '',
    'Golems Grant x% increased Accuracy': '',
    'x% increased Minion Damage': '',
    'x% more Damage against Chilled Enemies': '',
    'Minions deal x% less Damage': '',
    'x% increased Cast Speed': '',
    'Can use Items requiring up to level x': '',
    'Deals x% of Base Damage': '',
    'Minions\' Attacks deal x-y additional Physical Damage': '',
    'x% chance to cause Monsters to Flee when hit': '',
    'You and nearby allies gain x additional Evasion Rating': '',
    'Summons x Skeleton Warriors': '',
    'Summons x Skeleton Archers': '',
    'Summons x Skeleton Mage': '',
    'Can summon up to x Skeletons at a time': '',
    'Deals x-y Lightning Damage': '',
    'x% increased Duration ': '',
    'x% increased Buff Duration Per Endurance Charge': '',
    'You and nearby allies gain x additional Energy Shield': '',
    'Deals x-y Fire Damage': '',
    'x% chance to Ignite enemies': '',
    'x% increased Damage': '',
    'Cursed enemies take x% increased Physical damage': '',
    'x% increased Blinding duration': '',
    'Deals x Fire Damage per second': '',
    'x% Chance to Block': '',
    'x% Chance to Block Spells': '',
    'Minions recover x Life when they Block': '',
    'Explosion deals x-y Base Fire damage per Fuse Charge': '',
    'x% more Melee Attack Speed': '',
    'Ignites for x% of Overkill Damage': '',
    'x% more Area Damage': '',
    'x% reduced Enemy Stun Threshold': 'Stun<br>Threshold',
    'x% more Weapon Elemental Damage': '',
    'x% increased Projectile Speed': '',
    'x% increased Projectile Damage': '',
    'x% chance to Cast this Spell when you take a total of y Damage': '',
    'x% less Damage': '',
    'This Gem can only Support Skill Gems requiring Level x or lower': '',
    'Chains x Times': '',
    'Deals x Base Chaos Damage per second': '',
    'Creates Corpses up to Level x': '',
    'x additional Arrows': '',
    'Cursed enemies have x% reduced Accuracy Rating': '',
    'Cursed enemies deal x% less Damage': '',
    'You and nearby allies gain x% increased Attack Speed': '',
    'You and nearby allies gain x% increased Cast Speed': '',
    'You and nearby allies gain x% increased Movement Speed': '',
    'x% increased Attack Speed': '',
    'x% more Mine Damage': '',
    'Shields break after x total Damage is prevented': '',
    'x additional Armour': '',
    'Adds x-y Lightning Damage to Spells': '',
    'Adds x-y Lightning Damage to Attacks': '',
    'x% increased maximum Life': '',
    'Minions deal x% increased Physical Damage with Melee Attacks': '',
    'x% more Cast Speed': '',
    'x% increased Damage per one hundred nearby Enemies': '',
    'x Mana Regenerated per second': '',
    'Gain x% of your Physical Damage as Extra Fire Damage': '',
    'x% less Projectile Damage': '',
    'Cursed enemies lose x% Lightning Resistance': '',
    'Cursed enemies have x% chance to be Shocked by Lightning Damage': '',
    'You and nearby allies gain x% additional Fire Resistance': '',
    'You and nearby allies gain x% additional maximum Fire Resistance': '',
    'You and nearby allies regenerate x Mana per second': '',
    'x% increased Burning Damage': '',
    'Freezes enemies as though dealing x% more Damage': '',
    'x% less Skill Effect Duration': '',
    'x% less Damage to main target': '',
    'x% less Damage to other targets': '',
    'x% more Melee Physical Damage when on Full Life': '',
    'Golems Grant x% increased Damage': '',
    'Cursed enemies have x% reduced Stun Recovery': '',
    'Cursed enemies have an additional x% chance to be Stunned': '',
    'Cursed enemies have a x% chance to grant an Endurance Charge when slain': '',
    'Gain Onslaught for x seconds on Killing a Shocked Enemy': '',
    'x% chance to Shock enemies': '',
    'Gain x% of Physical Damage as Extra Chaos Damage': '',
    'x% increased Mana Leeched per second': '',
    'x to Level of Supported Active Skill Gems': '',
    'Gain x% of Physical Damage as Extra Lightning Damage': '',
    'x% chance to gain a Power Charge on Critical Strike': '',
    'x Life regenerated per second': '',
    'You and nearby allies gain x% to all Elemental Resistances': '',
    'x% more Melee Physical Damage': '',
    'Penetrates x% Cold Resistance': '',
    'x% more Trap Damage': '',
    'Adds x-y Cold Damage to Spells': '',
    'Adds x-y Cold Damage to Attacks': '',
    'Enemy Block Chance reduced by x% against this Skill': '',
    'Enemy Dodge Chance reduced by x% against this Skill': '',
    'Cursed enemies have x% less Evasion': '',
    'Cursed enemies grant x Life when Hit by Attacks': '',
    'Cursed enemies grant x Mana when Hit by Attacks': '',
    'Cursed enemies have a x% chance to grant a Frenzy Charge when slain': '',
    'Minions have x% less Life': '',
    'Minions have x% less Energy Shield': '',
    'x% reduced Mana Cost': '',
    'Can deal x-y base Fire damage': '',
    'Can deal x-y base Cold damage': '',
    'Can deal x-y base Lightning damage': '',
    'x% increased Critical Strike Chance': '',
    'x% increased Life Leeched per second': '',
    'x% more Damage per Repeat': '',
    'x% Chance to Dodge Attacks': '',
    'x% Chance to Dodge Spell Damage': '',
    'x% increased Spell Damage': '',
    'x Endurance Charges granted per one hundred nearby enemies': '',
    'x% increased Movement Speed': '',
    'x% increased totem life': '',
    'x% increased effect of Aura': '',
    'Minions deal x% more Damage': '',
    'x% increased Minion Movement Speed': '',
    'Minions have x% increased Cast Speed': '',
    'Cursed enemies grant x% more Physical Melee Damage on Melee hit': '',
    'Cursed enemies grant x% increased Attack Speed on Melee hit': '',
    'Deals x-y Physical Damage': '',
    'Supported Triggered Spells have x% increased Spell Damage': '',
    'x% to Quality of Supported Active Skill Gems': '',
    'x% more Melee Physical Damage against Bleeding Enemies': '',
    'x% increased Chill Duration on enemies': '',
    'x% more Damage at Maximum Charge Distance': '',
    'x% more Damage while Dead': '',
    'x% increased Melee Physical Damage': '',
    'Penetrates x% Fire Resistance': '',
    'x% chance to Cast this Spell when Stunned': '',
    'x additional Accuracy Rating': '',
    'x% reduced Movement Speed per Nearby Enemy': '',
    'x% reduced Movement Speed': '',
    'x% chance to Knock Enemies Back on hit': '',
    'x% less Physical Damage taken when Hit': '',
    'x% less Fire Damage taken when Hit': '',
    'You and nearby allies deal x-y additional Fire Damage with Attacks': '',
    'You and nearby allies deal x-y additional Fire Damage with Spells': '',
    'Deals x-y base Lightning Damage per Power Charge': '',
    'Deals x-y base Fire Damage per Endurance Charge': '',
    'Deals x-y base Cold Damage per Frenzy Charge': '',
    'Penetrates x% Lightning Resistance': '',
    'Cursed enemies take x% increased Damage from Projectiles': '',
    'Cursed enemies lose x% Cold Resistance': '',
    'Cursed enemies have x% chance to be Frozen by Cold Damage': '',
    'You and nearby allies gain x% additional Lightning Resistance': '',
    'You and nearby allies gain x% additional maximum Lightning Resistance': '',
    'You and nearby allies gain x% additional Cold Resistance': '',
    'You and nearby allies gain x% additional maximum Cold Resistance': '',
    'Cursed enemies lose x% Fire Resistance': '',
    'Cursed enemies have x% chance to be Ignited by Fire Damage': '',
    'x% more Physical Projectile Attack Damage': '',
    'You and nearby allies regenerate x% Life per second': '',
    'x% more Trap and Mine Damage': '',
    'x% less Projectile Speed': '',
    'x% more Projectile Damage': '',
    'Cursed enemies are x% slower': '',
    'Cursed enemies take x% more extra damage from Critical Strikes': '',
    'Cursed enemies have an additional x% chance to receive a Critical Strike': '',
    'Cursed enemies grant x Life when Killed': '',
    'Cursed enemies grant x Mana when Killed': '',
    'Cursed enemies have a x% chance to grant a Power Charge when slain': '',
    'x% chance of Projectiles Piercing': '',
    'Leeches x Life to you for each corpse consumed': '',
    'Leeches x Mana to you for each corpse consumed': '',
    'Wall will be x units long': '',
    'Adds an additional Projectile': '',
    'x% increased Quantity of Items Dropped by Slain Enemies': '',
    'Gain x% of Cold Damage as Extra Fire Damage': '',
    'x% chance to Cast linked Spells when you Crit an Enemy': '',
    'You and nearby allies gain x% more Armour': '',
    'x% chance to gain a Frenzy Charge on Killing a Frozen Enemy': '',
    'You and nearby allies gain x% of your Physical Damage as Extra Cold Damage': '',
    'Supported skills deal x% less Damage': '',
    'Deals x-y Chaos Damage': '',
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
    def __init__(self, **kwargs):
        self.desc_path = kwargs['desc_path']
        self.data_path = kwargs['data_path']

        self.opt = {
            'use_dat_value': False,
        }

        self.reader = RelationalReader(
            self.data_path,
            files=['BaseItemTypes.dat', 'SkillGems.dat', 'Stats.dat'],
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

            ge = skill_gem['GrantedEffectsKey']

            gepl = []
            for row in self.reader['GrantedEffectsPerLevel.dat']:
                if row['GrantedEffectsKey'] == ge:
                    gepl.append(row)

            is_aura = False
            tf = self.translation_cache.get_file('Metadata/skill_stat_descriptions.txt')
            for tag in skill_gem['GemTagsKeys']:
                if tag['Id'] == 'aura':
                    is_aura = True
                    tf = self.translation_cache.get_file('Metadata/aura_skill_stat_descriptions.txt')
                elif tag['Id'] == 'minion':
                    #TODO one of?
                    #tf = self.translation_cache.get_file('Metadata/minion_skill_stat_descriptions.txt')
                    tf = self.translation_cache.get_file('Metadata/minion_attack_skill_stat_descriptions.txt')
                    tf = self.translation_cache.get_file('Metadata/minion_spell_skill_stat_descriptions.txt')
                elif tag['Id'] == 'curse':
                    tf = self.translation_cache.get_file('Metadata/curse_skill_stat_descriptions.txt')

            attributes = {'Str': 0, 'Dex': 0, 'Int': 0}

            stat_ids = []
            stat_indexes = []
            for index, stat in enumerate(gepl[0]['StatsKeys']):
                stat_ids.append(stat['Id'])
                stat_indexes.append(index+1)

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
            values = [gepl[0]['Stat%sValue' % i] for i in stat_indexes]
            trans_result = tf.get_translation(stat_ids, values, full_result=True, use_placeholder=True)

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
            values = [gepl[0]['Stat%sValue' % i] for i in stat_indexes]
            trans_result = tf.get_translation(stat_ids, values, full_result=True, use_placeholder=True)

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
            for attr in tuple(attributes.keys()):
                if skill_gem[attr]:
                    out.append('| %s=yes\n' % attr.lower())
                    attributes[attr] = skill_gem[attr]
                else:
                    del attributes[attr]

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
                out.append('| c%s=Damage<br>Multiplier\n' % offset)

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
            for index, item in enumerate(trans_result.missing):
                line = '| c%s=%s\n' % (index+offset+1, item)
                out.append(line)

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
                            multi=attributes[attr],
                        ))

                if has_mana_cost:
                    out.append('| %s\n' % row['ManaCost'])

                if has_multiplier:
                    out.append('| %i%%\n' % (row['ManaMultiplier']))

                if has_damage:
                    out.append('| %.2f%%\n' % (row['DamageMultiplier']/100))

                fmt_values = [row['Stat%sValue' % i] for i in stat_indexes]
                values = tf.get_translation(stat_ids, fmt_values, only_values=True)

                for j, value in enumerate(values):
                    for k, v in enumerate(value):
                        if isinstance(v, float):
                            values[j][k] = '{0:.2f}'.format(v)
                        else:
                            values[j][k] = '{0:n}'.format(v)

                for item in values:
                    out.append('| %s\n' % '-'.join(item))

                for trans_id in trans_result.missing:
                    out.append('| %s\n' % fmt_values[stat_ids.index(trans_id)])

                for exp in (exp_level, exp_total):
                    try:
                        # Format in a readable manner
                        out.append('| {0:,d}\n'.format(exp[i]))
                    except IndexError:
                        out.append('| {{n/a}}\n')

            out.append('|}\n')
            #out.append(str(ge))
            r.add_result(
                lines=out,
                out_file='level_progression_%s.txt' % gem,
                wiki_page=base_item_type['Name'],
            )

        return r