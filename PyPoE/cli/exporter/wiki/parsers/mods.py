"""
Path     PyPoE/cli/exporter/wiki/parser/mods.py
Name     Wiki mods exporter
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO


http://pathofexile.gamepedia.com


AGREEMENT

See PyPoE/LICENSE


TODO

FIX the jewel generator (corrupted)
"""

# =============================================================================
# Imports
# =============================================================================

# Self
from PyPoE.poe.file.dat import DatFile
from PyPoE.poe.file.translations import DescriptionFile
from PyPoE.cli.core import console
from PyPoE.cli.exporter.wiki.handler import *


# =============================================================================
# Globals
# =============================================================================

__all__ = ['ModParser', 'ModsHandler']

# =============================================================================
# Classes
# =============================================================================

class ModsHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser('mods', help='Mods Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        lua_sub = self.parser.add_subparsers()

        parser = lua_sub.add_parser(
            'map',
            help='Extract map mods.'
        )
        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.map,
        )

        parser = lua_sub.add_parser(
            'tempest',
            help='Extract tempest stuff.',
        )
        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.tempest,
        )

        parser = lua_sub.add_parser(
            'jewel',
            help='Extract jewel mods.',
        )
        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.jewel,
        )
        parser.add_argument(
            'type',
            choices=('suffix', 'prefix', 'corrupted'),
            help='The type of jewel mod to extract.',
        )

class ModParser(object):
    dropdata = {
            0: 'Any other item',
            5: 'Bow',
            9: 'Wand',
            10: 'Staff',
            11: 'Mace',
            12: 'Sword',
            13: 'Dagger',
            14: 'Claw',
            15: 'Axe',
            29: 'Crimson' , # STR
            30: 'Viridian', # DEX
            31: 'Cobalt', # INT
            143: 'Weapon Mod?',
            144: 'Two-Hand',
            145: 'Dual-Wield',
            146: 'Shield',
            147: '(2H/Dual/Shield???)',
            148: '(Claw/Dagger/Wand/1h)',
            #149: 'Melee?',
        }
    #affix_wiki = '|-\n| %(Name)s\n| %(Description)s\n| %(Group)s \n| %(0)s || %(29)s || %(30)s || %(31)s || %(5)s || %(9)s || %(10)s || %(11)s || %(12)s || %(13)s || %(14)s || %(15)s  || %(143)s || %(144)s || %(145)s || %(146)s || %(147)s || %(148)s'
    affix_wiki = '|-\n| %(Name)s\n| %(Description)s\n| %(Group)s \n| %(0)s \n| %(29)s \n| %(30)s \n| %(31)s \n| %(GroupWeight)s\n'

    def __init__(self, data_path, desc_path):
        self.desc_path = desc_path

        opt = {
            'use_dat_value': False,
        }

        self.mods = DatFile('Mods.dat', read_file=data_path, options=opt).reader
        self.stats = DatFile('Stats.dat', read_file=data_path, options=opt).reader

        self.descriptions = DescriptionFile(self.desc_path + '/stat_descriptions.txt')
        #self.stat_descriptions = DescriptionFile(glob(desc_path + '/*_descriptions.txt'))

    def _get_stats(self, mod):
        stats = []
        for i in range(1, 5):
            key = mod['StatsKey%s' % i]
            if key != -1:
                stats.append(self.stats.table_data[key])

        ids = []
        values = []
        for i in range(0, len(stats)):
            stat = stats[i]
            j = i + 1
            values.append([mod['Stat%sMin' % j], mod['Stat%sMax' % j]])
            ids.append(stat['Id'])

        effects = self.descriptions.get_translation(ids, values)
        if not effects:
            console(ids, values)

        return self.descriptions.get_translation(ids, values)

    def map(self, parsed_args):
        #self.descriptions.merge(DescriptionFile(self.desc_path + '/map_stat_descriptions.txt'))

        mods = []
        for mod in self.mods.table_data:
            if mod['Domain'] != 5:
                continue
            if mod['GenerationType'] not in (1, 2):
                continue
            mods.append(mod)

        # Output processing
        out = []

        for mod in mods:
            try:
                effects = self._get_stats(mod)
                out.append("%s %s\n" % (mod['Name'], effects))
            except:
                pass

        r = ExporterResult()
        r.add_result(lines=out, out_file='map_mods.txt')

        return r

    def tempest(self, parsed_args):
        # Filter by tempest mods

        mods = []
        for mod in self.mods.table_data:
            if mod['CorrectGroup'] == 'MapEclipse':
                mods.append(mod)

        data = []
        for mod in mods:
            if 'of' not in mod['Name']:
                continue
            stats = []
            for i in range(1, 5):
                key = mod['StatsKey%s' % i]
                if key != -1:
                    stats.append(self.stats.table_data[key])

            info = {}
            info['name'] = mod['Name']
            effects = ['The area gets the following modifiers:']
            for i in range(0, len(stats)):
                stat = stats[i]
                j = i + 1
                values = [mod['Stat%sMin' % j], mod['Stat%sMax' % j]]
                if values[0] == values[1]:
                    values.pop(1)
                t= self.descriptions.get_translation([stat['Id'], ], values)
                if t:
                    effects.append('* %s' % t[0])
                else:
                    if len(values) == 1:
                        values = values[0]
                    effects.append('* %s %s' % (stat['Id'], values))
            info['effect'] = '\n'.join(effects)
            data.append(info)

        data.sort(key=lambda info: info['name'])

        out = []
        for info in data:
            out.append('|-\n')
            out.append('| %s\n' % info['name'])
            out.append('| %s\n' % info['effect'])
            out.append('| \n')

        r = ExporterResult()
        r.add_result(lines=out, out_file='tempest_mods.txt')

        return r

    def jewel(self, parsed_args):
        data = []
        tset = set()
        for mod in self.mods.table_data:
            # not a jewel
            if mod['Domain'] != 11:
                continue
            if parsed_args.type == 'prefix' and mod['GenerationType'] != 1:
                continue
            elif parsed_args.type == 'suffix' and mod['GenerationType'] != 2:
                continue
            elif parsed_args.type == 'corrupted' and mod['GenerationType'] != 5:
                continue

            listformat = {
                'Name': mod['Name'],
                'Description': '\n'.join(self._get_stats(mod)),
                'Group': mod['Data0'],
                'GroupWeight': [],
            }
            # Jewels: Strange...
            lg = len(mod['SpawnWeight_TagsKeys'])

            #
            for v in mod['SpawnWeight_TagsKeys']:
                tset.add(v)
            if lg == 1:
                listformat['0'] = mod['SpawnWeight_Values'][0]
            else:
                # Last two entries are reversed for no apparent reason other then to confuse us
                listformat[str(mod['SpawnWeight_TagsKeys'][-1])] = str(mod['SpawnWeight_Values'][-2])
                listformat[str(mod['SpawnWeight_TagsKeys'][-2])] = str(mod['SpawnWeight_Values'][-1])
                # These seem to be in order..
                for i in range(0, lg-2):
                    group_id = mod['SpawnWeight_TagsKeys'][i]
                    weight = mod['SpawnWeight_Values'][i]
                    if group_id in (0, 29, 30, 31):
                        listformat[str(group_id)] = weight
                    else:
                        listformat['GroupWeight'].append((group_id,  weight))
            disabled = True
            for item in self.dropdata:
                item = str(item)
                if item not in listformat:
                    listformat[item] = ''
                elif int(listformat[item]) != 0:
                    disabled = False

            if disabled:
                continue

            listformat['GroupWeight'].sort(key=lambda x: x[0])
            for i in range(0, len(listformat['GroupWeight'])):
                listformat['GroupWeight'][i] = '%s: %s' % listformat['GroupWeight'][i]
            listformat['GroupWeight'] = '<br>\n'.join(listformat['GroupWeight'])
            data.append(listformat)
        # Sort my name
        data.sort(key=lambda lf: lf['Name'])

        out = []
        for lf in data:
            out.append(self.affix_wiki % lf)

        r = ExporterResult()
        r.add_result(lines=out, out_file='jewel_%s_mods.txt' % parsed_args.type)

        return r