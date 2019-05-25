"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/monster.py                       |
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

Documentation
===============================================================================
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
from functools import partialmethod
from collections import OrderedDict

# Self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult
from PyPoE.cli.exporter.wiki import parser

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class MonsterWikiCondition(parser.WikiCondition):
    COPY_KEYS = (
        'main_page',
        'release_version',
        'screenshot_ext',
    )

    NAME = 'Monster'
    ADD_INCLUDE = False
    INDENT = 33


class MonsterCommandHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser(
            'monster',
            help='Monster exporter (non-lua)',
        )
        self.parser.set_defaults(func=lambda args: self.parser.print_help())

        sub = self.parser.add_subparsers()

        # By id
        a_id = sub.add_parser(
            'id',
            help='Extract monsters by their metadata id.'
        )
        self.add_default_parsers(
            parser=a_id,
            cls=MonsterParser,
            func=MonsterParser.by_id,
        )
        a_id.add_argument(
            'monster_id',
            help='Monster id',
            nargs='+',
        )

        # by name
        a_name = sub.add_parser(
            'name',
            help='Extract areas by their name.'
        )
        self.add_default_parsers(
            parser=a_name,
            cls=MonsterParser,
            func=MonsterParser.by_name,
        )
        a_name.add_argument(
            'monster_name',
            help='Visible name of the area (localized), can be specified '
                 'multiple times.',
            nargs='+',
        )

        # by row ID
        a_rid = sub.add_parser(
            'rowid',
            help='Extract monsters by rowid.'
        )
        self.add_default_parsers(
            parser=a_rid,
            cls=MonsterParser,
            func=MonsterParser.by_rowid,
        )
        a_rid.add_argument(
            'start',
            help='Starting index',
            nargs='?',
            type=int,
            default=0,
        )
        a_rid.add_argument(
            'end',
            nargs='?',
            help='Ending index',
            type=int,
        )

        # filtering
        a_filter = sub.add_parser(
            'filter',
            help='Extract monsters using filters.'
        )
        self.add_default_parsers(
            parser=a_filter,
            cls=MonsterParser,
            func=MonsterParser.by_filter,
        )

        a_filter.add_argument(
            '-ft-id', '--filter-id', '--filter-metadata-id',
            help='Regular expression on the id',
            type=str,
            dest='re_id',
        )

    def add_default_parsers(self, *args, **kwargs):
        super().add_default_parsers(*args, **kwargs)
        parser = kwargs['parser']
        self.add_format_argument(parser)


class MonsterParser(parser.BaseParser):
    _files = [
        'MonsterVarieties.dat',
    ]

    _area_column_index_filter = partialmethod(
        parser.BaseParser._column_index_filter,
        dat_file_name='MonsterVarieties.dat',
        error_msg='Several monsters have not been found:\n%s',
    )

    _COPY_KEYS = OrderedDict((
        ('Id', {
            'template': 'metadata_id',
        }),
        ('MonsterTypesKey', {
            'template': 'monster_type_id',
            'format': lambda v: v['Id'],
        }),
        ('ModsKeys', {
            'template': 'mod_ids',
            'format': lambda v: ', '.join([r['Id'] for r in v]),
        }),
        ('Part1_ModsKeys', {
            'template': 'part1_mod_ids',
            'format': lambda v: ', '.join([r['Id'] for r in v]),
        }),
        ('Part2_ModsKeys', {
            'template': 'part2_mod_ids',
            'format': lambda v: ', '.join([r['Id'] for r in v]),
        }),
        ('Endgame_ModsKeys', {
            'template': 'endgame_mod_ids',
            'format': lambda v: ', '.join([r['Id'] for r in v]),
        }),
        ('TagsKeys', {
            'template': 'tags',
            'format': lambda v: ', '.join([r['Id'] for r in v]),
        }),
        ('GrantedEffectsKeys', {
            'template': 'skill_ids',
            'format': lambda v: ', '.join([r['Id'] for r in v]),
        }),
        ('Name', {
            'template': 'name',
        }),
        ('ObjectSize', {
            'template': 'size',
        }),
        ('MinimumAttackDistance', {
            'template': 'minimum_attack_distance',
        }),
        ('MaximumAttackDistance', {
            'template': 'maximum_attack_distance',
        }),
        ('ModelSizeMultiplier', {
            'template': 'model_size_multiplier',
            'format': lambda v: v/100,
        }),
        ('ExperienceMultiplier', {
            'template': 'experience_multiplier',
            'format': lambda v: v/100,
        }),
        ('DamageMultiplier', {
            'template': 'damage_multiplier',
            'format': lambda v: v/100,
        }),
        ('LifeMultiplier', {
            'template': 'health_multiplier',
            'format': lambda v: v/100,
        }),
        ('CriticalStrikeChance', {
            'template': 'critical_strike_chance',
            'format': lambda v: v/100,
        }),
        ('AttackSpeed', {
            'template': 'attack_speed',
            'format': lambda v: v/1000,
        }),
    ))

    def by_rowid(self, parsed_args):
        return self.export(
            parsed_args,
            self.rr['MonsterVarieties.dat'][parsed_args.start:parsed_args.end],
        )

    def by_id(self, parsed_args):
        return self.export(parsed_args, self._area_column_index_filter(
            column_id='Id', arg_list=parsed_args.monster_id
        ))

    def by_name(self, parsed_args):
        return self.export(parsed_args, self._area_column_index_filter(
            column_id='Name', arg_list=parsed_args.monster_name
        ))

    def by_filter(self, parsed_args):
        re_id = re.compile(parsed_args.re_id) if parsed_args.re_id else None

        out = []
        for row in self.rr['MonsterVarieties.dat']:
            if re_id:
                if not re_id.match(row['Id']):
                    continue
            out.append(row)

        return self.export(parsed_args, out)

    def export(self, parsed_args, monsters):
        r = ExporterResult()

        if not monsters:
            console(
                'No monsters found for the specified parameters. Quitting.',
                msg=Msg.warning,
            )
            return r

        console('Found %s monsters, parsing...' % len(monsters))

        console('Accessing additional data...')

        for monster in monsters:
            data = OrderedDict()

            for row_key, copy_data in self._COPY_KEYS.items():
                value = monster[row_key]

                condition = copy_data.get('condition')
                if condition is not None and not condition(monster):
                    continue

                fmt = copy_data.get('format')
                if fmt:
                    value = fmt(value)

                if value:
                    data[copy_data['template']] = value

            cond = MonsterWikiCondition(
                data=data,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='monster_%s.txt' % data['metadata_id'].replace(
                    '/', '_'),
                wiki_page=[
                    {
                        'page': 'Monster:' +
                                self._format_wiki_title(data['metadata_id']),
                        'condition': cond,
                    },
                ],
                wiki_message='Monster updater',
            )

        return r

# =============================================================================
# Functions
# =============================================================================
