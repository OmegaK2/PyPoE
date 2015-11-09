"""
Utilities for accessing GGG translations

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/translations.py                                   |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Utilities for parsing and using GGG translations.

The translation GGG provides are generally suffixed by _descriptions.txt and
can be found in the MetaData/ folder.
To read those, use the class DescriptionFile.

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE

TODO
-------------------------------------------------------------------------------

optimize __hash__ - very slow atm; or remove, but it is needed for the diffs
reverse for non-number values?
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import io
import re
import os
import warnings
from string import ascii_letters
from collections import Iterable

# self
from PyPoE import CUSTOM_TRANSLATION_FILE
from PyPoE.poe.file.shared import AbstractFileReadOnly, ParserError, ParserWarning

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'TranslationFile',
    'TranslationFileCache',
    'get_custom_translation_file',
    'set_custom_translation_file',
    'custom_translation_file',
]

regex_translation_string = re.compile(
    r'^'
    r'[\s]*'
    r'(?P<minmax>(?:[0-9\-\|#]+[ \t]+)+)'
    r'"(?P<description>.*)"'
    r'(?P<quantifier>(?:[ \t]+[\w]+[ \t]+[0-9]+)*)'
    r'[ \t]*[\r\n]*'
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
    r'|(?:^include "(?P<include>.*)")'
    r'|(?:^no_description (?P<no_description>[\w+%]*)$)'
    r'|(?P<description>^description)',
    re.UNICODE | re.MULTILINE
)

_custom_translation_file = None

# =============================================================================
# Warnings
# =============================================================================


class TranslationWarning(ParserWarning):
    pass


class MissingIdentifierWarning(TranslationWarning):
    pass


class UnknownIdentifierWarning(TranslationWarning):
    pass


class DuplicateIdentifierWarning(TranslationWarning):
    pass

# =============================================================================
# Classes
# =============================================================================

class Translation(object):
    """
    Representation of a single translation.

    A translation has at least one id and at least the English language (along
    with the respective strings).

    :ivar languages: List of TranslationLanguage instances for this Translation
    :type languages: list[TranslationLanguage]

    :ivar ids: List of ids associated with this Translation
    :type ids: list[str]
    """

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

    def __repr__(self):
        return 'Translation<%s>(ids=%s)' % (id(self), self.ids)

    def __hash__(self):
        return hash((tuple(self.languages), tuple(self.ids)))

    def diff(self, other):
        if not isinstance(other, Translation):
            raise TypeError()

        if self.ids != other.ids:
            _diff_list(self.ids, other.ids, diff=False)

        if self.languages != other.languages:
            _diff_list(self.languages, other.languages)

    def get_language(self, language='English'):
        """
        Returns the TranslationLanguage record for the specified language.

        As a fallback if the language is not found, the English
        TranslationLanguage record will be returned.

        :param language: The language to get.
        :type language: str

        :return: Returns the TranslationLanguage record for the specified
        language or the English one if not found
        :rtype: TranslationLanguage
        """
        etr = None
        for tr in self.languages:
            if tr.language == language:
                return tr
            elif tr.language == 'English':
                etr = tr

        return etr


class TranslationLanguage(object):
    """
    Representation of a language in the translation file. Each language has
    one or multiple strings.

    :ivar parent: The parent Translation instance
    :type parent: Translation

    :ivar language: the language of this instance
    :type language: str

    :ivar strings: List of Translation String instances
    :type strings: list[TranslationString]
    """

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

    def get_string(self, values, indexes, use_placeholder=False, only_values=False):
        """
        Formats the string according with the given values and indexes and
        returns the string and any left over (unused) values.

        If use_placeholder is specified, the values will be replaced with
        a placeholder instead of the actual value, however in order to determine
        the correct string within the range, values are still required.

        If only_values is specified, the instead of the string the formatted
        values will be returned.


        :param values: A list of values to be used for substitution
        :type values: list[int]

        :param indexes: A list of relevant indexes corresponding to the values
        for this string.
        :type indexes: list[int]

        :param use_placeholder: Whether to use placeholders instead of the
        actual values.
        :type use_placeholder: bool

        :param only_values: Whether to return formatted values instead of the
        formatted string.
        :type only_values: bool

        :return: Returns the formatted string
        :rtype: str, list[int] or list[int], list[int]
        """
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

        return ts.format_string(short_values, is_range, use_placeholder, only_values)

    def reverse_string(self, string):
        """
        Attempts to find a match for the given string and returns a list of
        reversed values if a match is found for this language.

        :param string: String to match against
        :type string: str
        :return: handled list of values or None if not found
        :rtype: None or list
        """
        # TODO: Should only match one at a time. But may be not?
        for ts in self.strings:
            result = ts.reverse_string(string)
            if result is not None:
                return result

        return None


class TranslationString(object):
    """
    Representation of a single translation string. Each string comes with
    it's own quantifiers and acceptable range.

    :ivar parent: parent language
    :type parent: TranslationLanguage

    :ivar quantifier: the quantifier for this translation string
    :type quantifier: TranslationQuantifier

    :ivar range: acceptable ranges for this translation as a list of instances
    for each index
    :type range: list[TranslationRange]

    :ivar string: the actual string to use for translation
    :type string: str

    :ivar string_re: a compiled regular expression string for reverse matching
    """

    __slots__ = ['parent', 'quantifier', 'range', 'string', 'string_re']

    # replacement tags used in translations
    tags = '%%%s%%', '%%%s$+d'

    def __init__(self, parent):
        parent.strings.append(self)
        self.parent = parent
        self.quantifier = TranslationQuantifier()
        self.range = []
        self.string = ''
        self.string_re = ''

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

    def _tag_iter(self, i):
        i += 1
        for tag in self.tags:
            tag = tag % i
            yield tag

    def _replace(self, i, s, rpl):
        new = s
        for tag in self._tag_iter(i):
            new = new.replace(tag, rpl)
        return new, s == new

    def _set_string(self, string):
        self.string = string.replace('%%', '%')

        # TODO: Maybe make optional?
        self.string_re = re.compile('^' + re.sub(
            r'\\\%[0-9]+\\\%(|\+d)',
            '([0-9\.]+)',
            re.escape(self.string)
        ) + '$')

    def diff(self, other):
        if not isinstance(other, TranslationString):
            raise TypeError()

        if self.quantifier != other.quantifier:
            self.quantifier.diff(other.quantifier)

        if self.range != other.range:
            _diff_list(self.range, other.range)

        if self.string != other.string:
            print('String mismatch: %s vs %s' % (self.string, other.string))

    def format_string(self, values, is_range, use_placeholder=False, only_values=False):
        """
        Formats the string for the given values.

        Optionally use_placeholder can be specified to return a string formatted
        with a placeholder in place of the real value. It will use lowercase
        ASCII starting at x. For indexes > 3, it will use uppercase ASCII.

        If only_values is specified, no string formatting will performed
        and instead just parsed values will be returned.

        :param values: List of values to use for the formatting
        :type values: list[int]
        :param is_range: List of bools representing whether the values at the
        list index is a range or not
        :type is_range: list[bool]
        :param use_placeholder: Use a placeholder instead of replacing the values
        :type use_placeholder: bool
        :param only_values: Only return the values and not
        :type only_values: bool
        :return: Returns the formatted string and a list of unused values.
        If only placeholder is specified, instead of the string a list of
        parsed values is returned.
        :rtype: str, list[int] or list[int], list[int]
        """
        s = self.string
        values = self.quantifier.handle(values, is_range)
        unused = []

        if only_values:
            rtr = []
            # Some translations don't use all values, so only return the ones
            # actually used
            for i, value in enumerate(values):
                for tag in self._tag_iter(i):
                    if tag in s:
                        rtr.append(value)
                    else:
                        unused.append(value)

            return rtr, unused

        if use_placeholder:
            for i, val in enumerate(values):
                # It will go to uppercase letters if above 3, but should be
                # no problem otherwise
                s, r = self._replace(i, s, ascii_letters[23+i])
                if r:
                    unused.append(val)
            return s, unused

        for i, val in enumerate(values):
            if is_range[i]:
                rpl = '(%s to %s)' % tuple(val)
            else:
                rpl = str(val)
            s, r = self._replace(i, s, rpl)
            if r:
                unused.append(val)
        return s, unused

    def match_range(self, values, indexes):
        """
        Returns the accumulative range rating of the specified values at
        the specified indexes

        :param values: List of values
        :type values: list[int] or list[float]
        :param indexes: List of indexes
        :type indexes: list[int]
        :return: Sum of the ratings
        :rtype: int
        """
        rating = 0
        for i in indexes:
            rating += self.range[i].in_range(values[i])
        return rating

    def reverse_string(self, string):
        """
        Attempts to match this TranslationString against the given string.

        If a match is found, it will attempt to cast and reverse all values
        found in the string itself.

        For missing values, it will try to insert the range maximum/minimum
        values if set, otherwise None.

        :param values: string to match against
        :type values: str
        :return: handled list of values or None if no match
        :rtype: list[int] or None
        """
        match = self.string_re.match(string)
        if match:
            values = list(match.groups())

            for i in range(0, len(self.parent.parent.ids)):
                found = False
                for tag in self._tag_iter(i):
                    found = self.string.find(tag) != -1
                    if found:
                        break

                if found:
                    values[i] = float(values[i])
                else:
                    r = self.range[i]
                    warn = None
                    # The only definitive case
                    if r.min == r.max and r.max is not None:
                        values.insert(i, r.max)
                    elif r.min is not None and r.max is not None:
                        values.insert(i, r.max)
                        warn = r.max
                    elif r.min is None and r.max is not None:
                        values.insert(i, r.max)
                        warn = r.max
                    elif r.min is not None and r.min is None:
                        values.insert(i, r.min)
                        warn = r.min
                    else:
                        values.insert(i, None)

                    if warn:
                        warnings.warn(
                            'Can not safely find a value at index "%s", using '
                            'range value "%s" instead' % (i, warn),
                            TranslationWarning
                        )

            return self.quantifier.handle_reverse(values)
        else:
            return None


class TranslationRange(object):
    """
    Object to represent the acceptable range of a translation.

    Many translation strings only apply to a given minimum or maximum number.
    In some cases there are also special strings for specific conditions.

    For example, 100 for freeze turns into "Always Freeze" whereas less is
    "chance to freeze".

    :ivar parent: parent
    :type parent: TranslationString

    :ivar min: minimum range
    :type min: int

    :ivar max: maximum range
    :type max: int
    """

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
        """
        Checks whether the value is in range and returns the rating/accuracy
        of the check performed.

        0 if no match
        1 if any range is accepted
        2 if either minimum or maximum is specified
        3 if both minimum and maximum is specified

        :param value: Value to check
        :type value: int
        :return: Returns the rating of the value
        :rtype: int
        """
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
    """
    Class to represent and handle translation quantifiers.

    In the GGG files often there are qualifiers specified to adjust the output
    of the values; for example, a value might be negated (i.e so that it would
    show "5% reduced Damage" instead of "-5% reduced Damage").
    """

    handlers = {
        'deciseconds_to_seconds': lambda v: v*10,
        'divide_by_one_hundred': lambda v: v/100,
        'per_minute_to_per_second': lambda v: v/60,
        'milliseconds_to_seconds': lambda v: v/1000,
        'negate': lambda v: v*-1,
        'divide_by_one_hundred_and_negate': lambda v: -v/100,
        'old_leech_percent': lambda v: v/5,
        'old_leech_permyriad': lambda v: v/50,
        # TODO dp = precision?
        'per_minute_to_per_second_0dp': lambda v: int(round(v/60, 0)),
        'per_minute_to_per_second_2dp': lambda v: round(v/60, 2),
        'milliseconds_to_seconds_0dp': lambda v: int(round(v/1000, 0)),
        'milliseconds_to_seconds_2dp': lambda v: round(v/1000, 2),
        # Only once TODO
        #'multiplicative_damage_modifier': lambda v: v,
        #'mod_value_to_item_class': lambda v: v,
    }

    reverse_handlers = {
        'deciseconds_to_seconds': lambda v: v/10,
        'divide_by_one_hundred': lambda v: v*100,
        'per_minute_to_per_second': lambda v: v*60,
        'milliseconds_to_seconds': lambda v: v*1000,
        'negate': lambda v: v*-1,
        'divide_by_one_hundred_and_negate': lambda v: -v*100,
        'old_leech_percent': lambda v: v*5,
        'old_leech_permyriad': lambda v: v*50,
        # TODO hardly possible to accurately reverse rounding
        'per_minute_to_per_second_0dp': lambda v: v*60,
        'per_minute_to_per_second_2dp': lambda v: v*60,
        'milliseconds_to_seconds_0dp': lambda v: v*1000,
        'milliseconds_to_seconds_2dp': lambda v: v*1000,
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
        """
        Registers that the specified handler should be used for the given
        index of the value.

        :param handler: id of the handler
        :type handler: str
        :param index: index of the handler value
        :type index: int
        """

        if handler in self.registered_handlers:
            self.registered_handlers[handler].append(index)
        elif handler in self.handlers:
            self.registered_handlers[handler] = [index, ]
        else:
            warnings.warn('Warning, uncaptured! %s' % handler, UnknownIdentifierWarning)

    def handle(self, values, is_range):
        """
        Handle the given values based on the registered quantifiers.

        :param values: list of values
        :type values: list[int]
        :param is_range: specifies whether the value at the index is a range or
        not. Must be the same length as values.
        :type is_range: Iterable of bools
        :return: handled list of values
        :rtype: list[int]
        """
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

    def handle_reverse(self, values):
        """
        Reverses the quantifier for the given values.

        :param values: list of values
        :type values: list[int]
        :return: handled list of values
        :rtype: list[int]
        """
        for handler_name in self.registered_handlers:
            f = self.handlers[handler_name]
            for index in self.registered_handlers[handler_name]:
                index -= 1
                values[index] = f(values[index])

        return values


class TranslationResult(object):
    """
    Translation result and utility functions.

    :ivar found:
    :type found: list[Translation]

    :ivar lines:
    :type lines: list[str]

    :ivar indexes:
    :type indexes: list[int]

    :ivar missing_ids:
    :type missing_ids: list[str]

    :ivar missing_values:
    :type missing_values: list[int]

    :ivar values:
    :type values: list[int]

    :ivar invalid:
    :type invalid: list[str]

    :ivar values:
    :type values_unused: list[int]

    :ivar source_ids:
    :type source_ids: list[str]

    :ivar source_values:
    :type source_values: list[int] or list[int, int]

    """
    __slots__ = [
        'found',
        'lines',
        'indexes',
        'missing_ids',
        'missing_values',
        'values',
        'invalid',
        'values_unused',
        'source_ids',
        'source_values',
    ]

    def __init__(self, found, lines, indexes, missing, missing_values, values,
                 invalid, unused, source_ids, source_values):
        self.found = found
        self.lines = lines
        self.indexes = indexes
        self.missing_ids = missing
        self.missing_values = missing_values
        self.values = values
        self.invalid = invalid
        self.values_unused = unused
        self.source_ids = source_ids
        self.source_values = source_values

    def _get_found_ids(self):
        ids = []
        for tr in self.found:
            ids += tr.ids

        return ids

    found_ids = property(fget=_get_found_ids)


class TranslationReverseResult(object):
    """
    Result of TranslationFile.reverse_translation

    :ivar translations: List of Translation instances
    :type translations: list[Translation]

    :ivar values: List of values
    :type values: list[list[float]]
    """
    __slots__ = [
        'translations',
        'values',
    ]

    def __init__(self, translations, values):
        self.translations = translations
        self.values = values


class TranslationFile(AbstractFileReadOnly):

    __slots__ = ['_translations', '_translations_hash', '_base_dir', '_parent']

    def __init__(self, file_path=None, base_dir=None, parent=None):
        """
        Creates a new TranslationFile instance from the given translation
        file(s).

        file_path can be specified to initialize the file(s) right away. It
        takes the same arguments as :method:`TranslationFile.read`.

        Some translation files have an "include" tag which includes the
        translation strings of another translation file automatically. By
        default that behaviour is ignored and a warning is raised.
        To enable the automatic include, specify either of the base_dir or
        parent variables.


        :param file_path: The file to read. Can also accept an iterable of
        files to read which will all be merged into one file. Also see
        :method:`TranslationFile.read`
        :type: Iterable or str or None
        :param base_dir: Base directory from where other translation files that
        contain the "include" tag will be included
        :type base_dir: str or None
        :param parent: parent TranslationFileCache that will be used for
        inclusion
        :type parent: TranslationFileCache or None

        :raises TypeError: if parent is not a :class:`TranslationFileCache`
        :raises ValueError: if both parent and base_dir are specified
        """
        self._translations = []
        self._translations_hash = {}
        self._base_dir = base_dir

        if parent is not None:
            if not isinstance(parent, TranslationFileCache):
                raise TypeError('Parent must be a TranslationFileCache.')
            if base_dir is not None:
                raise ValueError('Set either parent or base_dir, but not both.')

        self._parent = parent

        # Note str must be first since strings are iterable as well
        if isinstance(file_path, (str, bytes, io.BytesIO)):
            self.read(file_path)
        elif isinstance(file_path, Iterable):
            for path in file_path:
                self.merge(TranslationFile(path))

    def _read(self, buffer, *args, **kwargs):
        self._translations = []
        data = buffer.read().decode('utf-16')

        # starts with bom?
        offset = 0
        match = regex_tokens.search(data, offset)
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
                            raise ParserError(
                                'Malformed translation string near line %s: %s' % (
                                    data.count('\n', 0, offset),
                                    data[offset:offset_next_lang],
                                )
                            )

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

                        ts._set_string(ts_match.group('description'))

                        quant = ts_match.group('quantifier').strip().split()
                        tmp = iter(range(0, len(quant)))
                        for i in tmp:
                            ts.quantifier.register(quant[i], int(quant[i+1]))
                            tmp.__next__()

                    offset = offset_next_lang

                self._translations.append(translation)
                for translation_id in translation.ids:
                    self._add_translation_hashed(translation_id, translation)

            elif match.group('no_description'):
                pass
            elif match.group('include'):
                if self._parent:
                    self.merge(self._parent.get_file(match.group('include')))
                elif self._base_dir:
                    real_path = os.path.join(self._base_dir, match.group('include'))
                    self.merge(TranslationFile(real_path, base_dir=self._base_dir))
                else:
                    warnings.warn('Translation file includes other file, but no base_dir or parent specified. Skipping.')
            elif match.group('header'):
                pass

            # Done, search next
            match = match_next

    def __eq__(self, other):
        if not isinstance(other, TranslationFile):
            return False

        for attr in ('_translations', '_translations_hash'):
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def _add_translation_hashed(self, translation_id, translation):
        if translation_id in self._translations_hash:
            for old_translation in self._translations_hash[translation_id]:
                # Identical, ignore
                if translation == old_translation:
                    return

                # Identical ids, but more recent - update
                if translation.ids == old_translation.ids:
                    self._translations_hash[translation_id] = [translation, ]
                    # Attempt to remove the old one if it exists
                    try:
                        self._translations.remove(old_translation)
                    except ValueError as e:
                        pass

                    return

                '''print('Diff for id: %s' % translation_id)
                translation.diff(other)
                print('')'''

                warnings.warn('Duplicate id "%s"' % translation_id, DuplicateIdentifierWarning)
                self._translations_hash[translation_id].append(translation)
        else:
            self._translations_hash[translation_id] = [translation, ]

    def copy(self):
        """
        Creates a shallow copy of this TranslationFile.

        Note that the same objects will still be referenced.

        :return: copy of self
        :rtype: :class:`TranslationFile`
        """
        t = TranslationFile()
        for name in self.__slots__:
            setattr(t, name, getattr(self, name))

        return t

    def merge(self, other):
        """
        Merges the current translation file with another translation file.

        :param other: other :class:`TranslationFile` object to merge with
        :type: :class:`TranslationFile`
        :return: None
        """

        if not isinstance(other, TranslationFile):
            TypeError('Wrong type: %s' % type(other))
        self._translations += other._translations
        for trans_id in other._translations_hash:
            for trans in other._translations_hash[trans_id]:
                self._add_translation_hashed(trans_id, trans)

        #self._translations_hash.update(other._translations_hash)

    def get_translation(self, tags, values, lang='English', full_result=False, use_placeholder=False, only_values=False):
        """
        Attempts to retrieve a translation from the loaded translation file for
        the specified language with the given tags and values.

        Generally the list of values should be the size of the number of tags.

        If instead of the real value a placeholder (i.e. x, y, z) is desired
        use_placeholder should be set to True. However, the according values
        still need to be specified; this is done so that the appropriate
        translation can be selected - i.e. the translation changes depending
        on the values.


        :param tags: A list of identifiers for the tags
        :type tags: list[str]
        :param values: A list of integer values to use for the translations. It
        is also possible to use a list of size 2 for each elemented, which then
        will be treated as range of acceptable value and formatted accordingly
        (i.e. (x to y) instead of just x).
        :type values: list[int] or list[int, int]
        :param lang: Language to use. If it doesn't exist, English will be used
        as fallback.
        :type lang: str
        :param full_result: If true, a :class:`TranslationResult` object will
         be returned
        :type full_result: bool
        :param use_placeholder: If true, Instead of values in the translations
        a placeholder (i.e. x, y, z) will be used. Values are still required
        however to find the "correct" wording of the translation.
        :type use_placeholder: bool
        :param only_values: If true, only the handled values instead of the
        string are returned
        :type only_values: bool

        :return: Returns a list of found translation strings. The list may be
        empty if none are found. If full_result is specified, a
        :class:`TranslationResult` object is returned instead
        :rtype: list[str] or TranslationResult
        """
        # A single translation might have multiple references
        # I.e. the case for always_freeze

        if isinstance(tags, str):
            tags = [tags, ]

        trans_found = []
        trans_missing = []
        trans_missing_values = []
        trans_found_indexes = []
        trans_found_values = []
        for i, tag in enumerate(tags):
            if tag not in self._translations_hash:
                trans_missing.append(tag)
                trans_missing_values.append(values[i])
                continue

            #tr = self._translations_hash[tag][-1]
            for tr in self._translations_hash[tag]:
                index = tr.ids.index(tag)
                if tr in trans_found:
                    tf_index = trans_found.index(tr)
                    trans_found_indexes[tf_index].append(index)
                    trans_found_values[tf_index][index] = values[i]
                else:
                    trans_found.append(tr)
                    trans_found_indexes.append([index, ])
                    # Used to identify invalid translations later
                    v = [0xFFFFFFFF for i in range(0, len(tr.ids))]
                    v[index] = values[i]
                    trans_found_values.append(v)

        # Remove invalid translations
        invalid = []
        for i, found_values in enumerate(trans_found_values):
            for value in found_values:
                if value == 0xFFFFFFFF:
                    invalid.append(trans_found[i])
                    break

        for tr in invalid:
            index = trans_found.index(tr)
            del trans_found[index]
            del trans_found_indexes[index]
            del trans_found_values[index]

        trans_lines = []
        unused = []
        for i, tr in enumerate(trans_found):

            tl = tr.get_language(lang)
            result = tl.get_string(trans_found_values[i], trans_found_indexes[i], use_placeholder, only_values)
            if result:
                trans_lines.append(result[0])
                if full_result:
                    unused.append(result[1])

        if full_result:
            return TranslationResult(
                found=trans_found,
                lines=trans_lines,
                indexes=trans_found_indexes,
                missing=trans_missing,
                missing_values=trans_missing_values,
                values=trans_found_values,
                invalid=invalid,
                unused=unused,
                source_ids=tags,
                source_values=values,
            )
        return trans_lines

    def reverse_translation(self, string, lang='English'):
        translations_found = []
        values_found = []

        for tr in self._translations:
            tl = tr.get_language(lang)
            values = tl.reverse_string(string)
            if values is not None:
                translations_found.append(tr)
                values_found.append(values)

        return TranslationReverseResult(translations_found, values_found)


class TranslationFileCache(object):
    """
    Creates a memory cache of :class:`TranslationFile` objects.

    It will store any loaded file in the cache and return it as needed.
    The advantage is that there is only one object that will handle all
    translation files and only load them if they're not in the cache already.

    In particular this is useful as many translation files include other
    files which will only be read once and then passed to the other file
    accordingly - separately loading those files would read any included
    file multiple times, as such there is a fairly significant performance
    improvement over using single files.


    There is a caveat though, for this to work files need to referenced with
    their internal location (i.e. by the root folder).
    """
    def __init__(self, base_dir, merge_with_custom_file=None):
        """
        Creates a new TranslationFileCache instance.

        :param base_dir: The base directory where the files will be requested
        from (without "Metadata/")
        :type base_dir: str
        :param merge_with_custom_file: If this option is specified, each file
        will be merged with a custom translation file.
        If set to True, it will load the default translation file located in
        PyPoE's data directory.
        Alternatively a TranslationFile instance can be passed which then will
        be used.
        :type merge_with_custom_file: None, bool, TranslationFile

        :raises TypeError: if merge_with_custom_file is of invalid type
        """
        self._base_dir = base_dir
        self._desc_dir = os.path.join(base_dir, 'Metadata')

        if merge_with_custom_file is None or merge_with_custom_file is False:
            self._custom_file = None
        elif merge_with_custom_file is True:
            self._custom_file = get_custom_translation_file()
        elif isinstance(merge_with_custom_file, TranslationFile):
            self._custom_file = merge_with_custom_file
        else:
            raise TypeError(
                'Argument merge_with_custom_file is of wrong type. %(type)s' %
                {'type': type(merge_with_custom_file)}
            )

        self._files = {}

    def __getitem__(self, item):
        """
        Shortcut for :method:`TranslationFileCache.get_file` that will also
        added Metadata automatically.

        That means the following is equivalent:
        obj['stat_descriptions.txt']
        obj.get_file('Metadata/stat_descriptions.txt')

        :param str item: file name/path relative to the Metadata/ directory

        :return: the specified TranslationFile
        :rtype: TranslationFile
        """
        if not item.startswith('Metadata/'):
            item = 'Metadata/' + item
        return self.get_file(item)

    def get_file(self, name):
        """
        Returns the specified file from the cache (and loads it if not in the
        cache already).

        Note that the file name must be relative to the root path of exile
        folder (or a virtual) folder or it won't work properly.
        That means 'Metadata/stat_descriptions.txt' needs to be referenced
        as such.
        For a shortcut consider using obj[name] instead.


        :param str name: file name/path relative to the root path of exile dir

        :return: the specified TranslationFile
        :rtype: TranslationFile
        """
        if name not in self._files:
            self._files[name] = TranslationFile(
                file_path=os.path.join(self._base_dir, name),
                parent=self,
            )
            if self._custom_file:
                self._files[name].merge(self._custom_file)

        return self._files[name]

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


def get_custom_translation_file():
    """
    Returns the currently loaded custom translation file.

    Loads the default file if none is loaded.
    """
    global _custom_translation_file
    if _custom_translation_file is None:
        set_custom_translation_file()
    return _custom_translation_file


def set_custom_translation_file(file=None):
    """
    Sets the custom translation file.

    :param file: Path where the custom translation file is located. If None,
    the default file will be loaded
    :type file: str
    """
    global _custom_translation_file
    _custom_translation_file = TranslationFile(
        file_path=file or CUSTOM_TRANSLATION_FILE
    )

custom_translation_file = property(
    fget=get_custom_translation_file,
    fset=set_custom_translation_file,
)

# =============================================================================
# Init
# =============================================================================



if __name__ == '__main__':
    from line_profiler import LineProfiler

    profiler = LineProfiler()

    #profiler.add_function(TranslationFile.get_translation)
    #profiler.add_function(TranslationFile._read)
    #profiler.add_function(Translation.get_language)
    #profiler.add_function(TranslationQuantifier.handle)
    #profiler.add_function(TranslationRange.in_range)
    #profiler.add_function(TranslationLanguage.get_string)

    profiler.run("s = TranslationFile('C:/Temp/MetaData/stat_descriptions.txt')")
    profiler.run("for i in range(0, 100): t = s.get_translation(tags=['additional_chance_to_take_critical_strike_%', 'additional_chance_to_take_critical_strike_%'], values=((3, 5), 6))")

    profiler.print_stats()

    print('Translation:', t)