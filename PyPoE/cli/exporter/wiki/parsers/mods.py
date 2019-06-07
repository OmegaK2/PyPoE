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
from collections import OrderedDict, defaultdict
from functools import partialmethod

# Self
from PyPoE.poe import text
from PyPoE.poe.constants import \
    MOD_DOMAIN, MOD_GENERATION_TYPE, MOD_STATS_RANGE, MOD_SELL_PRICES
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult
from PyPoE.cli.exporter.wiki.parser import BaseParser, WikiCondition
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


class ModWikiCondition(WikiCondition):
    COPY_KEYS = (
        'tier_text',
    )

    NAME = 'Mod'


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

        self.add_default_subparser_filters(sub, cls=ModParser)

        # mods filter
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

    def add_default_parsers(self, *args, **kwargs):
        super().add_default_parsers(*args, **kwargs)
        parser = kwargs['parser']
        self.add_format_argument(parser)


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

    _mod_column_index_filter = partialmethod(
        BaseParser._column_index_filter,
        dat_file_name='Mods.dat',
        error_msg='Several areas have not been found:\n%s',
    )

    def _append_effect(self, result, mylist, heading):
        mylist.append(heading)

        for line in result.lines:
            mylist.append('* %s' % line)
        for i, stat_id in enumerate(result.missing_ids):
            value = result.missing_values[i]
            if hasattr(value, '__iter__'):
                value = '(%s to %s)' % tuple(value)
            mylist.append('* %s %s' % (stat_id, value))

    def by_rowid(self, parsed_args):
        return self._export(
            parsed_args,
            self.rr['Mods.dat'][parsed_args.start:parsed_args.end],
        )

    def by_id(self, parsed_args):
        return self._export(parsed_args, self._mod_column_index_filter(
            column_id='Id', arg_list=parsed_args.id
        ))

    def by_name(self, parsed_args):
        return self._export(parsed_args, self._mod_column_index_filter(
            column_id='Name', arg_list=parsed_args.name
        ))

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

        return self._export(args, mods)

    def _export(self, parsed_args, mods):
        r = ExporterResult()

        if mods:
            console('Found %s mods. Processing...' % len(mods))
        else:
            console(
                'No mods found for the specified parameters. Quitting.',
                msg=Msg.warning
            )
            return r

        # Needed for localizing sell prices
        self.rr['BaseItemTypes.dat'].build_index('Id')

        for mod in mods:
            data = OrderedDict()

            for k in (
                ('Id', 'id'),
                ('CorrectGroup', 'mod_group'),
                ('Domain', 'domain'),
                ('GenerationType', 'generation_type'),
                ('Level', 'required_level'),
            ):
                v = mod[k[0]]
                if v:
                    data[k[1]] = v

            if mod['Name']:
                root = text.parse_description_tags(mod['Name'])

                def handler(hstr, parameter):
                    return hstr if parameter == 'MS' else ''

                data['name'] = root.handle_tags({'if': handler, 'elif': handler})

            if mod['BuffDefinitionsKey']:
                data['granted_buff_id'] = mod['BuffDefinitionsKey']['Id']
                data['granted_buff_value'] = mod['BuffValue']
            # todo ID for GEPL
            if mod['GrantedEffectsPerLevelKeys']:
                data['granted_skill'] = ', '.join(
                    [k['GrantedEffectsKey']['Id'] for k in
                     mod['GrantedEffectsPerLevelKeys']])
            data['mod_type'] = mod['ModTypeKey']['Name']

            stats = []
            values = []
            for i in MOD_STATS_RANGE:
                k = mod['StatsKey%s' % i]
                if k is None:
                    continue

                stat = k['Id']
                value = mod['Stat%sMin' % i], mod['Stat%sMax' % i]

                if value[0] == 0 and value[1] == 0:
                    continue

                stats.append(stat)
                values.append(value)

            data['stat_text'] = '<br>'.join(self._get_stats(stats, values, mod))

            for i, (sid, (vmin, vmax)) in enumerate(zip(stats, values), start=1):
                data['stat%s_id' % i] = sid
                data['stat%s_min' % i] = vmin
                data['stat%s_max' % i] = vmax

            for i, tag in enumerate(mod['SpawnWeight_TagsKeys']):
                j = i + 1
                data['spawn_weight%s_tag' % j] = tag['Id']
                data['spawn_weight%s_value' % j] = mod['SpawnWeight_Values'][i]

            for i, tag in enumerate(mod['GenerationWeight_TagsKeys']):
                j = i + 1
                data['generation_weight%s_tag' % j] = tag['Id']
                data['generation_weight%s_value' % j] = \
                    mod['GenerationWeight_Values'][i]

            tags = ', '.join(
                [t['Id'] for t in mod['ModTypeKey']['TagsKeys']] +
                [t['Id'] for t in mod['TagsKeys']]
            )
            if tags:
                data['tags'] = tags

            if mod['ModTypeKey']:
                sell_price = defaultdict(int)
                for msp in mod['ModTypeKey']['ModSellPriceTypesKeys']:
                    for i, (item_id, amount) in enumerate(
                            MOD_SELL_PRICES[msp['Id']].items(), start=1):
                        data['sell_price%s_name' % i] = self.rr[
                            'BaseItemTypes.dat'].index['Id'][item_id]['Name']
                        data['sell_price%s_amount' % i] = amount

                # Make sure this is always the same order
                sell_price = sorted(sell_price.items(), key=lambda x:x[0])

                for i, (item_name, amount) in enumerate(sell_price, start=1):
                    data['sell_price%s_name' % i] = item_name
                    data['sell_price%s_amount' % i] = amount

            # 3+ tildes not allowed
            page_name = 'Modifier:' + self._format_wiki_title(mod['Id'])
            cond = ModWikiCondition(data, parsed_args)

            r.add_result(
                text=cond,
                out_file='mod_%s.txt' % data['id'],
                wiki_page=[
                    {'page': page_name, 'condition': cond},
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
            for i in MOD_STATS_RANGE:
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
                    t = tf.get_translation(
                        tempest_stat_ids, tempest_values, full_result=True,
                        lang=config.get_option('language')
                    )
                    self._append_effect(t, effects, 'The tempest buff provides the following effects:')
                #if tempest['MonsterVarietiesKey']:
                #    print(tempest['MonsterVarietiesKey'])
                #    break

            t = tf.get_translation(
                stat_ids, stat_values, full_result=True,
                lang=config.get_option('language')
            )
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