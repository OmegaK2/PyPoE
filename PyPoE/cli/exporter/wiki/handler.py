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

# 3rd Party
try:
    import pywikibot
except Exception as e:
    pywikibot = None

# self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.handler import BaseHandler
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.wiki.util import check_hash

# =============================================================================
# Globals
# =============================================================================

__all__ = ['ExporterHandler', 'ExporterResult']

# =============================================================================
# Classes
# =============================================================================

class ExporterHandler(BaseHandler):
    def get_wrap(self, cls, func, handler, wiki_handler):
        def wrapper(pargs, *args, **kwargs):
            # Check Hash
            if not check_hash():
                console('Game file hash mismatch. Please rerun setup.', msg=Msg.error)
                return -1
            # Check outdir, if specified:
            out_dir = pargs.outdir if pargs.outdir is not None else config.get_option('out_dir')
            temp_dir = config.get_option('temp_dir')
            data_dir = os.path.join(temp_dir, 'Data')
            desc_dir = os.path.join(temp_dir, 'Metadata')

            for item in (out_dir, data_dir, desc_dir):
                if not os.path.exists(item):
                    console('Path "%s" does not exist' % item, msg=Msg.error)
                    return -1

            console('Reading .dat files...')
            parser = cls(data_path=data_dir, desc_path=desc_dir)

            console('Parsing...')
            if handler:
                return handler(parser, pargs, out_dir=out_dir)
            else:
                result = func(parser, pargs, *args, **kwargs)

                for item in result:
                    if pargs.print:
                        console(''.join(item['lines']))

                    if pargs.write:
                        out_path = os.path.join(out_dir, item['out_file'])
                        console('Writing data to "%s"...' % out_path)
                        with open(out_path, 'w') as f:
                            f.writelines(item['lines'])

                    if pargs.wiki:
                        if pywikibot is None:
                            try:
                                # Will raise the exception appropriately
                                __import__('pywikibot')
                            except ImportError:
                                console('Run pip install -e cli', msg=Msg.error)
                            except Exception:
                                raise

                        console(result['wiki_page'])

                console('Done.')

                return 0
        return wrapper

    def add_default_parsers(self, parser, cls, func=None, handler=None, wiki_handler=None):
        if handler is None:
            for item in (func,):
                if item is None:
                    raise ValueError('Must set either handler or func')

        parser.set_defaults(func=self.get_wrap(cls, func, handler, wiki_handler))
        parser.add_argument(
            '-d', '--outdir',
            help='Destination directory. If empty, uses current directory.'
        )
        parser.add_argument(
            '-p', '--print',
            help='Print the contents of the file',
            action='store_true',
        )
        parser.add_argument(
            '--write',
            help='Write to file',
            action='store_true',
        )
        parser.add_argument(
            '--wiki',
            help='Write to the gamepedia page (requires pywikibot)',
            action='store_true',
        )


class ExporterResult(list):
    def add_result(self, lines=None, out_file=None, wiki_page=None):
        self.append({
            'lines': lines,
            'out_file': out_file,
            'wiki_page': wiki_page,
        })
