"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/passives.py                      |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================



Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

Interal API
-------------------------------------------------------------------------------
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import os.path
from functools import partialmethod
from collections import OrderedDict

# 3rd-party

# self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki import parser
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult
from PyPoE.poe.file.psg import PSGFile

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class WikiCondition(parser.WikiCondition):
    COPY_KEYS = (
    )

    NAME = 'Passive skill'
    ADD_INCLUDE = False
    INDENT = 36


class PassiveSkillCommandHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser(
            'passive',
            help='Passive skill exporter',
        )
        self.parser.set_defaults(func=lambda args: self.parser.print_help())

        sub = self.parser.add_subparsers()

        # By id
        a_id = sub.add_parser(
            'id',
            help='Extract areas by their id.'
        )
        self.add_default_parsers(
            parser=a_id,
            cls=PassiveSkillParser,
            func=PassiveSkillParser.by_id,
        )
        a_id.add_argument(
            'passive_id',
            help='Id of the passive, can be specified multiple times.',
            nargs='+',
        )

        # by name
        a_name = sub.add_parser(
            'name',
            help='Extract areas by their name.'
        )
        self.add_default_parsers(
            parser=a_name,
            cls=PassiveSkillParser,
            func=PassiveSkillParser.by_name,
        )
        a_name.add_argument(
            'passive_name',
            help='Visible name of the passive skill (localized), can be '
                 'specified multiple times.',
            nargs='+',
        )

        # by row ID
        a_rid = sub.add_parser(
            'rowid',
            help='Extract passive skills by rowid.'
        )
        self.add_default_parsers(
            parser=a_rid,
            cls=PassiveSkillParser,
            func=PassiveSkillParser.by_rowid,
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
        '''a_filter = sub.add_parser(
            'filter',
            help='Extract passives using filters.'
        )
        self.add_default_parsers(
            parser=a_filter,
            cls=PassiveSkillParser,
            func=PassiveSkillParser.by_filter,
        )

        a_filter.add_argument(
            '-ft-id', '--filter-id', '--filter-metadata-id',
            help='Regular expression on the id',
            type=str,
            dest='re_id',
        )'''

    def add_default_parsers(self, *args, **kwargs):
        super().add_default_parsers(*args, **kwargs)
        self.add_format_argument(kwargs['parser'])


class PassiveSkillParser(parser.BaseParser):
    _files = [
        'PassiveSkills.dat',
    ]

    _area_column_index_filter = partialmethod(
        parser.BaseParser._column_index_filter,
        dat_file_name='PassiveSkills.dat',
        error_msg='Several passives have not been found:\n%s',
    )

    _MAX_STAT_ID = 5

    _COPY_KEYS = OrderedDict((
        ('Id', {
            'template': 'id',
        }),
        ('PassiveSkillGraphId', {
            'template': 'int_id',
        }),
        ('Name', {
            'template': 'name',
        }),
        ('FlavourText', {
            'template': 'flavour_text',
            'default': '',
        }),
        ('Reminder_ClientStringsKeys', {
            'template': 'reminder_text',
            'format': lambda value: '<br>'.join([x['Text'] for x in value]),
            'default': '',
        }),
        ('GrantedBuff_BuffDefinitionsKey', {
            'template': 'buff_id',
        }),
        ('SkillPointsGranted', {
            'template': 'skill_points',
            'default': 0,
        }),
        # icon handled not here
        ('AscendancyKey', {
            'template': 'ascendancy_class',
            'format': lambda value: value['Name'],
        }),
        ('IsKeystone', {
            'template': 'is_keystone',
        }),
        ('IsNotable', {
            'template': 'is_notable',
        }),
        ('IsMultipleChoiceOption', {
            'template': 'is_multiple_choice_option',
        }),
        ('IsMultipleChoice', {
            'template': 'is_multiple_choice',
        }),
        ('IsJustIcon', {
            'template': 'is_icon_only',
        }),
        ('IsJewelSocket', {
            'template': 'is_jewel_socket',
        }),
        ('IsAscendancyStartingNode', {
            'template': 'is_ascendancy_starting_node',
        }),
    ))

    def by_rowid(self, parsed_args):
        return self.export(
            parsed_args,
            self.rr['PassiveSkills.dat'][parsed_args.start:parsed_args.end],
        )

    def by_id(self, parsed_args):
        return self.export(parsed_args, self._area_column_index_filter(
            column_id='Id', arg_list=parsed_args.area_id
        ))

    def by_name(self, parsed_args):
        return self.export(parsed_args, self._area_column_index_filter(
            column_id='Name', arg_list=parsed_args.area_name
        ))

    def by_filter(self, parsed_args):
        out = []
        return self.export(parsed_args, out)

    def export(self, parsed_args, passives):
        r = ExporterResult()

        if not passives:
            console(
                'No passives found for the specified parameters. Quitting.',
                msg=Msg.warning,
            )
            return r

        console('Accessing additional data...')

        psg = PSGFile()
        psg.read(
            file_path_or_raw=os.path.join(
                self.base_path, 'Metadata', 'PassiveSkillGraph.psg'
            ),
        )

        node_index = {}
        for group in psg.groups:
            for node in group.nodes:
                node_index[node.passive_skill] = node
        self.rr['PassiveSkills.dat'].build_index('PassiveSkillGraphId')

        console('Found %s, parsing...' % len(passives))

        for passive in passives:
            data = OrderedDict()

            for row_key, copy_data in self._COPY_KEYS.items():
                value = passive[row_key]

                condition = copy_data.get('condition')
                if condition is not None and not condition(passive):
                    continue

                # Skip default values to reduce size of template
                if value == copy_data.get('default'):
                    continue

                fmt = copy_data.get('format')
                if fmt:
                    value = fmt(value)
                data[copy_data['template']] = value

            node = node_index.get(passive['PassiveSkillGraphId'])
            if node and node.connections:
                data['connections'] = ','.join([
                    self.rr['PassiveSkills.dat'].index['PassiveSkillGraphId'][
                        psg_id]['Id'] for psg_id in node.connections])

            # TODO icon

            for i in range(0, self._MAX_STAT_ID):
                try:
                    stat = passive['StatsKeys'][i]
                except IndexError:
                    break
                j = i + 1
                data['stat%s_id' % j] = stat['Id']
                data['stat%s_value' % j] = passive['Stat%sValue' % j]

            cond = WikiCondition(
                data=data,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='passive_skill_%s.txt' % data['id'],
                wiki_page=[
                    {
                        'page': 'Passive Skill:' + self._format_wiki_title(data['id']),
                        'condition': cond,
                    },
                ],
                wiki_message='Passive skill updater',
            )

        return r

# =============================================================================
# Functions
# =============================================================================
