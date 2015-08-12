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
from PyPoE.poe.file.dat import DatFile
from PyPoE.poe.file.translations import DescriptionFile
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

        self.base_item_types = DatFile('BaseItemTypes.dat', read_file=data_path, options=self.opt).reader
        self.skill_gems = DatFile('SkillGems.dat', read_file=data_path, options=self.opt).reader
        #self.mods = DatFile('Mods.dat', read_file=data_path, options=self.opt).reader
        self.stats = DatFile('Stats.dat', read_file=data_path, options=self.opt).reader



        self.descriptions = DescriptionFile(self.desc_path + '/stat_descriptions.txt')
        #self.stat_descriptions = DescriptionFile(glob(desc_path + '/*_descriptions.txt'))

    def calc_exp(self, level, multi=1):
        # 0f: 100%: int(multi*(1.5*level+6))
        # 3f 60%: round(multi*(1.6*level+5)
        return multi*(1.6*level+6)

    def _support(self, level):
        # perfect!
        return int(1.5*level+6)

    def _active(self, level):
        # roughly... true?
        return 2.1*level+7.8

    def _get_gem(self, name):

        base_item_type = None
        for row in self.base_item_types:
            if row['Name'] == name:
                base_item_type = row
                break

        if base_item_type is None:
            print(Fore.LIGHTRED_EX + 'The specified item was not found.' + Fore.RESET)
            sys.exit(-1)

        skill_gem = None
        for row in self.skill_gems:
            if row['BaseItemTypesKey'] == base_item_type.rowid:
                skill_gem = row
                break

        if skill_gem is None:
            print(Fore.LIGHTRED_EX + 'The specified skill gem was not found. Is the item a skill?' + Fore.RESET)
            sys.exit(-1)

        return base_item_type, skill_gem

    def level_progression(self, parsed_args):
        base_item_type, skill_gem = self._get_gem(parsed_args.gem)

        print('Loading additional files...')
        granted_effects = DatFile('GrantedEffects.dat', read_file=self.data_path, options=self.opt).reader
        granted_effects_per_level = DatFile('GrantedEffectsPerLevel.dat', read_file=self.data_path, options=self.opt).reader
        item_experience_per_level = DatFile('ItemExperiencePerLevel.dat', read_file=self.data_path, options=self.opt).reader

        print('Processing information...')

        # TODO: Maybe catch empty stuff here?
        exp = []
        for row in item_experience_per_level:
            if row['BaseItemTypesKey'] == base_item_type.rowid:
                exp.append(row)

        ge = None
        for row in granted_effects:
            if row.rowid == skill_gem['GrantedEffectsKey']:
                ge = row

        gepl = []
        for row in granted_effects_per_level:
            if row['GrantedEffectsKey'] == ge.rowid:
                gepl.append(row)

        attributes = {'Str': 0, 'Dex': 0, 'Int': 0}

        out = []
        out.append('{{GemLevelTable\n')
        for attr in tuple(attributes.keys()):
            if skill_gem[attr]:
                out.append('| %s=yes\n' % attr.lower())
                attributes[attr] = skill_gem[attr] / 100
            else:
                del attributes[attr]

        offset = 0
        if gepl[0]['ManaCost']:
            offset += 1
            out.append('| c%s = Mana<br>Cost\n' % offset)

        stat_ids = []
        for stat in gepl[0]['StatsKeys']:
            stat_ids.append(self.stats[stat]['Id'])

        desc, translation_indexes = self.descriptions.get_translation(stat_ids, (42, )*len(stat_ids), return_indexes=True)
        for index, item in enumerate(desc):
            line = '| c%s=%s\n' % (index+offset+1, item)
            out.append(line.replace('42', 'x'))

        out.append('}}\n')

        # Is sorted already, but just in case..
        gepl.sort(key=lambda row: row['Level'])
        for i, row in enumerate(gepl):
            out.append('|- \n')
            out.append('! %s\n' % row['Level'])
            out.append('| %s\n' % row['LevelRequirement'])

            for attr in attributes:
                #TODO: Fix
                #out.append('| %i\n' % (attributes[attr]))
                out.append('| ?\n')

            if row['ManaCost']:
                out.append('| %s\n' % row['ManaCost'])

            stat_offset = 1
            for indexes in translation_indexes:
                icount = len(indexes)
                values = []
                for j in range(stat_offset, stat_offset+icount):
                    values.append(str(row['Stat%sValue' % j]))

                out.append('| %s\n' % '-'.join(values))
                stat_offset += icount

            try:
                # Format in a readable manner
                out.append('| {0:,d}\n'.format(exp[i]['Experience']))
            except IndexError:
                out.append('| {{n/a}}\n')

        out.append('|}\n')
        #out.append(str(ge))

        return out