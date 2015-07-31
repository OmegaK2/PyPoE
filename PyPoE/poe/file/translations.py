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

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import warnings
from collections import Iterable

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
        if len(values) and isinstance(values[0], Iterable):
            test_values = [value[0] for value in values]
            is_range = True
        else:
            test_values = values
            is_range = False

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

        valid_strings.append(ts.format_string(values, is_range))

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
            if is_range:
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
                if is_range:
                    values[index] = (f(values[index][0]), f(values[index][1]))
                else:
                    values[index] = f(values[index])

        return values

class DescriptionFile(object):
    regex_ids = re.compile('([0-9])(?(1)(.*))', re.UNICODE)
    regex_id_strings = re.compile('([\S]+)', re.UNICODE)
    regex_strings = re.compile('(?:"(.+)")|([\S]+)+', re.UNICODE)
    regex_int = re.compile('[0-9]+', re.UNICODE)
    regex_isnumber = re.compile('^[0-9\-]+$', re.UNICODE)

    def __init__(self, file_path=None):
        self._translations = []

        # Note str must be first since strings are iterable as well
        if isinstance(file_path, str):
            self._read(file_path)
        elif isinstance(file_path, Iterable):
            for path in file_path:
                self.merge(DescriptionFile(path))

    def _get_next(self, lines, regex):
        """
        Continues until the regex for the next line is non-empty

        :param lines:
        :param regex:
        :return:
        """
        while True:
            l = lines.__next__()
            result = re.findall(regex, l)
            if result:
                return result

    def _abc(self, translation, lines, lang=None):
        tl = TranslationLanguage(lang, parent=translation)
        tcount = int(self._get_next(lines, self.regex_int)[0])
        for i in range(0, tcount):
            data = self._get_next(lines, self.regex_strings)

            ts = TranslationString(parent=tl)
            ids_len = len(translation.ids)

            for i in range(0, ids_len):
                match = data[i][1]
                if match == '#':
                    TranslationRange(None, None, parent=ts)
                elif re.match(self.regex_isnumber, match):
                    value = int(match)
                    TranslationRange(value, value, parent=ts)
                elif '|' in match:
                    minmax = match.split('|')
                    min = int(minmax[0]) if minmax[0] != '#' else None
                    max = int(minmax[1]) if minmax[1] != '#' else None
                    TranslationRange(min, max, parent=ts)
                else:
                    raise Exception(match)

            ts.string = data[ids_len][0]


            tmp = iter(range(ids_len+1, len(data)))
            for i in tmp:
                match = data[i][1]
                # Adding q_ should avoid random clashes
                if hasattr(ts.quantifier, 'q_' + match):
                    getattr(ts.quantifier, 'q_' + match).append(int(data[i+1][1]))
                    tmp.__next__()
                else:
                    warnings.warn('Warning, uncaptured! %s' % match, UnknownIdentifierWarning)

    def _read(self, file_path):
        self._translations = []
        with open(file_path, encoding='utf-16_le') as descfile:
            lines = iter(descfile.readlines())
        try:
            item = None
            while True:
                if item is None:
                    item = lines.__next__()
                if not item.startswith('description'):
                    item = None
                    continue

                translation = Translation()

                # N(Ids) ID1 ID2 ... IDn
                ids = self._get_next(lines, self.regex_ids)
                if not ids:
                    warnings.warning('WTF')
                id_count = int(ids[0][0])
                ids = re.findall(self.regex_id_strings, ids[0][1])

                if len(ids) != id_count:
                    warnings.warn('Length mismatch for %s' % ids)
                translation.ids = ids

                # English Translation doesnt have a tag, so we can start this
                # way lazily
                language = 'English'
                while True:
                    self._abc(translation, lines, language)

                    # Do not replace with _get_next or it will skip new lines
                    # between descriptions and cause it to miss >_>
                    result = self._get_next(lines, self.regex_strings)
                    if len(result) != 2 or result[0][1] == 'description':
                        # sets item to description
                        item = result[0][1]
                        break

                    language = ''.join(result[1])

                self._translations.append(translation)
        except StopIteration:
            pass

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
    print(t)