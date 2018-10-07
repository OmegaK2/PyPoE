"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/parsers/incursion.py                     |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Parsers for incursion related things.

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
import os
from functools import partialmethod
from collections import OrderedDict

# 3rd-party

# self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.wiki import parser
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, ExporterResult
from PyPoE.poe.file.ggpk import extract_dds
from PyPoE.poe.file.idl import IDLFile

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class IncursionRoomWikiCondition(parser.WikiCondition):
    COPY_KEYS = (
    )

    NAME = 'Incursion room'
    ADD_INCLUDE = False
    INDENT = 24


class IncursionCommandHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser(
            'incursion',
            help='Incursion data exporter',
        )
        self.parser.set_defaults(func=lambda args: self.parser.print_help())

        sub = self.parser.add_subparsers()
        rooms = sub.add_parser(
            'rooms',
            help='Exporting incursion rooms',
        )
        rooms.set_defaults(func=lambda args: rooms.print_help())

        self.add_default_subparser_filters(
            sub_parser=rooms.add_subparsers(),
            cls=IncursionRoomParser,
        )

    def add_default_parsers(self, *args, **kwargs):
        super().add_default_parsers(*args, **kwargs)
        parser = kwargs['parser']
        self.add_format_argument(parser)
        self.add_image_arguments(parser)


class IncursionRoomParser(parser.BaseParser):
    _files = [
        'IncursionRooms.dat',
    ]

    _incursion_column_index_filter = partialmethod(
        parser.BaseParser._column_index_filter,
        dat_file_name='IncursionRooms.dat',
        error_msg='Several incursion rooms have not been found:\n%s',
    )

    _COPY_KEYS = OrderedDict((
        ('Id', {
            'template': 'id',
        }),
        ('Name', {
            'template': 'name',
        }),
        ('Description', {
            'template': 'description',
            'format': lambda value: value.replace('\n', '<br />'),
        }),
        ('FlavourText', {
            'template': 'flavour_text',
            'format': lambda value: value.replace('\n', '<br />'),
        }),
        ('Tier', {
            'template': 'tier',
        }),
        ('RoomUpgrade_IncursionRoomsKey', {
            'template': 'upgrade_room_id',
            'format': lambda value: value['Id'],
            'condition': lambda value: value is not None,
        }),
        ('UIIcon', {
            'template': 'icon',
            'format': lambda value: value.replace(
                'Art/2DArt/UIImages/InGame/Incursion/Rooms/', ''),
        }),
        ('MinLevel', {
            'template': 'min_level',
            'default': 0,
        }),
        ('ModsKey', {
            'template': 'modifier_ids',
            'format': lambda value: value['Id'],
            'condition': lambda value: value is not None,
        }),
        #('IncursionArchitectKey', {
        #    'template': 'architect_metadata_id',
        #    'format': lambda value: value['MonsterVarietiesKey']['Id'],
        #    'condition': lambda value: value is not None,
        #}),
    ))

    _incursion_room_page_name = {
        'English': 'incursion room',
        'Russian': 'комната вмешательства',
    }

    def by_rowid(self, parsed_args):
        return self.export(
            parsed_args,
            self.rr['IncursionRooms.dat'][parsed_args.start:parsed_args.end],
        )

    def by_id(self, parsed_args):
        return self.export(parsed_args, self._incursion_column_index_filter(
            column_id='Id', arg_list=parsed_args.id
        ))

    def by_name(self, parsed_args):
        return self.export(parsed_args, self._incursion_column_index_filter(
            column_id='Name', arg_list=parsed_args.name
        ))

    def export(self, parsed_args, incursion_rooms):
        r = ExporterResult()

        if not incursion_rooms:
            console(
                'No incursion rooms  found for the specified parameters. '
                'Quitting.',
                msg=Msg.warning,
            )
            return r
        console('Found %s rooms...' % len(incursion_rooms))

        console('Additional files may be loaded. Processing information - this '
                'may take a while...')
        self._image_init(parsed_args)
        idl_sources = set()
        if parsed_args.store_images:
            idl = IDLFile()
            idl.read(file_path_or_raw=
                     self.ggpk['Art/UIImages1.txt'].record.extract())
            idl_lookup = idl.as_dict()

        console('Parsing data into templates...')
        for incursion_room in incursion_rooms:
            if 'TEMPLATE' in incursion_room['Id']:
                console(
                    'Skipping template room "%s"' % incursion_room['Id'],
                    msg=Msg.warning
                )
                continue
            elif not incursion_room['Name']:
                console(
                    'Skipping incursion room "%s" without a name' %
                    incursion_room['Id'],
                    msg=Msg.warning
                )
                continue
            data = OrderedDict()

            for row_key, copy_data in self._COPY_KEYS.items():
                value = incursion_room[row_key]

                condition = copy_data.get('condition')
                if condition is not None and not condition(incursion_room):
                    continue

                # Skip default values to reduce size of template
                if value == copy_data.get('default'):
                    continue

                fmt = copy_data.get('format')
                if fmt:
                    value = fmt(value)
                data[copy_data['template']] = value

            if incursion_room['IncursionArchitectKey']:
                mv = incursion_room['IncursionArchitectKey'][
                    'MonsterVarietiesKey']
                data['architect_metadata_id'] = mv['Id']
                data['architect_name'] = mv['Name']

            cond = IncursionRoomWikiCondition(
                data=data,
                cmdargs=parsed_args,
            )

            if parsed_args.store_images and self.ggpk and \
                    incursion_room['UIIcon']:
                idl_record = idl_lookup[incursion_room['UIIcon']]
                src = os.path.join(self._img_path, os.path.split(idl_record.source)[-1])
                if src not in idl_sources:
                    console(
                        'Writing source file "%s" to images' % src
                    )
                    with open(src, 'wb') as f:
                        img_data = extract_dds(
                            self.ggpk[
                            idl_record.source].record.extract().read(),
                            path_or_ggpk=self.ggpk,
                        )
                        f.write(img_data[:84])
                        if img_data[84:88].decode('ascii') == 'DXT4':
                            f.write('DXT5'.encode('ascii'))
                        else:
                            f.write(img_data[84:88])
                        f.write(img_data[88:])
                    idl_sources.add(src)

                os.system(
                    'magick "%(src)s" -crop %(w)sx%(h)s+%(x)s+%(y)s '
                    '"%(dst)s incursion room icon.png"' %
                    {
                        'src': src,
                        'dst': os.path.join(self._img_path, data['icon']),
                        'h': idl_record.h,
                        'w': idl_record.w,
                        'x': idl_record.x1,
                        'y': idl_record.y1,
                    }
                )

            r.add_result(
                text=cond,
                out_file='incursion_room_%s.txt' % data['name'],
                wiki_page=[
                    {
                        'page': data['name'],
                        'condition': cond,
                    },
                    {
                        'page': data['name'] + ' (%s)' % (
                            self._incursion_room_page_name[
                                config.get_option('language')
                            ]
                        ),
                        'condition': cond,
                    }
                ],
                wiki_message='Incursion room updater',
            )

        if idl_sources:
            console('Cleaning up image files that are no longer necessary')
            for src in idl_sources:
                os.remove(os.path.join(self._img_path, src))

        return r
