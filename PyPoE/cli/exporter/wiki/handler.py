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
from collections import Iterable
from concurrent.futures import ThreadPoolExecutor

# 3rd Party
try:
    import mwclient
except Exception as e:
    mwclient = None

# self
from PyPoE import __version__
from PyPoE.cli.core import console, Msg
from PyPoE.cli.handler import BaseHandler
from PyPoE.cli.exporter import config
from PyPoE.cli.exporter.util import check_hash

# =============================================================================
# Globals
# =============================================================================

__all__ = ['ExporterHandler', 'ExporterResult', 'WikiHandler',
           'add_format_argument']

# =============================================================================
# Classes
# =============================================================================


class WikiHandler(object):
    def add_arguments(self, parser):
        parser.add_argument(
            '-w', '--wiki',
            help='Write to the gamepedia page (requires pywikibot)',
            action='store_true',
        )

        parser.add_argument(
            '-w-u', '--wiki-user',
            dest='user',
            help='Gamepedia user name to use to login into the wiki',
            action='store',
            type=str,
            default='',
        )

        parser.add_argument(
            '-w-p', '-w-pw', '--wiki-password',
            dest='password',
            help='Gamepedia password to use to login into the wiki',
            action='store',
            type=str,
            default='',
        )

        parser.add_argument(
            '-w-mt', '--wiki-max-threads',
            dest='wiki_threads',
            help='Maximum number of threads to spawn when editing wiki',
            action='store',
            type=int,
            default=1,
        )

        parser.add_argument(
            '-w-dr', '--wiki-dry-run',
            dest='dry_run',
            help='Don\'t actually save the wiki page and print it instead',
            action='store_true',
        )

    def handle_page(self, *a, row):
        if isinstance(row['wiki_page'], str):
            pages = [
                {'page': row['wiki_page'], 'condition': None},
            ]
        else:
            pages = row['wiki_page']
        console('Scanning for wiki page candidates "%s"' %
                ', '.join([p['page'] for p in pages]))
        page_found = False
        new = False
        for pdata in pages:
            page = self.site.pages[pdata['page']]
            if page.exists:
                condition = pdata.get('condition')
                success = True
                if condition is None:
                    console(
                        'No conditions given - page content on "%s" will be '
                        'overriden' % pdata['page'],
                        msg=Msg.warning,
                    )
                    success = True
                elif callable(condition):
                    success = condition(page=page)
                elif isinstance(condition, Iterable):
                    for cond in condition:
                        success = cond(page=page)
                        if not success:
                            break
                else:
                    raise ValueError('Invalid condition type "%s"' %
                                     type(condition))
                if success:
                    console('All conditions met on page "%s". Editing.' %
                            pdata['page'])
                    page_found = True
                    break
                else:
                    console(
                        'One or more conditions failed on page "%s". Skipping.'
                        % pdata['page'], msg=Msg.warning
                    )
            else:
                console('Page "%s" does not exist. It will be created.' %
                        pdata['page'])
                page_found = True
                new = True
                break

        if page_found:
            text = row['text']
            if callable(text):
                kwargs = {}
                if not new:
                    kwargs['page'] = page
                text = text(**kwargs)

            if text == page.text():
                console('No update required. Skipping.')
                return

            if self.cmdargs.dry_run:
                console(text)
            else:
                response = page.save(
                    text=text,
                    summary='PyPoE/ExporterBot/%s: %s' %
                            (__version__, row['wiki_message'])
                )
                if response['result'] == 'Success':
                    console('Page was edited successfully (time: %s)' %
                            response['newtimestamp'])
                else:
                    #TODO: what happens if it fails?
                    console('Something went wrong, status code:', msg=Msg.error)
                    console(response, msg=Msg.error)
        else:
            console(
                'No wiki page candidates found, skipping this row.',
                msg=Msg.error,
            )

    def handle(self, *a, mwclient, result, cmdargs, parser):
        # First row is handled separately to prompt the user for his password
        self.site = mwclient.Site(
            ('http', 'pathofexile.gamepedia.com'),
            path='/'
        )

        self.site.login(
            username=cmdargs.user or input('Enter your gamepedia user name:\n'),
            password=cmdargs.password or input(
                'Please enter your password for the specified user\n'
                'WARNING: Password will be visible in console\n'
            ),
        )
        self.mwclient = mwclient
        self.cmdargs = cmdargs
        self.parser = parser


        if cmdargs.wiki_threads > 1:
            console('Starting thread pool...')
            tp = ThreadPoolExecutor(max_workers=cmdargs.wiki_threads)

            for row in result:
                tp.submit(
                    self.handle_page,
                    row=row,
                )

            tp.shutdown(wait=True)
        else:
            console('Editing pages...')
            for row in result:
                self.handle_page(row=row)


class ExporterHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(ExporterHandler, self).__init__(*args, **kwargs)

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
                    if callable(item['text']):
                        text = item['text']()
                    else:
                        text = item['text']
                    if pargs.print:
                        console(text)

                    if pargs.write:
                        out_path = os.path.join(out_dir, item['out_file'])
                        console('Writing data to "%s"...' % out_path)
                        with open(out_path, 'w') as f:
                            f.write(text)

                if pargs.wiki:
                    if mwclient is None:
                        try:
                            # Will raise the exception appropriately
                            __import__('')
                        except ImportError:
                            console('Run pip install -e cli', msg=Msg.error)
                        except Exception:
                            raise

                    if wiki_handler is None:
                        console('No wiki-handler defined for this function',
                                msg=Msg.error)
                        return 0

                    console('Running wikibot...')
                    console('-'*80)
                    wiki_handler.handle(mwclient=mwclient, result=result, cmdargs=pargs,
                                        parser=parser)
                    console('-'*80)
                    console('Completed wikibot execution.')

                console('Done.')

                return 0
        return wrapper

    def add_default_parsers(self, parser, cls, func=None, handler=None,
                            wiki=True, wiki_handler=None):
        if handler is None:
            for item in (func,):
                if item is None:
                    raise ValueError('Must set either handler or func')

        if wiki:
            if wiki_handler is not None:
                if not isinstance(wiki_handler, WikiHandler):
                    raise TypeError('wiki_handler must be a WikiHandler '
                                    'instance.')
            else:
                wiki_handler = WikiHandler()
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
            '-wr', '--write',
            help='Write to file',
            action='store_true',
        )


class ExporterResult(list):
    def add_result(self, text=None, out_file=None, wiki_page=None,
                   wiki_message='', **extra):
        data = {
            'text': text,
            'out_file': out_file,
            'wiki_page': wiki_page,
            'wiki_message': wiki_message,
        }
        data.update(extra)

        self.append(data)


# =============================================================================
# Functions
# =============================================================================


def add_format_argument(parser):
    parser.add_argument(
        '--format',
        help='Output format',
        choices=['template', 'module'],
        default='template',
    )