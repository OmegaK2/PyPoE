"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/area.py                          |
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
from functools import partialmethod
from collections import OrderedDict

# 3rd-party

# self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki import parser
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult, \
    add_format_argument

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class WikiCondition(parser.WikiCondition):
    COPY_KEYS = (
        #'main_page',
        'release_version',
    )

    NAME = 'Area'
    ADD_INCLUDE = False
    INDENT = 33


class AreaCommandHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser(
            'area',
            help='Area Exporter',
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
            cls=AreaParser,
            func=AreaParser.by_id,
        )
        add_format_argument(a_id)
        a_id.add_argument(
            'area_id',
            help='Id of the area, can be specified multiple times.',
            nargs='+',
        )

        # by name
        a_name = sub.add_parser(
            'name',
            help='Extract areas by their name.'
        )
        self.add_default_parsers(
            parser=a_name,
            cls=AreaParser,
            func=AreaParser.by_name,
        )
        add_format_argument(a_name)
        a_name.add_argument(
            'area_name',
            help='Visible name of the area (localized), can be specified multiple times.',
            nargs='+',
        )

        # by row ID
        a_rid = sub.add_parser(
            'rowid',
            help='Extract areas by rowid.'
        )
        self.add_default_parsers(
            parser=a_rid,
            cls=AreaParser,
            func=AreaParser.by_rowid,
        )
        add_format_argument(a_rid)
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
            help='Extract areas using filters.'
        )
        self.add_default_parsers(
            parser=a_filter,
            cls=AreaParser,
            func=AreaParser.by_filter,
        )
        add_format_argument(a_filter)

        a_filter.add_argument(
            '-ft-id', '--filter-id', '--filter-metadata-id',
            help='Regular expression on the id',
            type=str,
            dest='re_id',
        )


class AreaParser(parser.BaseParser):
    _files = [
        'WorldAreas.dat',
        'MapPins.dat',
        'AtlasNode.dat',
    ]

    _area_column_index_filter = partialmethod(
        parser.BaseParser._column_index_filter,
        dat_file_name='WorldAreas.dat',
        error_msg='Several areas have not been found:\n%s',
    )

    _COPY_KEYS = OrderedDict((
        ('Id', {
            'template': 'id',
        }),
        ('Name', {
            'template': 'name',
        }),
        ('Act', {
            'template': 'act',
        }),
        ('AreaLevel', {
            'template': 'level',
        }),
        ('MaxLevel', {
            'template': 'level_restriction_max',
            'default': 100,
        }),
        ('AreaType_TagsKeys', {
            'template': 'area_type_tags',
            'format': lambda value: ', '.join([
                tag['Id'] for tag in value
            ]),
            'default': [],
        }),
        ('TagsKeys', {
            'template': 'tags',
            'format': lambda value: ', '.join([
                tag['Id'] for tag in value
            ]),
            'default': [],
        }),
        ('LoadingScreen_DDSFile', {
            'template': 'loading_screen',
            'format': lambda value: value.replace('Art/Textures/Interface/Loadi'
                'ngImages/', '').replace('.dds', ''),
        }),
        ('Connections_WorldAreasKeys', {
            'template': 'connection_ids',
            'format': lambda value: ', '.join(OrderedDict.fromkeys([
                area['Id'] for area in value
            ]).keys()),
            'default': [],
        }),
        ('ParentTown_WorldAreasKey', {
            'template': 'parent_area_id',
            'format': lambda value: value['Id'],
        }),
        ('ModsKeys', {
            'template': 'modifier_ids',
            'format': lambda value: ', '.join([
                mod['Id'] for mod in value
            ]),
            'default': [],
        }),
        ('Bosses_MonsterVarietiesKeys', {
            'template': 'boss_monster_ids',
            'format': lambda value: ', '.join([
                mv['Id'] for mv in value
            ]),
            'default': [],
        }),
        ('Monsters_MonsterVarietiesKeys', {
            'template': 'monster_ids',
            'format': lambda value: ', '.join([
                mv['Id'] for mv in value
            ]),
            'default': [],
        }),
        ('FirstEntry_NPCTextAudioKey', {
            'template': 'entry_text',
            'format': lambda value: value['Text'],
        }),
        ('FirstEntry_NPCsKey', {
            'template': 'entry_npc',
            'condition': lambda area:
                area['FirstEntry_NPCTextAudioKey'] is not None,
            'format': lambda value: value['Name'],
        }),
        # Spawn chances section
        ('VaalArea_SpawnChance', {
            'template': 'vaal_area_spawn_chance',
            'condition': lambda area: area['VaalArea_SpawnChance'] > 0 and
                                      area['VaalArea_WorldAreasKeys'],
        }),
        ('VaalArea_WorldAreasKeys', {
            'template': 'vaal_area_ids',
            'condition': lambda area: area['VaalArea_SpawnChance'] > 0 and
                                      area['VaalArea_WorldAreasKeys'],
            'format': lambda value: ', '.join([
                area['Id'] for area in value
            ]),
        }),

        ('Strongbox_SpawnChance', {
            'template': 'strongbox_spawn_chance',
            'condition': lambda area: area['Strongbox_SpawnChance'] > 0,
        }),
        ('Strongbox_MaxCount', {
            'template': 'strongbox_max',
            'condition': lambda area: area['Strongbox_SpawnChance'] > 0,
            'default': 0,
        }),
        ('Strongbox_RarityWeight', {
            'template': 'strongbox_rarity_weight',
            'condition': lambda area: area['Strongbox_SpawnChance'] > 0,
            'default': '',
            'format': lambda value: ', '.join([str(v) for v in value]),
        }),
        # bools
        ('IsMapArea', {
            'template': 'is_map_area',
            'default': False,
        }),
        ('IsUniqueMapArea', {
            'template': 'is_unique_map_area',
            'default': False,
        }),
        ('IsTown', {
            'template': 'is_town_area',
            'default': False,
        }),
        ('IsHideout', {
            'template': 'is_hideout_area',
            'default': False,
        }),
        ('IsVaalArea', {
            'template': 'is_vaal_area',
            'default': False,
        }),
        ('IsMasterDailyArea', {
            'template': 'is_master_daily_area',
            'default': False,
        }),
        ('IsLabyrinthArea', {
            'template': 'is_labyrinth_area',
            'default': False,
        }),
        ('IsLabyrinthAirlock', {
            'template': 'is_labyrinth_airlock_area',
            'default': False,
        }),
        ('IsLabyrinthBossArea', {
            'template': 'is_labyrinth_boss_area',
            'default': False,
        }),
        ('HasWaypoint', {
            'template': 'has_waypoint',
            'default': False,
        }),
    ))

    def by_rowid(self, parsed_args):
        return self.export(
            parsed_args,
            self.rr['WorldAreas.dat'][parsed_args.start:parsed_args.end],
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
        re_id = re.compile(parsed_args.re_id) if parsed_args.re_id else None

        out = []
        for row in self.rr['WorldAreas.dat']:
            if re_id:
                if not re_id.match(row['Id']):
                    continue
            out.append(row)

        return self.export(parsed_args, out)

    def export(self, parsed_args, areas):
        console('Found %s areas, parsing...' % len(areas))

        r = ExporterResult()

        if not areas:
            console(
                'No areas found for the specified parameters. Quitting.',
                msg=Msg.warning,
            )
            return r

        console('Accessing additional data...')

        self.rr['MapPins.dat'].build_index('WorldAreasKeys')
        self.rr['AtlasNode.dat'].build_index('WorldAreasKey')

        console('Found %s areas. Processing...' % len(areas))

        for area in areas:
            data = OrderedDict()

            for row_key, copy_data in self._COPY_KEYS.items():
                value = area[row_key]

                condition = copy_data.get('condition')
                if condition is not None and not condition(area):
                    continue

                # Skip default values to reduce size of template
                if value == copy_data.get('default'):
                    continue
                '''default = copy_data.get('default')
                if default is not None and value == default:
                        continue'''

                fmt = copy_data.get('format')
                if fmt:
                    value = fmt(value)
                data[copy_data['template']] = value

            for i, (tag, value) in enumerate(zip(area['SpawnWeight_TagsKeys'],
                                                 area['SpawnWeight_Values']),
                                             start=1):
                data['spawn_weight%s_tag' % i] = tag['Id']
                data['spawn_weight%s_value' % i] = value

            map_pin = self.rr['MapPins.dat'].index['WorldAreasKeys'].get(area)
            if map_pin:
                data['flavour_text'] = map_pin[0]['FlavourText']

            atlas_node = self.rr['AtlasNode.dat'].index['WorldAreasKey'].get(
                area)
            if atlas_node:
                data['flavour_text'] = atlas_node[0]['FlavourText']

            #
            # Add main-page if possible
            #

            # TODO: Harbinger maps are not handled correctly atm

            # Double legacy maps, pre 2.0
            map_version = None
            if data.get('tags') and 'map' in data['tags']:
                for row in self.rr['MapSeries.dat']:
                    if not area['Id'].startswith(row['Id']):
                        continue
                    map_version = row['Name']


            if map_version:
                if 'Unique' in area['Id'] or 'BreachBoss' in area['Id'] or \
                        area['Id'].endswith('ShapersRealm'):
                    data['main_page'] = '%s (%s)' % (area['Name'], map_version)
                elif 'Harbinger' in area['Id']:
                    data['main_page'] = '%s (%s Tier) (%s)' % (
                        area['Name'],
                        re.sub('^.*Harbinger', '', area['Id']),
                        map_version,
                    )
                else:
                    data['main_page'] = '%s Map (%s)' % (
                        area['Name'], map_version
                    )

            cond = WikiCondition(
                data=data,
                cmdargs=parsed_args,
            )

            r.add_result(
                text=cond,
                out_file='area_%s.txt' % data['id'],
                wiki_page=[
                    {
                        'page': 'Area:' + self._format_wiki_title(data['id']),
                        'condition': cond,
                    },
                ],
                wiki_message='Area updater',
            )


        return r

# =============================================================================
# Functions
# =============================================================================
