"""
Wiki Export Base Parser

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/handler.py                               |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Base classes and related functions for Wiki Export Parsers.

Agreement
===============================================================================

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import os
from concurrent.futures import ThreadPoolExecutor

# 3rd Party
try:
    from PyPoE.cli.exporter import pywikibot_setup as pws
except Exception as e:
    pws = None

# self
from PyPoE.cli.core import console, Msg
from PyPoE.cli.handler import BaseHandler
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.util import check_hash

# =============================================================================
# Globals
# =============================================================================

__all__ = ['ExporterHandler', 'ExporterResult', 'WikiHandler']

# =============================================================================
# Classes
# =============================================================================

class WikiHandler(object):
    regex_search = None
    regex_replace = None

    def __init__(self, *a, name=None, rowmsg='Editing page "{page_name}"...\n'):
        self.name = name
        self.rowmsg = rowmsg

    def add_arguments(self, parser):
        parser.add_argument(
            '-w-mt', '--wiki-max-threads',
            dest='wiki_threads',
            help='Maximum number of threads to spawn when editing wiki',
            action='store',
            type=int,
            default=16,
        )
        parser.add_argument(
            '--dry-run',
            dest='dry_run',
            help='Don\'t actually save the wiki page and print it instead',
            action='store_true',
        )

    def save_page(self, page, text, message):
        if text == page.text:
            console('No update required. Skipping.')
            return

        if self.cmdargs.dry_run:
            print(text)
        else:
            page.text = text
            page.save(pws.get_edit_message(message))

    def handle_page(self, *a, row):
        page_name = row['wiki_page']
        if self.rowmsg:
            console(self.rowmsg.format(page_name=page_name))
        page = self.pws.pywikibot.Page(self.site, page_name)

        self.save_page(
            page=page,
            text=''.join(row['lines']),
            message=self.name,
        )

    def handle(self, *a, pws, result, cmdargs):
        site = pws.get_site()

        # First row is handled separately to prompt the user for his password
        self.site = site
        self.pws = pws
        self.cmdargs = cmdargs
        self.handle_page(row=result[0])

        tp = ThreadPoolExecutor(max_workers=cmdargs.wiki_threads)

        for row in result[1:]:
            tp.submit(
                self.handle_page,
                row=row,
            )

        tp.shutdown(wait=True)


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

            for item in (out_dir, temp_dir):
                if not os.path.exists(item):
                    console('Path "%s" does not exist' % item, msg=Msg.error)
                    return -1

            console('Reading .dat files...')
            parser = cls(base_path=temp_dir)

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
                    if pws is None:
                        try:
                            # Will raise the exception appropriately
                            __import__('PyPoE.cli.exporter.pywikibot_setup')
                        except ImportError:
                            console('Run pip install -e cli', msg=Msg.error)
                        except Exception:
                            raise

                    if wiki_handler is None:
                        console('No wiki-handler defined for this function', msg=Msg.error)
                        return 0

                    console('Running wikibot...')
                    console('-'*80)
                    wiki_handler.handle(pws=pws, result=result, cmdargs=pargs)
                    console('-'*80)
                    console('Completed wikibot execution.')

                console('Done.')

                return 0
        return wrapper

    def add_default_parsers(self, parser, cls, func=None, handler=None, wiki_handler=None):
        if handler is None:
            for item in (func,):
                if item is None:
                    raise ValueError('Must set either handler or func')

        if wiki_handler is not None:
            if not isinstance(wiki_handler, WikiHandler):
                raise TypeError('wiki_handler must be a WikiHandler instance.')

            wiki_handler.add_arguments(parser)

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
    def add_result(self, lines=None, out_file=None, wiki_page=None, **extra):
        data = {
            'lines': lines,
            'out_file': out_file,
            'wiki_page': wiki_page,
        }
        data.update(extra)

        self.append(data)
