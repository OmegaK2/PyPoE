"""
.dat export to JSON

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/dat/parsers/json.py                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

.dat export to JSON

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import argparse
from json import dump

# self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.dat.handler import DatExportHandler

# =============================================================================
# Globals
# =============================================================================

__all__ = ['JSONExportHandler']

# =============================================================================
# Classes
# =============================================================================


class JSONExportHandler(DatExportHandler):
    def __init__(self, sub_parser):
        """

        :type sub_parser: argparse._SubParsersAction
        """
        self.json = sub_parser.add_parser(
            'json',
            help='Export to JSON',
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self.json.add_argument(
            'target',
            help='target to export to',
        )

        self.json.add_argument(
            '--use-object-format',
            help='Export files as objects as row and header instead of lists. '
                 'Will significantly increase the the size of the export',
            dest='use_object_format',
            action='store_true',
        )

        self.json.add_argument(
            '--include-virtual-fields',
            help='includes virtual_fields from the spec',
            dest='include_virtual_fields',
            action='store_true',
        )

        self.json.add_argument(
            '--force-ascii-format',
            help='Will enforce the json file to be written as ascii, escaping '
                 'unicode characters using python escapes accordingly',
            dest='ascii',
            action='store_true',
        )

        self.json.add_argument(
            '--include-record-length',
            help='Save the table record length of a DAT file',
            dest='include_record_length',
            action='store_true',
        )

        self.add_default_arguments(self.json)

    def handle(self, args):
        super().handle(args)

        dict_spec = args.spec.as_dict()

        with open(
                args.target,
                mode='w',
                encoding='ascii' if args.ascii else 'utf-8'
        ) as f:
            dat_files = self._read_dat_files(args)

            console('Building data object...')
            out = []

            for file_name in args.files:
                dat_file = dat_files[file_name]
                
                header = [
                    dict({ 'name': name, 'rowid': index }, **props)
                    for index, (name, props) 
                    in enumerate(dict_spec[file_name]['fields'].items())
                ]

                virtual_header = [
                    dict({ 'name': name, 'rowid': index }, **props)
                    for index, (name, props) 
                    in enumerate(dict_spec[file_name]['virtual_fields'].items())
                ]

                if args.use_object_format:
                    out_obj = {
                        'filename': file_name,
                        'header': {row['name']: row for row in header},
                        'data': [{
                                cid: row[i] for i, cid in enumerate(
                                    dat_file.reader.columns_data
                                )
                            } for row in dat_file.reader.table_data
                        ],
                    }

                    virtual_header = (
                        {row['name']: row for row in virtual_header}
                    )
                else:
                    out_obj = {
                        'filename': file_name,
                        'header': header,
                        'data': dat_file.reader.table_data,
                    }

                if args.include_virtual_fields:
                    out_obj['virtual_header'] = virtual_header

                if args.include_record_length:
                    out_obj['record_length'] = dat_files[file_name].reader.table_record_length

                out.append(out_obj)

            console('Dumping data to "%s"...' % args.target)

            dump(out, f, ensure_ascii=args.ascii, indent=4)

        console('Done.')

# =============================================================================
# Functions
# =============================================================================
