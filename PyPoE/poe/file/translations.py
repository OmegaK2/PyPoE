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

optimize __hash__ - very slow atm; or remove, but it is needed for the diffs

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

regex_translation_string = re.compile(
    r'^'
    r'[\s]*'
    r'(?P<minmax>(?:[0-9\-\|#]+[ \t]+)+)'
    r'"(?P<description>.*)"'
    r'(?P<quantifier>(?:[ \t]+[\w]+[ \t]+[0-9]+)*)'
    r'[ \t]*'
    r'$',
    re.UNICODE | re.MULTILINE
)

regex_ids = re.compile('([0-9])(?(1)(.*))', re.UNICODE)
regex_id_strings = re.compile('([\S]+)', re.UNICODE)
regex_strings = re.compile('(?:"(.+)")|([\S]+)+', re.UNICODE)
regex_int = re.compile('[0-9]+', re.UNICODE)
regex_isnumber = re.compile('^[0-9\-]+$', re.UNICODE)
regex_lang = re.compile(
    r'^[\s]*lang "(?P<language>[\w ]+)"[\s]*$',
    re.UNICODE | re.MULTILINE
)
regex_tokens = re.compile(
    r'(?:^"(?P<header>.*)"$)'
    r'|(?:^include "(?P<include>.*)"$)'
    r'|(?:^no_description (?P<no_description>[\w+%]*)$)'
    r'|(?P<description>^description)',
    re.UNICODE | re.MULTILINE
)

# =============================================================================
# Classes
# =============================================================================

class UnknownIdentifierWarning(UserWarning):
    pass

class DuplicateIdentifierWarning(UserWarning):
    pass

class Translation(object):

    __slots__ = ['languages', 'ids']

    def __init__(self):
        self.languages = []
        self.ids = []

    def __eq__(self, other):
        if not isinstance(other, Translation):
            return False

        if self.ids != other.ids:
            return False

        if self.languages != other.languages:
            return False

        return True

    def __hash__(self):
        return hash((tuple(self.languages), tuple(self.ids)))

    def diff(self, other):
        if not isinstance(other, Translation):
            raise TypeError()

        if self.ids != other.ids:
            _diff_list(self.ids, other.ids, diff=False)

        if self.languages != other.languages:
            _diff_list(self.languages, other.languages)

    def get_language(self, language):
        etr = None
        for tr in self.languages:
            if tr.language == language:
                return tr
            elif tr.language == 'English':
                etr = tr

        return etr

class TranslationLanguage(object):

    __slots__ = ['parent', 'language', 'strings']

    def __init__(self, language, parent):
        parent.languages.append(self)
        self.parent = parent
        self.language = language
        self.strings = []

    def __eq__(self, other):
        if not isinstance(other, TranslationLanguage):
            return False

        if self.language != other.language:
            return False

        if self.strings != other.strings:
            return False

        return True

    def __hash__(self):
        return hash((self.language, tuple(self.strings)))

    def diff(self, other):
        if not isinstance(other, TranslationLanguage):
            raise TypeError()

        if self.language != other.language:
            print('Self: %s, other: %s' % (self.language, other.language))

        if self.strings != other.strings:
            _diff_list(self.strings, other.strings)

    def get_string(self, values, indexes):
        valid_strings = []

        # Support for ranges
        is_range = []
        test_values = []
        short_values = []
        for item in values:
            # faster then isinstance(item, Iterable)
            if hasattr(item, '__iter__'):
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

    __slots__ = ['parent', 'quantifier', 'range', 'string']

    def __init__(self, parent):
        parent.strings.append(self)
        self.parent = parent
        self.quantifier = TranslationQuantifier()
        self.range = []
        self.string = ''

    def __eq__(self, other):
        if not isinstance(other, TranslationString):
            return False

        if self.quantifier != other.quantifier:
            return False

        if self.range != other.range:
            return False

        if self.string != other.string:
            return False

        return True

    def __hash__(self):
        return hash((self.string, tuple(self.range), self.quantifier))

    def __repr__(self):
        return 'TranslationString(string=%s, range=%s, quantifier=%s)' % (self.string, self.range, self.quantifier)

    def diff(self, other):
        if not isinstance(other, TranslationString):
            raise TypeError()

        if self.quantifier != other.quantifier:
            self.quantifier.diff(other.quantifier)

        if self.range != other.range:
            _diff_list(self.range, other.range)

        if self.string != other.string:
            print('String mismatch: %s vs %s' % (self.string, other.string))

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

    __slots__ = ['parent', 'min', 'max']

    def __init__(self, min, max, parent):
        parent.range.append(self)
        self.parent = parent
        self.min = min
        self.max = max

    def __repr__(self):
        return 'TranslationRange(min=%s, max=%s, parent=%s)' % (self.min, self.max, hex(id(self.parent)))

    def __eq__(self, other):
        if not isinstance(other, TranslationRange):
            return False

        if self.min != other.min:
            return False

        if self.max != other.max:
            return False

        return True

    def __hash__(self):
        return hash((self.min, self.max))

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

    __slots__ = ['registered_handlers']

    def __init__(self):
        self.registered_handlers = {}

    def __repr__(self):
        return 'TranslationQuantifier(registered_handlers=%s)' % (self.registered_handlers, )

    def __eq__(self, other):
        if not isinstance(other, TranslationQuantifier):
            return False

        if self.registered_handlers != other.registered_handlers:
            return False

        return True

    def __hash__(self):
        #return hash((tuple(self.registered_handlers.keys()), tuple(self.registered_handlers.values())))
        return hash(tuple(self.registered_handlers.keys()))

    def diff(self, other):
        if not isinstance(other, TranslationQuantifier):
            raise TypeError

        #if self.registered_handlers != other.registered_handlers:
        _diff_dict(self.registered_handlers, other.registered_handlers)




    def register(self, handler, index):
        if handler in self.registered_handlers:
            self.registered_handlers[handler].append(index)
        elif handler in self.handlers:
            self.registered_handlers[handler] = [index, ]
        else:
            warnings.warn('Warning, uncaptured! %s' % handler, UnknownIdentifierWarning)

    def handle(self, values, is_range):
        values = list(values)
        for handler_name in self.registered_handlers:
            f = self.handlers[handler_name]
            for index in self.registered_handlers[handler_name]:
                index -= 1
                if is_range[index]:
                    values[index] = (f(values[index][0]), f(values[index][1]))
                else:
                    values[index] = f(values[index])

        return values

class DescriptionFile(object):
    def __init__(self, file_path=None):
        self._translations = []
        self._translations_hash = {}

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
                            ts.quantifier.register(quant[i], int(quant[i+1]))
                            tmp.__next__()

                    offset = offset_next_lang


                for translation_id in translation.ids:
                    if translation_id in self._translations_hash:
                        other = self._translations_hash[translation_id]
                        # Identical, ignore
                        if other == translation:
                            continue
                        '''print('Diff for id: %s' % translation_id)
                        translation.diff(other)
                        print('')'''
                        warnings.warn('Duplicate id "%s", overriding.' % translation_id, DuplicateIdentifierWarning)
                    self._translations_hash[translation_id] = translation
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
        self._translations_hash.update(other._translations_hash)

    def get_translation(self, tags, values, lang='English', return_indexes=False):
        # A single translation might have multiple references
        # I.e. the case for always_freeze

        if isinstance(tags, str):
            tags = [tags, ]

        trans_found = []
        trans_found_indexes = []
        for tag in tags:
            if tag not in self._translations_hash:
                continue
            tr = self._translations_hash[tag]
            index = tr.ids.index(tag)
            if tr in trans_found:
                trans_found_indexes[trans_found.index(tr)].append(index)
            else:
                trans_found.append(tr)
                trans_found_indexes.append([index, ])

        trans_lines = []
        for i, tr in enumerate(trans_found):
            indexes = trans_found_indexes[i]

            tl = tr.get_language(lang)
            result = tl.get_string(values, indexes)
            if result:
                trans_lines += result

        if return_indexes:
            return trans_lines, trans_found_indexes
        return trans_lines


# =============================================================================
# Functions
# =============================================================================

def _diff_list(self, other, diff=True):
    len_self = len(self)
    len_other = len(other)
    if len_self != len_other:
        print('Different length, %s vs %s' % (len_self, len_other))

        set_self = set(self)
        set_other = set(other)
        print('Extra items in self: %s' % set_self.difference(set_other))
        print('Extra item in other: %s' % set_other.difference(set_self))
        return

    if diff:
        for i in range(0, len_self):
            self[i].diff(other[i])

def _diff_dict(self, other):
    key_self = set(tuple(self.keys()))
    key_other = set(tuple(other.keys()))

    kdiff_self = key_self.difference(key_other)
    kdiff_other = key_other.difference(key_self)

    if kdiff_self:
        print('Extra keys in self:')
        for key in kdiff_self:
            print('Key "%s": Value "%s"' % (key, self[key]))

    if kdiff_other:
        print('Extra keys in other:')
        for key in kdiff_other:
            print('Key "%s": Value "%s"' % (key, other[key]))

# =============================================================================
# Misc
# =============================================================================

if __name__ == '__main__':
    from line_profiler import LineProfiler

    profiler = LineProfiler()

    #profiler.add_function(DescriptionFile.get_translation)
    #profiler.add_function(DescriptionFile._read)
    #profiler.add_function(Translation.get_language)
    #profiler.add_function(TranslationQuantifier.handle)
    #profiler.add_function(TranslationRange.in_range)
    #profiler.add_function(TranslationLanguage.get_string)

    profiler.run("s = DescriptionFile('C:/Temp/MetaData/stat_descriptions.txt')")
    profiler.run("for i in range(0, 100): t = s.get_translation(tags=['additional_chance_to_take_critical_strike_%'], values=((3, 5)))")

    profiler.print_stats()

    print('Translation:', t)