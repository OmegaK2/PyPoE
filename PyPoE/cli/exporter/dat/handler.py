"""
.dat export base handler

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/dat/handler.py                                |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

.dat export base handler

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python

# 3rd-party
from tqdm import tqdm

# self
from PyPoE.poe.constants import VERSION
from PyPoE.poe.file import dat
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.util import get_content_ggpk, get_content_ggpk_path

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class DatExportHandler:
    def add_default_arguments(self, parser):
        """

        :param parser:
        :type parser: argparse.ArgumentParser

        :return:
        """
        parser.set_defaults(func=self.handle)
        parser.add_argument(
            '--files', '--file',
            help='.dat files to export',
            nargs='*',
        )

        parser.add_argument(
            '-lang', '--language',
            help='Language subdirectory to use',
            dest='language',
            default=None,
        )

    def handle(self, args):
        ver = config.get_option('version')

        if ver != VERSION.DEFAULT:
            console('Loading specification for %s' % ver)
            dat.set_default_spec(version=ver)

        spec = dat._default_spec
        if args.files is None:
            args.files = list(spec)
        else:
            files = set()

            for file_name in args.files:
                if file_name in spec:
                    files.add(file_name)
                elif not file_name.endswith('.dat'):
                    file_name += '.dat'
                    if file_name not in spec:
                        console('.dat file "%s" is not in specification. Removing.' % file_name, msg=Msg.error)
                    else:
                        files.add(file_name)

            files = list(files)
            files.sort()
            args.files = files

        args.spec = spec

    def _read_dat_files(self, args, prefix=''):
        path = get_content_ggpk_path()

        console(prefix + 'Reading "%s"...' % path)

        ggpk = get_content_ggpk(path)

        console(prefix + 'Reading .dat files')

        dat_files = {}
        ggpk_data = ggpk['Data']
        lang = args.language or config.get_option('language')
        if lang != 'English':
            ggpk_data = ggpk_data[lang]
        remove = []
        for name in tqdm(args.files):
            try:
                node = ggpk_data[name]
            except FileNotFoundError:
                console('Skipping "%s" (missing)' % name, msg=Msg.warning)
                remove.append(name)
                continue

            df = dat.DatFile(name)
            df.read(file_path_or_raw=node.record.extract(), use_dat_value=False)

            dat_files[name] = df

        for file_name in remove:
            args.files.remove(file_name)

        return dat_files


# =============================================================================
# Functions
# =============================================================================
