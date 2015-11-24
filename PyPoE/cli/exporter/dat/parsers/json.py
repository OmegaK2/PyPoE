"""
.dat export to JSON

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/dat/parsers/json.py                           |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

.dat export to JSON

Agreement
-------------------------------------------------------------------------------

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

        self.add_default_arguments(self.json)

    def handle(self, args):
        super(JSONExportHandler, self).handle(args)

        with open(args.target, mode='w') as f:
            dat_files = self._read_dat_files(args)

            console('Building data object...')
            out = []

            for file_name in args.files:
                out.append({
                    'filename': file_name,
                    'header': list(dat_files[file_name].reader.table_columns),
                    'data': dat_files[file_name].reader.table_data,
                })

            console('Dumping data to "%s"...' % args.target)

            dump(out, f)

        console('Done.')

# =============================================================================
# Functions
# =============================================================================
