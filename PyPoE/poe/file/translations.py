"""
Path     PyPoE/poe/file/translations.py
Name     Utilities for accessing GGG translations
Version  1.00.000
Revision $Id$
Author   [#OMEGA]- K2

INFO

Utilities for parsing and using GGG translations.

The translation GGG provides are generally suffixed by _descriptions.txt and
can be found in the MetaData/ folder.
To read those, use the class DescriptionFile.


AGREEMENT

See PyPoE/LICENSE


TODO

optimize
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import warnings
from collections import Iterable

# =============================================================================
# Globals
# =============================================================================

__all__ = ['DescriptionFile']

regex_translation_string = re.compile('''^
[\s]*
(?P<minmax>(?:[0-9\-\|#]+[ \t]+)+)
"(?P<description>.*)"
(?P<quantifier>(?:[ \t]+[\w]+[ \t]+[0-9]+)*)
[ \t]*
$'''.replace('\n', ''), re.UNICODE | re.MULTILINE)

regex_ids = re.compile('([0-9])(?(1)(.*))', re.UNICODE)
regex_id_strings = re.compile('([\S]+)', re.UNICODE)
regex_strings = re.compile('(?:"(.+)")|([\S]+)+', re.UNICODE)
regex_int = re.compile('[0-9]+', re.UNICODE)
regex_isnumber = re.compile('^[0-9\-]+$', re.UNICODE)
regex_lang = re.compile('^[\s]*lang "(?P<language>[\w ]+)"[\s]*$', re.UNICODE | re.MULTILINE)
regex_tokens = re.compile(r"""(?:^"(?P<header>.*)"$)
|(?:^include "(?P<include>.*)"$)
|(?:^no_description (?P<no_description>[\w+%]*)$)
|(?P<description>^description)
""", re.UNICODE | re.MULTILINE)

# =============================================================================
# Classes
# =============================================================================

class UnknownIdentifierWarning(UserWarning):
    pass

class Translation(object):
    def __init__(self):
        self.languages = []
        self.ids = []

    def get_language(self, language):
        etr = None
        for tr in self.languages:
            if tr.language == language:
                return tr
            elif tr.language == 'English':
                etr = tr

        return etr

class TranslationLanguage(object):
    def __init__(self, language, parent):
        parent.languages.append(self)
        self.parent = parent
        self.language = language
        self.strings = []

    def get_string(self, values, indexes):
        valid_strings = []

        # Support for ranges
        is_range = []
        test_values = []
        short_values = []
        for item in values:
            if isinstance(item, Iterable):
                test_values.append(item[0])
                if item[0] == item[1]:
                    short_values.append(item[0])
                    is_range.append(False)
                else:
                    short_values.append(item)
                    is_range.append(True)
            else:
                test_values.append(item)
                short_values.append(item)
                is_range.append(False)

        temp = []
        for ts in self.strings:
            # TODO: check whether this really is a non issue now
            #if len(values) != len(ts.range):
            #   raise Exception('mismatch %s' % ts.range)

            match = ts.match_range(test_values, indexes)
            temp.append((match, ts))

        # Only the highest scoring/matching translation...
        temp.sort(key=lambda x: -x[0])
        ts = temp[0][1]

        valid_strings.append(ts.format_string(short_values, is_range))

        return valid_strings


class TranslationString(object):
    def __init__(self, parent):
        parent.strings.append(self)
        self.parent = parent
        self.quantifier = TranslationQuantifier()
        self.range = []
        self.string = ''

    def format_string(self, values, is_range):
        values = self.quantifier.handle(values, is_range)
        s = self.string.replace('%%', '%')
        for i in range(0, len(values)):
            if is_range[i]:
                rpl = '(%s to %s)' % tuple(values[i])
            else:
                rpl = str(values[i])
            s = s.replace('%%%s%%' % (i+1), rpl)
            s = s.replace('%%%s$+d' % (i+1), rpl)
        return s

    def match_range(self, values, indexes):
        rating = 0
        for i in indexes:
            rating += self.range[i].in_range(values[i])
        return rating

class TranslationRange(object):
    def __init__(self, min, max, parent):
        parent.range.append(self)
        self.parent = parent
        self.min = min
        self.max = max

    def __repr__(self):
        return 'TranslationRange(%s, %s, %s)' % (self.min, self.max, hex(id(self.parent)))

    def in_range(self, value):
        # Any range is accepted
        if self.min is None and self.max is None:
            return 1

        if self.min is None and value <= self.max:
            return 2

        if self.max is None and value >= self.min:
            return 2

        if self.min is not None and self.max is not None:
            if self.min <= value <= self.max:
                return 3

        return 0


class TranslationQuantifier(object):
    handlers = {
        'deciseconds_to_seconds': lambda v: v*10,
        'divide_by_one_hundred': lambda v: v/100,
        'per_minute_to_per_second': lambda v: v*60,
        'milliseconds_to_seconds': lambda v: v/1000,
        'negate': lambda v: v*-1,
        # TODO: check accuracy of those values
        'old_leech_percent': lambda v: v/5,
        'old_leech_permyriad': lambda v: v/50,
        # TODO dp = precision?
        'per_minute_to_per_second_0dp': lambda v: v*60,
        'per_minute_to_per_second_2dp': lambda v: round(v*60, 2),
        'milliseconds_to_seconds_0dp': lambda v: round(v/1000, 0),
        'milliseconds_to_seconds_2dp': lambda v: round(v/1000, 2),
        # Only once TODO
        'multiplicative_damage_modifier': lambda v: v,
        'mod_value_to_item_class': lambda v: v,
    }

    def __init__(self):
        for handler_name in self.handlers:
            setattr(self, 'q_' + handler_name, [])

    def handle(self, values, is_range):
        values = list(values)
        for handler_name in self.handlers:
            f = self.handlers[handler_name]
            for index in getattr(self, 'q_' + handler_name):
                index -= 1
                if is_range[index]:
                    values[index] = (f(values[index][0]), f(values[index][1]))
                else:
                    values[index] = f(values[index])

        return values

class DescriptionFile(object):


    def __init__(self, file_path=None):
        self._translations = []

        # Note str must be first since strings are iterable as well
        if isinstance(file_path, str):
            self._read(file_path)
        elif isinstance(file_path, Iterable):
            for path in file_path:
                self.merge(DescriptionFile(path))

    def _read(self, file_path):
        self._translations = []
        with open(file_path, encoding='utf-16_le') as descfile:
            data = descfile.read()

        # starts with bom?
        offset = 0
        match =regex_tokens.search(data, offset)
        while match is not None:
            offset = match.end()
            match_next = regex_tokens.search(data, offset)
            offset_max = match_next.start() if match_next else len(data)
            if match.group('description'):
                translation = Translation()

                # Parse the IDs for the translations
                ids = regex_ids.search(data, offset, offset_max)
                if ids is None:
                    warnings.warning('Missing ID after description')

                offset = ids.end()

                ids = ids.group().split(maxsplit=1)
                id_count = int(ids[0])
                ids = re.findall(regex_id_strings, ids[1])

                if len(ids) != id_count:
                    warnings.warn('Length mismatch for %s' % ids)
                translation.ids = ids
                t = True
                language = 'English'
                while t:
                    tl = TranslationLanguage(language, parent=translation)
                    tcount = regex_int.search(data, offset, offset_max)
                    offset = tcount.end()
                    language_match = regex_lang.search(data, offset, offset_max)

                    if language_match is None:
                        offset_next_lang = offset_max
                        t = False
                    else:
                        offset_next_lang = language_match.start()
                        language = language_match.group('language')

                    for i in range(0, int(tcount.group())):
                        ts_match = regex_translation_string.search(data, offset, offset_next_lang)
                        if not ts_match:
                            print(data[offset:offset_max])
                            raise Exception()

                        offset = ts_match.end()

                        ts = TranslationString(parent=tl)

                        # Min/Max limiter
                        limiter = ts_match.group('minmax').strip().split()
                        for i in range(0, id_count):
                            matchstr = limiter[i]
                            if matchstr == '#':
                                TranslationRange(None, None, parent=ts)
                            elif regex_isnumber.match(matchstr):
                                value = int(matchstr)
                                TranslationRange(value, value, parent=ts)
                            elif '|' in matchstr:
                                minmax = matchstr.split('|')
                                min = int(minmax[0]) if minmax[0] != '#' else None
                                max = int(minmax[1]) if minmax[1] != '#' else None
                                TranslationRange(min, max, parent=ts)
                            else:
                                raise Exception(matchstr)

                        ts.string = ts_match.group('description')

                        quant = ts_match.group('quantifier').strip().split()
                        tmp = iter(range(0, len(quant)))
                        for i in tmp:
                            quantifier_name = 'q_' + quant[i]
                            # Adding q_ should avoid random clashes
                            if hasattr(ts.quantifier, quantifier_name):
                                getattr(ts.quantifier, quantifier_name).append(int(quant[i+1]))
                                tmp.__next__()
                            else:
                                #print(ts_match.group(), ids)
                                #raise Exception('Warning, uncaptured! %s' % quantifier_name[2:])
                                warnings.warn('Warning, uncaptured! %s' % quantifier_name[2:], UnknownIdentifierWarning)

                    offset = offset_next_lang

                self._translations.append(translation)
            elif match.group('no_description'):
                pass
            elif match.group('include'):
                pass
            elif match.group('header'):
                pass

            # Done, search next
            match = match_next

    def merge(self, other):
        if not isinstance(other, DescriptionFile):
            TypeError('Wrong type: %s' % type(other))
        self._translations += other._translations

    def get_translation(self, tags, values, lang='English'):
        # A single translation might have multiple references
        # I.e. the case for always_freeze

        if isinstance(tags, str):
            tags = [tags, ]

        trans_found = {}
        for tag in tags:
            for tr in self._translations:
                try:
                    index = tr.ids.index(tag)
                except ValueError:
                    continue
                if tr in trans_found:
                    trans_found[tr].append(index)
                    continue
                trans_found[tr] = [index, ]

        trans_lines = []
        for tr in trans_found:
            indexes = trans_found[tr]

            tl = tr.get_language(lang)
            result = tl.get_string(values, indexes)
            if result:
                trans_lines += result
        return trans_lines

if __name__ == '__main__':
    s = DescriptionFile('C:/Temp/stat_descriptions.txt')
    t = s.get_translation(tags=['life_regeneration_rate_+%'], values=(-2, ))
    print('Translation:', t)