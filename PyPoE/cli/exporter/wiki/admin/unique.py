"""
Copy unique items

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/cli/exporter/wiki/admin/admin.py                           |
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

TODO-List
===============================================================================

Documentation
===============================================================================
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import traceback
from collections import defaultdict

# 3rd-party
import mwclient
import mwparserfromhell
from rapidfuzz import fuzz

# self
from PyPoE.poe.constants import WORDLISTS
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.cli.core import console, Msg
from PyPoE.cli.exporter.wiki.parser import BaseParser
from PyPoE.cli.exporter.wiki.handler import ExporterHandler, add_parser_arguments, WIKIS

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class UniqueCommandHandler(ExporterHandler):
    def __init__(self, sub_parser):
        self.parser = sub_parser.add_parser(
            'unique',
            help='Unique item administrative utility functions',
        )
        self.parser.set_defaults(func=lambda args: self.parser.print_help())
        sub = self.parser.add_subparsers()

        copy = sub.add_parser(
            'copy',
            help='Copy unique item data from English wiki and translate various strings'
        )

        add_parser_arguments(copy)
        copy.add_argument(
            '-en-w-u', '--english-wiki-user',
            dest='en_user',
            help='Gamepedia user name to use to login into the English wiki (source). Bot access speeds things up.',
            action='store',
            type=str,
            default='',
        )

        copy.add_argument(
            '-en-w-p', '-en-w-pw', '--english-wiki-password',
            dest='en_password',
            help='Gamepedia password to use to login into the English wiki (source). Bot access speeds things up.',
            action='store',
            type=str,
            default='',
        )

        copy.add_argument(
            '-uf', '-cuf', '-c-uf', '--copy-upgraded-from',
            dest='copy_upgraded_from',
            help='Copy upgraded from',
            action='store_true',
            default=False,
        )

        copy.add_argument(
            'page',
            help='page of the unique item to process',
            nargs='+',
        )
        copy.set_defaults(func=self.get_wrap(
            cls=UniqueCopy,
            func=None,
            handler=UniqueCopy.run,
            wiki_handler=None,
        ))


class UniqueCopy(BaseParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set this up at the earlist so no processing time is wasted
        if not self.parsed_args.user or not self.parsed_args.password:
            raise ValueError('User login to target wiki is required for this operation.')

        self.site_english = mwclient.Site(WIKIS['English'], path='/', scheme='https')
        self.site_english.login(self.parsed_args.en_user, self.parsed_args.en_password)
        self.site_other = mwclient.Site(WIKIS[self.lang], path='/', scheme='https')
        self.site_other.login(self.parsed_args.user, self.parsed_args.password)

        if self.lang == 'English':
            raise ValueError('Can\'t export unique items TO English wiki')

        self.rr_english = RelationalReader(
            path_or_ggpk=self.base_path,
            raise_error_on_missing_relation=False,
            read_options={
                'use_dat_value': False,
                'auto_build_index': True,
            },
            language='English'
        )

        console('Creating lookup cache...')
        self.words = []
        for row in self.rr_english['Words.dat']:
            if row['WordlistsKey'] == WORDLISTS.UNIQUE_ITEM:
                self.words.append(row)

        self.cache = defaultdict(BaseItemCacheInstance)
        for row in self.rr_english['BaseItemTypes.dat']:
            self.cache[row['ItemClassesKey']['Id']].append(row)
            self.cache[row['ItemClassesKey']['Id']].index['Name'][row['Name']].append(row)

    def fuzzy_find_text(self, text, file_name, key, source_list=None, fuzzy_func=fuzz.partial_ratio):
        text = text.strip()

        if source_list is None:
            source_list = self.rr_english[file_name]

        # Try faster indexed search first and see if we get any perfect results
        if key not in self.rr_english[file_name].index:
            self.rr_english[file_name].build_index(key)
        results = self.rr_english[file_name].index[key][text]
        if len(results) == 1:
            return self.rr[file_name][results[0].rowid][key]

        # Try to find translation for the name using fuzzy search
        results = []
        for row in source_list:
            ratio = fuzzy_func(row[key], text)
            if ratio > 90:
                results.append({
                    'id': row.rowid,
                    'text': row[key],
                    'ratio': ratio,
                })

        if len(results) == 0:
            console('No matching text found.')
            text = input('Enter translated text.\n')
            if text == '':
                console('No text specified - skipping search for "%s".' % text)
                return
            return text
        elif len(results) >= 2:
            console('Multiple matching names found.\n')
            for i, row in enumerate(results):
                row['i'] = i
                console('%(i)s: %(ratio)s\n%(text)s\n----------------' % row)

            try:
                correct = results[int(input('Enter index of correct translation:\n'))]
            except Exception as e:
                traceback.print_exc()

            return self.rr[file_name][correct['id']][key]
        else:
            return self.rr[file_name][results[0]['id']][key]

    def copy(self, pn):
        console('Processing %s' % pn)
        page = self.site_english.pages[pn]
        if not page.exists:
            raise Exception('Page %s not found' % pn)

        mwtext = mwparserfromhell.parse(page.text())
        for mwtemplate in mwtext.filter_templates():
            if mwtemplate.name.strip().lower() == 'item':
                break
        else:
            raise Exception('Item template not found')

        console('Finding flavour text...')
        if not mwtemplate.has('flavour_text_id') and mwtemplate.has('flavour_text'):
            console('Missing flavour_text_id. Trying to find flavour text in FlavourText.dat')

            ftext = self.fuzzy_find_text(
                mwtemplate.get('flavour_text'),
                'FlavourText.dat',
                'Text',
                fuzzy_func=fuzz.partial_token_set_ratio
            )

            results = []
            for row in self.rr_english['FlavourText.dat']:
                ratio = fuzz.partial_token_set_ratio(row['Text'], ftext)
                if ratio > 90:
                    results.append({
                        'id': row['Id'],
                        'text': row['Text'],
                        'ratio': ratio,
                    })

            if len(results) == 0:
                console('No matching flavour text found.')
                text = input('Enter translated flavour text. Type None to skip item entirely.\n')
                if text == 'None':
                    console('Skipping item %s.' % pn)
                    return
                mwtemplate.get('flavour_text').value = text
            elif len(results) >= 2:
                console('Multiple matching flavour text entries found.\n')
                for i, row in enumerate(results):
                    row['i'] = i
                    console('%(i)s %(id)s: %(ratio)s\n%(text)s\n----------------' % row)

                try:
                    correct = results[int(input('Enter index of correct translation.'))]
                except Exception as e:
                    traceback.print_exc()

                mwtemplate.get('flavour_text_id').value = correct['id']
            else:
                mwtemplate.get('flavour_text_id').value = results[0]['id']

        # Grab flavour text from other language
        if mwtemplate.has('flavour_text_id'):
            mwtemplate.get('flavour_text').value = ' %s\n' % self.rr['FlavourText.dat'].index['Id'][
                mwtemplate.get('flavour_text_id').value.strip()]['Text'].replace('\r', '').replace('\n', '<br>')

        # Need this for multiple things
        name = mwtemplate.get('name').value.strip()

        # Add inventory icon so it shows up correctly
        if not mwtemplate.has('inventory_icon'):
            mwtemplate.add('{0: <40}'.format('inventory_icon'), name)

        # Find translated item name
        console('Finding item name...')
        new = self.fuzzy_find_text(name, 'Words.dat', 'Text2', source_list=self.words)
        if new is None:
            console('Didn\'t get an english name for this item, skipping.')
            return

        mwtemplate.get('name').value = ' %s\n' % new

        # Find the correct name of the base item
        console('Finding base item...')
        if mwtemplate.has('base_item_id'):
            # TODO
            pass
        elif mwtemplate.has('base_item_page'):
            # TODO
            pass
        elif mwtemplate.has('base_item'):
            base = self.fuzzy_find_text(
                mwtemplate.get('base_item'),
                'BaseItemTypes.dat',
                'Name',
                source_list=self.cache[mwtemplate.get('class_id').value.strip()]
            )
            if base is None:
                console('Base item is required for unique items. Skipping.')
                return

            mwtemplate.get('base_item').value = ' %s\n' % base

        if self.parsed_args.copy_upgraded_from:
            # TODO
            pass
        else:
            # Need to copy the list or it won't be deleted properly as it deletes from itself during iteration
            for mwparam in list(mwtemplate.params):
                pname = mwparam.name.strip()
                if pname.startswith('upgraded_from'):
                    mwtemplate.remove(mwparam.name)
                elif pname in ('class'):
                    mwtemplate.remove(mwparam.name)

        if mwtemplate.has('drop_text'):
            console('Drop text might need a translation. Current text:\n\n%s' % mwtemplate.get('drop_text').value.strip())
            text = input('\nNew text (leave empty to copy old):\n')
            if text:
                mwtemplate.get('drop_text').value = ' %s\n' % text

        console('Saving on other wiki...')
        if pn == name:
            page = self.site_other.pages[new]
        else:
            console('Name of page doesn\'t equal item name. \nOld: %s\nItem:%s' % (pn, new))
            cont = True
            while cont:
                t = '%s (%s)' % (new, input('Enter phrase for parenthesis:\n'))
                console('Is this correct?:\n%s' % t)
                cont = input('y/n?\n') != 'y'
            page = self.site_other.pages[t]

        page.save('%s\n\n[[en:%s]]' % (str(mwtemplate), pn))
        console('Done.')

    def run(self, parsed_args, **kwargs):
        console('Parsing...')
        for item in parsed_args.page:
            self.copy(item)


class BaseItemCacheInstance(list):
    index = {'Name': defaultdict(list)}

# =============================================================================
# Functions
# =============================================================================

def run():
    cache = defaultdict(BaseItemCacheInstance)
    for row in self.rr_english['BaseItemTypes.dat']:
        cache[row['ItemClassesKey']['Id']].append(row)
        cache[row['ItemClassesKey']['Id']].index['Name'][row['Name']].append(row)


    for pn in ['Bubonic Trail (1 Abyssal Socket)']:
        copy(pn, cache)

    '''from line_profiler import LineProfiler
    profiler = LineProfiler(
        fuzzy_find_text,
        find,
    )
    profiler.runcall(copy, "Brightbeak", cache)
    profiler.print_stats()'''

#run()