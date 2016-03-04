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
from PyPoE.cli.exporter.wiki.handler import *
from PyPoE.cli.exporter.wiki.parser import BaseParser
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


class ModWikiHandler(WikiHandler):
    _regex = re.compile(
        '{{Mod[^}]*}}',
        re.UNICODE | re.MULTILINE | re.DOTALL
    )

    def _find_page(self, row, page_name):
        page = self.pws.pywikibot.Page(self.site, page_name)
        match = self._regex.search(page.text)

        if match:
            console('Found wiki page "%s"' % page_name)
            return page, page.text[:match.start()] + ''.join(row['lines']) + page.text[match.end():]
        else:
            console('Failed to find the mod table on wiki page "%s"' % page_name, msg=Msg.warning)
            return None, None

    def handle_page(self, *a, row):
        page_name = row['wiki_page']
        console('Editing Mod "%s"...' % page_name)

        if self.cmdargs.force:
            text = ''.join(row['lines'])
            page = self.pws.pywikibot.Page(self.site, page_name)
        else:
            kwargs = {
                'row': row,
                'page_name': page_name,
            }

            page, text = self._find_page(**kwargs)
            if text is None:
                kwargs['page_name'] = '%s (Mod)' % page_name
                page, text = self._find_page(**kwargs)

            if text is None:
                console('Can\'t find working wikipage. Skipping.', Msg.error)
                return

        self.save_page(
            page=page,
            text=text,
            message=self.name,
        )

    def add_arguments(self, parser):
        super(ModWikiHandler, self).add_arguments(parser)
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignores the validation check and force replacement of the entire page',
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

        wiki_handler = ModWikiHandler(
            name='Mod updater',
        )

        sub = mparser.add_subparsers(help='Method of extracting mods')

        parser = sub.add_parser('modid', help='Use the string mod identifer')
        parser.add_argument(
            'modid',
            help='Ids of the mods to update; can be specified multiple times',
            nargs='+',
        )

        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.modid,
            wiki_handler=wiki_handler,
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

        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.rowid,
            wiki_handler=wiki_handler,
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

        self.add_default_parsers(
            parser=parser,
            cls=ModParser,
            func=ModParser.filter,
            wiki_handler=wiki_handler,
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

        return self.mod(self, args, mods)

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
                data['spawn_tag%s' % j] = tag['Id']
                data['spawn_value%s' % j] = mod['SpawnWeight_Values'][i]

            if mod['TagsKeys']:
                data['tags'] = ', '.join([t['Id'] for t in mod['TagsKeys']])

            out = ['{{Mod\n']
            for key, value in data.items():
                out.append('|{0: <16}= {1}\n'.format(key, value))
            out.append('}}\n')

            r.add_result(
                lines=out,
                out_file='mod_%s.txt' % mod['Id'],
                wiki_page=mod['Id'].replace('_', '~'),
            )

        return r

    @deprecated(message='Will be done in-wiki in the future.')
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