"""
Wiki mods exporter

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/mods.py                          |
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

TODO
===============================================================================

FIX the jewel generator (corrupted)
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import warnings
from collections import OrderedDict

# Self
from PyPoE.poe.constants import MOD_DOMAIN, MOD_GENERATION_TYPE
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult, \
    add_format_argument
from PyPoE.cli.exporter.wiki.parser import BaseParser, format_result_rows
from PyPoE.shared.decorators import deprecated

# =============================================================================
# Globals
# =============================================================================

__all__ = ['ModParser', 'ModsHandler']

# =============================================================================
# Classes
# =============================================================================


class OutOfBoundsWarning(UserWarning):
    pass


class WikiCondition(object):
    _regex = re.compile(
        '{{Mod[^}]*}}',
        re.UNICODE | re.MULTILINE | re.DOTALL
    )

    def __init__(self, data, cmdargs):
        self.data = data
        self.cmdargs = cmdargs
        self.match = None

    def __call__(self, *args, **kwargs):
        page = kwargs.get('page')

        if page:
            # Abuse this so it can be called as "text" and "condition"
            if self.match is None:
                self.match = self._regex.search(page.text())
                if self.match is None:
                    return False

                return True

            # I need the +1 offset or it adds a space everytime for some reason.
            return page.text[:self.match.start()] + ''.join(self._get_text()) \
                + page.text[self.match.end()+1:]
        else:
            return self._get_text()

    def _get_text(self):
        return format_result_rows(
            parsed_args=self.cmdargs,
            template_name='Mod',
            ordered_dict=self.data,
        )



class ModsHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser('mods', help='Mods Exporter')
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        lua_sub = self.parser.add_subparsers()

        # Mods
        mparser = lua_sub.add_parser(
            'mods',
            help='Extract all mods.'
        )
        mparser.set_defaults(func=lambda args: mparser.print_help())

        sub = mparser.add_subparsers(help='Method of extracting mods')

        parser = sub.add_parser('modid', help='Use the string mod identifer')
        parser.add_argument(
            'modid',
            help='Ids of the mods to update; can be specified multiple times',
            nargs='+',
        )

        add_format_argument(parser)

        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.modid,
        )

        parser = sub.add_parser('rowid', help='Use the rowid')
        parser.add_argument(
            'start',
            help='Starting index',
            nargs='?',
            type=int,
            default=0,
        )

        parser.add_argument(
            'end',
            nargs='?',
            help='Ending index',
            type=int,
        )

        add_format_argument(parser)

        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.rowid,
        )

        parser = sub.add_parser('filter', help='Filter mods')
        parser.add_argument(
            '--domain',
            dest='domain',
            help='Mod domain',
            choices=[k.name for k in MOD_DOMAIN],
        )

        parser.add_argument(
            '--generation-type', '--type',
            dest='generation_type',
            help='Mod domain',
            choices=[k.name for k in MOD_GENERATION_TYPE],
        )

        add_format_argument(parser)

        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.filter,
        )

        # Tempest

        parser = lua_sub.add_parser(
            'tempest',
            help='Extract tempest stuff (DEPRECATED).',
        )
        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.tempest,
            wiki=False,
        )


class ModParser(BaseParser):
    # Load files in advance
    _files = [
        'Mods.dat',
        'Stats.dat',
    ]
    
    # Load translations in advance
    _translations = [
        'map_stat_descriptions.txt',
    ]

    def _append_effect(self, result, mylist, heading):
        mylist.append(heading)

        for line in result.lines:
            mylist.append('* %s' % line)
        for i, stat_id in enumerate(result.missing_ids):
            value = result.missing_values[i]
            if hasattr(value, '__iter__'):
                value = '(%s to %s)' % tuple(value)
            mylist.append('* %s %s' % (stat_id, value))

    def modid(self, args):
        mods = []

        requested_mods = list(args.modid)

        for mod in self.rr['Mods.dat']:
            try:
                i = requested_mods.index(mod['Id'])
            except ValueError:
                continue

            requested_mods.pop(i)
            mods.append(mod)

        return self.mod(args, mods)

    def rowid(self, args):
        mods = list(self.rr['Mods.dat'])
        l = len(mods)

        # Warnings only to make it a bit more user friendly
        if abs(args.start) > len(mods):
            warnings.warn(
                'Specified minimum index "%s" is larger then the total '
                'number of mods (%s).' % (args.start, l),
                OutOfBoundsWarning,
            )

        if args.end is not None:
            if abs(args.end) > len(mods):
                warnings.warn(
                    'Specified maximum index "%s" is larger then the total '
                    'number of mods (%s).' % (args.end, l),
                    OutOfBoundsWarning,
                )

            if args.start >=0 and args.end >= 0 and args.start > args.end:
                warnings.warn(
                    'Specified maximum index "%s" is smaller then the '
                    'specified minimum index "%s"' % (args.end, args.start),
                    OutOfBoundsWarning,
                )

        mods = mods[args.start:args.end]

        return self.mod(args, mods)

    def filter(self, args):
        mods = []

        filters = []
        if args.domain:
            filters.append({
                'column': 'Domain',
                'comp': getattr(MOD_DOMAIN, args.domain),
            })

        if args.generation_type:
            filters.append({
                'column': 'GenerationType',
                'comp': getattr(MOD_GENERATION_TYPE, args.generation_type),
            })

        for mod in self.rr['Mods.dat']:
            for filter in filters:
                if mod[filter['column']] != filter['comp']:
                    break
            else:
                mods.append(mod)

        return self.mod(args, mods)

    def mod(self, args, mods):
        r = ExporterResult()

        if mods:
            console('Found %s mods. Processing...' % len(mods))
        else:
            warnings.warn(
                'No mods found for the specified parameters. Quitting.'
            )
            return r

        for mod in mods:
            data = OrderedDict()

            for k in (
                ('Id', 'id'),
                ('Name', 'name'),
                ('CorrectGroup', 'mod_group'),
                ('Domain', 'domain'),
                ('GenerationType', 'generation_type'),
                ('Level', 'required_level'),

            ):
                data[k[1]] = mod[k[0]]

            if mod['BuffDefinitionsKey']:
                data['granted_buff_id'] = mod['BuffDefinitionsKey']['Id']
                data['granted_buff_value'] = mod['BuffValue']
            # todo ID for GEPL
            if mod['GrantedEffectsPerLevelKey']:
                data['granted_skill'] = mod['GrantedEffectsPerLevelKey']['GrantedEffectsKey']['Id']
            data['mod_type'] = mod['ModTypeKey']['Name']

            data['stat_text'] = '<br>'.join(self._get_stats(mod))

            for i in range(1, 6):
                k = mod['StatsKey%s' % i]
                if k is None:
                    continue
                data['stat%s_id' % i] = k['Id']
                data['stat%s_min' % i] = mod['Stat%sMin' % i]
                data['stat%s_max' % i] = mod['Stat%sMax' % i]

            for i, tag in enumerate(mod['SpawnWeight_TagsKeys']):
                j = i + 1
                data['spawn_weight%s_tag' % j] = tag['Id']
                data['spawn_weight%s_value' % j] = mod['SpawnWeight_Values'][i]

            for i, tag in enumerate(mod['GenerationWeight_TagsKeys']):
                j = i + 1
                data['generation_weight%s_tag' % j] = tag['Id']
                data['generation_weight%s_value' % j] = \
                    mod['GenerationWeight_Values'][i]

            if mod['TagsKeys']:
                data['tags'] = ', '.join([t['Id'] for t in mod['TagsKeys']])

            page_name = mod['Id'].replace('_', '~')
            cond = WikiCondition(data, args)

            r.add_result(
                text=cond,
                out_file='mod_%s.txt' % mod['Id'],
                wiki_page=[
                    {'page': page_name, 'condition': cond},
                    {'page': page_name + ' (Mod)', 'condition': cond},
                ],
                wiki_message='Mod updater',
            )

        return r

    @deprecated(message='Will be done in-wiki in the future - non functional')
    def tempest(self, parsed_args):
        tf = self.tc['map_stat_descriptions.txt']
        data = []
        for mod in self.rr['Mods.dat']:
            # Is it a tempest mod?
            if mod['CorrectGroup'] != 'MapEclipse':
                continue

            # Doesn't have a name - probably not implemented
            if not mod['Name']:
                continue

            stats = []
            for i in range(1, 6):
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
                tempest = self.rr['ExplodingStormBuffs.dat'][stat_values[index]-1]

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