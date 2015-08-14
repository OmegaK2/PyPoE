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
import sys

# 3rd Party
from colorama import Fore

# Self
from PyPoE.poe.file.dat import DatFile, RelationalReader
from PyPoE.poe.file.translations import DescriptionFile
from PyPoE.poe.sim.formula import gem_stat_requirement, GemTypes
from PyPoE.cli.exporter.wiki.handler import ExporterHandler

# =============================================================================
# Classes
# =============================================================================

class GemsHandler(ExporterHandler):
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
            outfile='level_progression.txt',
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

    def add_gem_arg(self, parser):
        parser.add_argument(
            'gem',
            help='Name of the skill gem',
        )

class GemsParser(object):
    def __init__(self, data_path, desc_path):
        self.desc_path = desc_path
        self.data_path = data_path

        self.opt = {
            'use_dat_value': False,
        }

        self.reader = RelationalReader(
            data_path,
            files=['BaseItemTypes.dat', 'SkillGems.dat', 'Stats.dat'],
            options=self.opt,
        )

        self.descriptions = DescriptionFile(self.desc_path + '/stat_descriptions.txt')
        self.descriptions.merge(DescriptionFile(self.desc_path + '/gem_stat_descriptions.txt'))
        self.descriptions.merge(DescriptionFile(self.desc_path + '/skill_stat_descriptions.txt'))
        #self.stat_descriptions = DescriptionFile(glob(desc_path + '/*_descriptions.txt'))

    def _get_gem(self, name):
        base_item_type = None
        for row in self.reader['BaseItemTypes.dat']:
            if row['Name'] == name:
                base_item_type = row
                break

        if base_item_type is None:
            print(Fore.LIGHTRED_EX + 'The specified item was not found.' + Fore.RESET)
            sys.exit(-1)

        skill_gem = None
        for row in self.reader['SkillGems.dat']:
            if row['BaseItemTypesKey'] == base_item_type:
                skill_gem = row
                break

        if skill_gem is None:
            print(Fore.LIGHTRED_EX + 'The specified skill gem was not found. Is the item a skill?' + Fore.RESET)
            sys.exit(-1)

        return base_item_type, skill_gem

    def level_progression(self, parsed_args):
        base_item_type, skill_gem = self._get_gem(parsed_args.gem)

        print('Loading additional files...')
        self.reader.read_file('GrantedEffects.dat')
        self.reader.read_file('GrantedEffectsPerLevel.dat')
        self.reader.read_file('ItemExperiencePerLevel.dat')

        print('Processing information...')

        # TODO: Maybe catch empty stuff here?
        exp = []
        for row in self.reader['ItemExperiencePerLevel.dat']:
            if row['BaseItemTypesKey'] == base_item_type:
                exp.append(row)

        ge = skill_gem['GrantedEffectsKey']

        gepl = []
        for row in self.reader['GrantedEffectsPerLevel.dat']:
            if row['GrantedEffectsKey'] == ge:
                gepl.append(row)

        attributes = {'Str': 0, 'Dex': 0, 'Int': 0}

        stat_ids = []
        for stat in gepl[0]['StatsKeys']:
            stat_ids.append(stat['Id'])

        # Find fixed stats
        fixed = []
        for i in range(1, len(stat_ids)+1):
            is_static = True
            val = gepl[0]['Stat%sValue' % i]
            for row in gepl[1:]:
                if val != row['Stat%sValue' % i]:
                    is_static = False
                    break

            if is_static:
                fixed.append(stat_ids[i-1])

        for item in fixed:
            stat_ids.remove(item)

        trans_result = self.descriptions.get_translation(stat_ids, (42, )*len(stat_ids), full_result=True)

        has_damage = False
        has_multiplier = False
        damage = gepl[0]['DamageMultiplier']
        multiplier = gepl[0]['ManaMultiplier']
        for row in gepl[1:]:
            if damage != row['DamageMultiplier']:
                has_damage = True
            if multiplier != row['ManaMultiplier']:
                has_multiplier = True

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
        if gepl[0]['ManaCost']:
            offset += 1
            out.append('| c%s = Mana<br>Cost\n' % offset)

        if has_multiplier:
            offset += 1
            out.append('| c%s = Mana<br>Multiplier\n' % offset)

        if has_damage:
            offset += 1
            out.append('| c%s = Damage<br>Multiplier\n' % offset)

        for index, item in enumerate(trans_result.lines):
            line = '| c%s=%s\n' % (index+offset+1, item)
            out.append(line.replace('42', 'x'))
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

            if row['ManaCost']:
                out.append('| %s\n' % row['ManaCost'])

            if has_multiplier:
                out.append('| %i%%\n' % (row['ManaMultiplier']))

            if has_damage:
                out.append('| %.2f%%\n' % (row['DamageMultiplier']/100))

            stat_offset = 1
            for indexes in trans_result.indexes:
                icount = len(indexes)
                values = []
                for j in range(stat_offset, stat_offset+icount):
                    values.append(str(row['Stat%sValue' % j]))

                out.append('| %s\n' % '-'.join(values))
                stat_offset += icount
            for index in range(stat_offset, len(stat_ids)+1):
                print(str(row['Stat%sValue' % index]))

            try:
                # Format in a readable manner
                out.append('| {0:,d}\n'.format(exp[i]['Experience']))
            except IndexError:
                out.append('| {{n/a}}\n')

        out.append('|}\n')
        #out.append(str(ge))

        return out