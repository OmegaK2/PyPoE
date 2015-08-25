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
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.poe.file.translations import TranslationFileCache
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

    base_jewel_map = {
        'not_str': ['int', 'dex'],
        'not_int': ['dex', 'str'],
        'not_dex': ['int', 'str'],
    }


    def __init__(self, **kwargs):
        self.desc_path = kwargs['desc_path']

        opt = {
            'use_dat_value': False,
        }

        self.r = RelationalReader(kwargs['data_path'], files=[
            'Mods.dat',
            'Stats.dat',
        ], options=opt)

        self.translation_cache = TranslationFileCache(kwargs['base_path'])
        # Touch files we'll need
        self.translation_cache['map_stat_descriptions.txt']

        #self.descriptions = DescriptionFile(self.desc_path + '/map_descriptions.txt')
        #self.stat_descriptions = DescriptionFile(glob(desc_path + '/*_descriptions.txt'))

    def _get_stats(self, mod):
        stats = []
        for i in range(1, 5):
            stat = mod['StatsKey%s' % i]
            if stat:
                stats.append(stat)

        ids = []
        values = []
        for i, stat in enumerate(stats):
            j = i + 1
            values.append([mod['Stat%sMin' % j], mod['Stat%sMax' % j]])
            ids.append(stat['Id'])

        tf = self.translation_cache['stat_descriptions.txt']

        effects = tf.get_translation(ids, values)
        if not effects:
            console("%s %s" % (ids, values))

        return tf.get_translation(ids, values)

    def _append_effect(self, result, mylist, heading):
        mylist.append(heading)

        for line in result.lines:
            mylist.append('* %s' % line)
        for i, stat_id in enumerate(result.missing_ids):
            value = result.missing_values[i]
            if hasattr(value, '__iter__'):
                value = '(%s to %s)' % tuple(value)
            mylist.append('* %s %s' % (stat_id, value))

    def map(self, parsed_args):
        tf = self.translation_cache['map_stat_descriptions.txt']

        mods = []
        for mod in self.r['Mods.dat']:
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
        tf = self.translation_cache['map_stat_descriptions.txt']
        data = []
        for mod in self.r['Mods.dat']:
            # Is it a tempest mod?
            if mod['CorrectGroup'] != 'MapEclipse':
                continue

            # Doesn't have a name - probably not implemented
            if not mod['Name']:
                continue

            stats = []
            for i in range(1, 5):
                stat = mod['StatsKey%s' % i]
                if stat:
                    stats.append(stat)

            info = {}
            info['name'] = mod['Name']
            effects = []

            stat_ids = [st['Id'] for st in stats]
            stat_values = []

            for i, stat in enumerate(stats):
                j = i + 1
                values = [mod['Stat%sMin' % j], mod['Stat%sMax' % j]]
                if values[0] == values[1]:
                    values = values[0]
                stat_values.append(values)

            try:
                index = stat_ids.index('map_summon_exploding_buff_storms')
            except ValueError:
                pass
            else:
                # Value is incremented by 1 for some reason
                tempest = self.r['ExplodingStormBuffs.dat'][stat_values[index]-1]

                stat_ids.pop(index)
                stat_values.pop(index)

                if tempest['BuffDefinitionsKey']:
                    tempest_stats = tempest['BuffDefinitionsKey']['StatKeys']
                    tempest_values = tempest['StatValues']
                    tempest_stat_ids = [st['Id'] for st in tempest_stats]
                    t = tf.get_translation(tempest_stat_ids, tempest_values, full_result=True)
                    self._append_effect(t, effects, 'The tempest buff provides the following effects:')
                #if tempest['MonsterVarietiesKey']:
                #    print(tempest['MonsterVarietiesKey'])
                #    break

            t = tf.get_translation(stat_ids, stat_values, full_result=True)
            self._append_effect(t, effects, 'The area gets the following modifiers:')

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
        for mod in self.r['Mods.dat']:
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
                'Group': '<br>'.join([t['Id'] for t in mod['TagsKeys']]),
                'GroupWeight': [],
            }

            # Check whether the mod can spawn at all
            v = 0
            for value in mod['SpawnWeight_Values']:
                if value > 0:
                    v = 1
                    break
            if v == 0:
                continue

            # Default is always last mod, so this should work
            for i, tag in enumerate(mod['SpawnWeight_TagsKeys']):
                weight = mod['SpawnWeight_Values'][i]
                tid = tag['Id']
                if tid == 'default':
                    listformat[tid] = weight
                    for k in ('int', 'dex', 'str'):
                        if k not in listformat:
                            listformat[k] = weight
                elif tid in ('not_int', 'not_dex', 'not_str'):
                    for k in self.base_jewel_map[tid]:
                        listformat[k] = weight
                else:
                    listformat['GroupWeight'].append((tid,  weight))

            listformat['GroupWeight'].sort(key=lambda x: x[0])
            for i in range(0, len(listformat['GroupWeight'])):
                listformat['GroupWeight'][i] = '%s: %s' % listformat['GroupWeight'][i]
            listformat['GroupWeight'] = '<br>\n'.join(listformat['GroupWeight'])
            data.append(listformat)
        # Sort my name
        data.sort(key=lambda lf: lf['Name'])

        if parsed_args.type == 'corrupted':
            fmt = (
                '|- \n'
                '| %(Description)s\n'
            )
        else:
            fmt = (
                '|-\n'
                '| %(Name)s\n'
                '| %(Description)s\n'
                '| %(Group)s \n'
                # '| %(default)s \n'
                '| %(str)s \n'
                '| %(int)s \n'
                '| %(dex)s \n'
                '| %(GroupWeight)s\n'
            )

        out = []
        for lf in data:
            out.append(fmt % lf)

        r = ExporterResult()
        r.add_result(lines=out, out_file='jewel_%s_mods.txt' % parsed_args.type)

        return r