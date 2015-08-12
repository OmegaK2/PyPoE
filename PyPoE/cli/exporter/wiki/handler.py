"""
Path     PyPoE/cli/exporter/wiki/handler.py
Name     Wiki Export Handler
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Base classes and related functions for Wiki Export Handlers.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os

# 3rd-Party
from colorama import Fore

# self
from PyPoE.cli.handler import BaseHandler
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.wiki.util import check_hash

# =============================================================================
# Globals
# =============================================================================

__all__ = ['ExporterHandler', ]

# =============================================================================
# Classes
# =============================================================================

class ExporterHandler(BaseHandler):
    def get_wrap(self, cls, func, out_file, handler=None):
        def wrapper(pargs, *args, **kwargs):
            # Check Hash
            if not check_hash():
                print(Fore.LIGHTRED_EX + 'Game file hash mismatch. Please rerun setup.' + Fore.RESET)
                return -1
            # Check outdir, if specified:
            out_dir = pargs.outdir if pargs.outdir is not None else config.get_option('out_dir')
            temp_dir = config.get_option('temp_dir')
            data_dir = os.path.join(temp_dir, 'Data')
            desc_dir = os.path.join(temp_dir, 'Data')

            for item in (out_dir, data_dir, desc_dir):
                if not os.path.exists(item):
                    print(Fore.LIGHTREX_EX + 'Path "%s" does not exist' % item + Fore.RESET)
                    return -1

            if handler:
                return handler(pargs)
            else:
                print('Reading .dat files...')
                parser = cls(data_path=data_dir, desc_path=desc_dir)

                print('Parsing...')
                out = func(parser, pargs, *args, **kwargs)

                out_path = os.path.join(out_dir, out_file)
                print('Writing data to "%s"...' % out_path)
                with open(out_path, 'w') as f:
                    f.writelines(out)

                print('Done.')

                return 0
        return wrapper

    def add_default_parsers(self, parser, cls=None, func=None, outfile=None, handler=None):
        if handler is None:
            for item in (cls, func, outfile):
                if item is None:
                    raise ValueError('Must set either handler or (cls, func, outfile)')

        parser.set_defaults(func=self.get_wrap(cls, func, outfile, handler))
        parser.add_argument(
            '-d', '--outdir',
            help='Destination directory. If empty, uses current directory.'
        )