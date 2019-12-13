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

Internal API
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
        'main_page',
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

        self.add_default_subparser_filters(
            sub_parser=self.parser.add_subparsers(),
            cls=PassiveSkillParser,
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
        self.add_image_arguments(kwargs['parser'])
        kwargs['parser'].add_argument(
            '-ft-id', '--filter-id', '--filter-metadata-id',
            help='Regular expression on the id',
            type=str,
            dest='re_id',
        )


class PassiveSkillParser(parser.BaseParser):
    _files = [
        'PassiveSkills.dat',
    ]

    _passive_column_index_filter = partialmethod(
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
            'condition': lambda passive: passive['Reminder_ClientStringsKeys']
        }),
        ('PassiveSkillBuffsKeys', {
            'template': 'buff_id',
            'format': lambda value: ','.join([x['BuffDefinitionsKey']['Id'] for x in value]),
            'condition': lambda passive: passive['PassiveSkillBuffsKeys']
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
            'default': False,
        }),
        ('IsNotable', {
            'template': 'is_notable',
            'default': False,
        }),
        ('IsMultipleChoiceOption', {
            'template': 'is_multiple_choice_option',
            'default': False,
        }),
        ('IsMultipleChoice', {
            'template': 'is_multiple_choice',
            'default': False,
        }),
        ('IsJustIcon', {
            'template': 'is_icon_only',
            'default': False,
        }),
        ('IsJewelSocket', {
            'template': 'is_jewel_socket',
            'default': False,
        }),
        ('IsAscendancyStartingNode', {
            'template': 'is_ascendancy_starting_node',
            'default': False,
        }),
    ))

    def _apply_filter(self, parsed_args, passives):
        if parsed_args.re_id:
            parsed_args.re_id = re.compile(parsed_args.re_id, flags=re.UNICODE)
        else:
            return passives

        new = []

        for passive in passives:
            if parsed_args.re_id and not \
                    parsed_args.re_id.match(passive['Id']):
                continue

            new.append(passive)

        return new

    def by_rowid(self, parsed_args):
        return self.export(
            parsed_args,
            self.rr['PassiveSkills.dat'][parsed_args.start:parsed_args.end],
        )

    def by_id(self, parsed_args):
        return self.export(parsed_args, self._passive_column_index_filter(
            column_id='Id', arg_list=parsed_args.id
        ))

    def by_name(self, parsed_args):
        return self.export(parsed_args, self._passive_column_index_filter(
            column_id='Name', arg_list=parsed_args.name
        ))

    def export(self, parsed_args, passives):
        r = ExporterResult()

        passives = self._apply_filter(parsed_args, passives)

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
        # Connections are one-way, make them two way
        for psg_id, node in node_index.items():
            for other_psg_id in node.connections:
                node_index[other_psg_id].connections.append(psg_id)

        self.rr['PassiveSkills.dat'].build_index('PassiveSkillGraphId')

        self._image_init(parsed_args)

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

            if passive['Icon_DDSFile']:
                icon = passive['Icon_DDSFile'].split('/')
                if passive['Icon_DDSFile'].startswith(
                        'Art/2DArt/SkillIcons/passives/'):
                    if icon[-2] == 'passives':
                        data['icon'] = icon[-1]
                    else:
                        data['icon'] = '%s (%s)' % (icon[-1], icon[-2])
                else:
                    data['icon'] = icon[-1]

            data['icon'] = data['icon'].replace('.dds', '')

            stat_ids = []
            values = []

            j = 0
            for i in range(0, self._MAX_STAT_ID):
                try:
                    stat = passive['StatsKeys'][i]
                except IndexError:
                    break
                j = i + 1
                stat_ids.append(stat['Id'])
                data['stat%s_id' % j] = stat['Id']
                values.append(passive['Stat%sValue' % j])
                data['stat%s_value' % j] = passive['Stat%sValue' % j]

            data['stat_text'] = '<br>'.join(self._get_stats(
                stat_ids, values,
                translation_file='passive_skill_stat_descriptions.txt'
            ))

            # For now this is being added to the stat text
            for ps_buff in passive['PassiveSkillBuffsKeys']:
                stat_ids = [stat['Id'] for stat in
                            ps_buff['BuffDefinitionsKey']['StatsKeys']]
                values = ps_buff['Buff_StatValues']
                #if passive['Id'] == 'AscendancyChampion7':
                #    index = stat_ids.index('damage_taken_+%_from_hits')
                #    del stat_ids[index]
                #    del values[index]
                for i, (sid, val) in enumerate(zip(stat_ids, values)):
                    j += 1
                    data['stat%s_id' % j] = sid
                    data['stat%s_value' % j] = val

                text = '<br>'.join(self._get_stats(
                    stat_ids, values,
                    translation_file='passive_skill_aura_stat_descriptions.txt'
                ))

                if data['stat_text']:
                    data['stat_text'] += '<br>' + text
                else:
                    data['stat_text'] = text

            node = node_index.get(passive['PassiveSkillGraphId'])
            if node and node.connections:
                data['connections'] = ','.join([
                    self.rr['PassiveSkills.dat'].index['PassiveSkillGraphId'][
                        psg_id]['Id'] for psg_id in node.connections])

            # extract icons if specified
            if parsed_args.store_images and self.ggpk:
                fn = data['icon'] + ' passive skill icon'
                dds = os.path.join(self._img_path, fn + '.dds')
                png = os.path.join(self._img_path, fn + '.png')
                if not (os.path.exists(dds) or os.path.exists(png)):
                    self._write_dds(
                        data=self.ggpk[passive['Icon_DDSFile']].record.extract(
                            ).read(),
                        out_path=dds,
                        parsed_args=parsed_args,
                    )

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
