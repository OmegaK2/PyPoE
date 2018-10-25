"""
Utilities for accessing Path of Exile's translation file format.

Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/translations.py                                   |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Utilities for parsing and using GGG translations.

The translation GGG provides are generally suffixed by _descriptions.txt and
can be found in the MetaData/StatDescriptions/ folder.

Agreement
===============================================================================

See PyPoE/LICENSE

.. todo::

    optimize __hash__ very slow atm; or remove, but it is needed for the diffs
    reverse for non-number values?

    Fix empty translation strings

    passive_skill_stat_descriptions: tolerance vs missing stuff.

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

API for common and every day use.

Most of the time you'll just want to import the :class:`TranslationFile` or
:class:`TranslationFileCache` classes and work with the instantiated
:meth:`TranslationFile.get_translation` and
:meth:`TranslationFile.reverse_translation` methods.

The result formats :class:`TranslationResult` and
:class:`TranslationReverseResult` provide optional wrappers around the function
results that contain extra information and utility methods.


.. autoclass:: TranslationFile
    :inherited-members:

.. autoclass:: TranslationFileCache
    :inherited-members:
    :special-members: __getitem__

.. autoclass:: TranslationResult

.. autoclass:: TranslationReverseResult

.. autofunc:: get_custom_translation_file

.. autofunc:: set_custom_translation_file

.. autofunc:: install_data_dependant_quantifiers

Internal API
-------------------------------------------------------------------------------

API for internal use, but still may be useful to work with more directly.

.. autoclass:: Translation
    :special-members: __eq__

.. autoclass:: TranslationLanguage
    :special-members: __eq__

.. autoclass:: TranslationString
    :special-members: __eq__

.. autoclass:: TranslationRange
    :special-members: __eq__

.. autoclass:: TranslationQuantifierHandler
    :special-members: __eq__

Warning Classes
===============================================================================

.. autoclass:: TranslationWarning

.. autoclass:: MissingIdentifierWarning

.. autoclass:: UnknownIdentifierWarning

.. autoclass:: DuplicateIdentifierWarning

"""

# =============================================================================
# Imports
# =============================================================================

# Python
import io
import re
import os
import warnings
from enum import IntEnum
from string import ascii_letters
from collections import Iterable, OrderedDict, defaultdict

# self
from PyPoE import DATA_DIR
from PyPoE.shared.decorators import doc
from PyPoE.shared.mixins import ReprMixin
from PyPoE.poe.constants import MOD_GENERATION_TYPE
from PyPoE.poe.file.shared import AbstractFileReadOnly, ParserError, ParserWarning
from PyPoE.poe.file.shared.cache import AbstractFileCache

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'TranslationFile',
    'TranslationFileCache',
    'get_custom_translation_file',
    'set_custom_translation_file',
    'custom_translation_file',
    'install_data_dependant_quantifiers',
]

CUSTOM_TRANSLATION_FILE = os.path.join(DATA_DIR, 'custom_descriptions.txt')

regex_translation_string = re.compile(
    r'^'
    r'[\s]*'
    r'(?P<minmax>(?:[0-9\-\|#]+[ \t]+)+)'
    r'"(?P<description>.*)"'
    r'(?P<quantifier>(?:[ \t]*[\w%]+)*)'
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


class TranslationReprMixin(ReprMixin):

    _REPR_ARGUMENTS_TO_ATTRIBUTES = {
        'parent': '_parent_repr',
    }

    @property
    def _parent_repr(self):
        return '%s<%s>' % (self.parent.__class__.__name__, hex(id(self.parent)))


class Translation(TranslationReprMixin):
    """
    Representation of a single translation.

    A translation has at least one id and at least the English language (along
    with the respective strings).

    Attributes
    ----------
    languages : list[TranslationLanguage]
        List of :class:`TranslationLanguage` instances for this
        :class:`Translation`
    ids : list[str]
        List of ids associated with this translation
    """

    __slots__ = ['languages', 'ids']

    _REPR_EXTRA_ATTRIBUTES = OrderedDict((
        ('ids', None),
    ))

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

    def get_language(self, language='English'):
        """
        Returns the :class:`TranslationLanguage` record for the specified
        language.

        As a fallback if the language is not found, the English
        :class:`TranslationLanguage` record will be returned.

        Parameters
        ----------
        language : str
            The language to get.


        Returns
        -------
        TranslationLanguage
            Returns the :class:`TranslationLanguage record for the specified
            language or the English one if not found
        """
        etr = None
        for tr in self.languages:
            if tr.language == language:
                return tr
            elif tr.language == 'English':
                etr = tr

        return etr


class TranslationLanguage(TranslationReprMixin):
    """
    Representation of a language in the translation file. Each language has
    one or multiple strings.

    Attributes
    ----------
    parent : Translation
        The parent :class:`Translation` instance
    language : str
        the language of this instance
    strings : list[TranslationString]
        List of :class:`TranslationString` instances for this language
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

    def get_string(self, values, use_placeholder=False, only_values=False):
        """
        Formats the string according with the given values and
        returns the string and any left over (unused) values.

        If use_placeholder is specified, the values will be replaced with
        a placeholder instead of the actual value.

        If only_values is specified, the instead of the string the formatted
        values will be returned.


        Parameters
        ----------
        values : list[int]
            A list of values to be used for substitution
        use_placeholder : bool or callable
            If true, Instead of values in the translations a placeholder (i.e.
            x, y, z) will be used. Values are still required however to find
            the "correct" wording of the translation.
            If a callable is specified, it will call the function with
            the index as first parameter. The callable should return a
            string to use as placeholder.
        only_values : bool
            Whether to return formatted values instead of the formatted string.


        Returns
        -------
        str or list[int], list[int], list[int], dict[str, str]
            Returns the formatted string. See
            :meth:`TranslationString:format_string` for details.
        """
        # Support for ranges
        is_range = []
        test_values = []
        short_values = []
        for item in values:
            # faster then isinstance(item, Iterable)
            if hasattr(item, '__iter__'):
                # Use the greater value unless it is zero
                test_values.append(item[1] or item[0])
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

            match = ts.match_range(test_values)
            temp.append((match, ts))

        # Only the highest scoring/matching translation...
        temp.sort(key=lambda x: -x[0])
        rating, ts = temp[0]

        if rating == 0:
            return None

        return ts.format_string(short_values, is_range, use_placeholder, only_values)

    def reverse_string(self, string):
        """
        Attempts to find a match for the given string and returns a list of
        reversed values if a match is found for this language.

        Parameters
        ----------
        string : str
            String to match against


        Returns
        -------
        None or list
            handled list of values or None if not found
        """
        # TODO: Should only match one at a time. But may be not?
        for ts in self.strings:
            result = ts.reverse_string(string)
            if result is None:
                continue

            return result

        return None


class TranslationString(TranslationReprMixin):
    """
    Representation of a single translation string. Each string comes with
    it's own quantifiers and acceptable range.

    Attributes
    ----------
    parent : TranslationLanguage
        parent :class:`TranslationLanguage` instance
    quantifier : TranslationQuantifierHandler
        the associated :class:`TranslationQuantifierHandler` instance for this
        translation string
    range : list[TranslationRange]
        list of :class:`TranslationRange` instances containing the acceptable
        ranges for this translation as a list of instances for each index
    strings : list[str]
        translation string broken down into segments
    tags : list[int]
        tags for value replacement between segments
    tags_types : list[str]
        list of tag types
    """

    __slots__ = ['parent', 'quantifier', 'range', 'strings', 'tags',
                 'tags_types']
    
    _REPR_EXTRA_ATTRIBUTES = OrderedDict((
        ('string', None),
    ))

    # replacement tags used in translations
    _re_split = re.compile(
        r'(?:%(?P<id>[0-9]*)(?P<type>[\$]?[\+]?d[%]?|%))',
        re.UNICODE
    )

    _RANGE_FORMAT = '({0}-{1})'
    _NEGATIVE_RANGE_FORMAT = '-({0}-{1})'

    def __init__(self, parent):
        parent.strings.append(self)
        self.parent = parent
        self.quantifier = TranslationQuantifierHandler()
        self.range = []
        self.tags = []
        self.tags_types = []
        self.strings = []

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

    def _set_string(self, string):
        string = string.replace('%%', '%').replace('\\n', '\n')

        start = None
        for match in self._re_split.finditer(string):
            self.strings.append(string[start:match.start()])
            # Py indexes start at 0, not at 1
            self.tags.append(int(match.group('id') or 1)-1)
            # Can be none for %d% tag
            self.tags_types.append(match.group('type'))
            start = match.end()
        self.strings.append(string[start:])

    @property
    def string(self):
        """
        Reconstructed original string that would be used for translation

        Returns
        -------
        str
            the original string
        """
        s = []
        for i, tag in enumerate(self.tags):
            s.append(self.strings[i])
            s.append('%')
            s.append(str(tag+1))
            s.append(self.tags_types[i])
        s.append(self.strings[-1])
        return ''.join(s)

    @property
    def as_format_string(self):
        """
        The translation string as python str.format string

        Returns
        -------
        str
            str.format string
        """
        s = []
        for i, tag in enumerate(self.tags):
            s.append(self.strings[i])
            s.append('{%s}' % tag)
        s.append(self.strings[-1])
        return ''.join(s)

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

        Parameters
        ----------
        values : list[int]
            List of values to use for the formatting
        is_range : list[bool]
            List of bools representing whether the values at the list index is
            a range or not
        use_placeholder : bool or callable
            If true, Instead of values in the translations a placeholder (i.e.
            x, y, z) will be used. Values are still required however to find
            the "correct" wording of the translation.
            If a callable is specified, it will call the function with
            the index as first parameter. The callable should return a
            string to use as placeholder.
        only_values : bool
            Only return the values and not


        Returns
        -------
        str or list[int], list[int], list[int], dict[str, str]
            Returns 4 values.

            The first return value is the formatted string. If only placeholder
            is specified, instead of the string a list of parsed values is
            returned.

            The second return value is a list of unused values.

            The third return value is a list of used values.

            The forth return value is a dictionary of extra strings
        """
        values, extra_strings = self.quantifier.handle(values, is_range)

        string = []
        used = set()
        for i, tagid in enumerate(self.tags):
            value = values[tagid]
            if not only_values:
                string.append(self.strings[i])
                # For adding the plus sign to the $+d and $+d%% formats
                if '+' in self.tags_types[i] and (
                        is_range[tagid] and value[1] > 0 or not is_range[tagid]
                        and value > 0):
                    string.append('+')

                if not use_placeholder:
                    if 'd' in self.tags_types[i]:
                        fmt = '{0:n}'
                    else:
                        fmt = '{0}'

                    if is_range[tagid]:
                        # Move the minus outside if both values are negative
                        try:
                            if value[0] < 0 and value[1] < 0:
                                value = [-v for v in value]
                                range_fmt = self._NEGATIVE_RANGE_FORMAT
                            else:
                                range_fmt = self._RANGE_FORMAT
                        #TODO: how to show ranges for text stuff?
                        except TypeError:
                            range_fmt = self._RANGE_FORMAT
                        value = range_fmt.format(
                            fmt, fmt.replace('{0', '{1')
                        ).format(*value)
                    else:
                        value = fmt.format(value)
                elif use_placeholder is True:
                    value = ascii_letters[23+i]
                elif callable(use_placeholder):
                    value = use_placeholder(i)
            string.append(value)
            used.add(tagid)

            if self.tags_types[i].endswith('d%'):
                string.append('%')

        unused = []
        for i, val in enumerate(values):
            if i in used:
                continue
            unused.append(val)

        if only_values:
            string = values
        else:
            string = ''.join(string + [self.strings[-1]])

        return string, unused, values, extra_strings

    def match_range(self, values):
        """
        Returns the accumulative range rating of the specified values.

        Parameters
        ----------
        values : list[int] or list[float]
            List of values

        Returns
        -------
        int
            Sum of the ratings
        """
        rating = 0
        for i, value in enumerate(values):
            rating += self.range[i].in_range(value)
        return rating

    def reverse_string(self, string):
        """
        Attempts to match this :class:`TranslationString` against the given
        string.

        If a match is found, it will attempt to cast and reverse all values
        found in the string itself.

        For missing values, it will try to insert the range maximum/minimum
        values if set, otherwise None.

        Parameters
        ----------
        string : str
            string to match against


        Returns
        -------
        list[int] or None
            handled list of values or None if no match
        """
        index = 0
        values_indexes = []
        for partial in self.strings:
            match = string.find(partial, index)
            if match == -1:
                return None
            # Matched at the start of string, no preceeding value

            index = match + len(partial)
            values_indexes.append(index)

        # Fix for TR strings starting with value
        if self.strings[0] == '':
            values_indexes.append(None)
        # Fix for TR strings ending with value
        if self.strings[-1] == '':
            values_indexes[-1] = None

        values = []
        for i in range(0, len(values_indexes)-1):
            j = i + 1
            values.append(string[values_indexes[i]:values_indexes[j]])

        # tags may appear multiple times, reduce to one tag per value
        tags = {}
        for i, tag in enumerate(self.tags):
            tags[tag] = values[i]

        values = list(range(0, len(self.range)))
        for i in values:
            if i in tags:
                # Fix for %1$+d
                values[i] = tags[i].strip('%')
            else:
                # The only definitive case
                r = self.range[i]
                warn = True
                if r.min == r.max and r.max is not None:
                    val = r.min
                    warn = False
                elif r.min is not None and r.max is not None:
                    val = r.max
                elif r.min is None and r.max is not None:
                    val = r.max
                elif r.min is not None and r.min is None:
                    val = r.min
                else:
                    val = 0

                if warn:
                    warnings.warn(
                        'Can not safely find a value at index "%s", using '
                        'range value "%s" instead' % (i, val),
                        TranslationWarning
                    )

                values[i] = val

        return self.quantifier.handle_reverse(values)


class TranslationRange(TranslationReprMixin):
    """
    Object to represent the acceptable range of a translation.

    Many translation strings only apply to a given minimum or maximum number.
    In some cases there are also special strings for specific conditions.

    For example, 100 for freeze turns into "Always Freeze" whereas less is
    "chance to freeze".

    Attributes
    ----------
    parent : TranslationString
        parent :class:`TranslationString` instance
    min : int
        minimum range
    max : int
        maximum range
    """

    __slots__ = ['parent', 'min', 'max']

    def __init__(self, min, max, parent):
        parent.range.append(self)
        self.parent = parent
        self.min = min
        self.max = max

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

        Parameters
        ----------
        value : int
            Value to check


        Returns
        -------
        int
            Returns the rating of the value
            -100 if mismatch (out of range)
            0 if no match
            1 if any range is accepted
            2 if either minimum or maximum is specified
            3 if both minimum and maximum is specified
        """
        # Any range is accepted
        if self.min is None and self.max is None:
            return 1

        if self.min is None:
            if value <= self.max:
                return 2
            else:
                return -100

        if self.max is None:
            if value >= self.min:
                return 2
            else:
                return -100

        if self.min is not None and self.max is not None:
            if self.min <= value <= self.max:
                return 3
            else:
                return -100

        return 0


class TranslationQuantifierHandler(TranslationReprMixin):
    """
    Class to represent and handle translation quantifiers.

    In the GGG files often there are qualifiers specified to adjust the output
    of the values; for example, a value might be negated (i.e so that it would
    show "5% reduced Damage" instead of "-5% reduced Damage").
    
    Attributes
    ----------
    index_handlers : dict[str, list[int]]
        Mapping of the name of registered handlers to the ids they apply to

    handlers : dict[str, TranslationQuantifier]
        Class variable. Installed handlers

    reverse_handlers : dict[str, TranslationQuantifier]
        Class variable. Installed reverse handlers.
    """

    _REPR_EXTRA_ATTRIBUTES = OrderedDict((
        ('index_handlers', None),
        ('string_handlers', None),
    ))

    handlers = {
    }

    reverse_handlers = {
    }

    regex = None

    __slots__ = ['index_handlers', 'string_handlers']

    def __init__(self):
        self.index_handlers = defaultdict(list)
        self.string_handlers = defaultdict(list)

    def __eq__(self, other):
        if not isinstance(other, TranslationQuantifierHandler):
            return False

        if self.index_handlers != other.index_handlers:
            return False

        return True

    def __hash__(self):
        #return hash((tuple(self.registered_handlers.keys()), tuple(self.registered_handlers.values())))
        return hash(tuple(self.index_handlers.keys()))

    def _warn_uncaptured(self, name):
        warnings.warn(
            'Warning uncaptured quantifier %s' % name, UnknownIdentifierWarning
        )

    def _whole_float_to_int(self, value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value


    @classmethod
    def install_quantifier(cls, quantifier):
        """
        Install the specified quantifier into the generic quantifier handling

        Parameters
        ----------
        quantifier - TranslationQuantifier
            :class:`TranslationQuantifier` instance

        Returns
        -------
        """

        cls.handlers[quantifier.id] = quantifier
        cls.reverse_handlers[quantifier.id] = quantifier

    @classmethod
    def init(cls):
        cls.regex = re.compile(
            r'(%s)(?!\_)' % '|'.join(cls.handlers.keys()),
            re.UNICODE
        )

    def diff(self, other):
        if not isinstance(other, TranslationQuantifierHandler):
            raise TypeError

        #if self.registered_handlers != other.registered_handlers:
        _diff_dict(self.index_handlers, other.index_handlers)

    def _get_handler_func(self, handler_name):
        try:
            f = self.handlers[handler_name].handler
        except KeyError:
            self._warn_uncaptured(handler_name)
            return None
        if f is None:
            self._warn_uncaptured(handler_name)
            return None
        return f

    def register_from_string(self, string):
        """
        Registers handlers from the quantifier string.

        Parameters
        ----------
        string : str
            quantifier string
        offset : int
            offset this operation is appearing at (to show errors)
        """
        values = iter(self.regex.split(string))

        for partial in values:
            partial = partial.strip()
            if partial == '':
                continue
            handler = self.handlers.get(partial)
            if handler:
                args = [values.__next__() for i in range(0, handler.arg_size)]
                if handler.type == TranslationQuantifier.QuantifierTypes.INT:
                    try:
                        self.index_handlers[handler.id].append(int(args[0]))
                    except ValueError as e:
                        warnings.warn('Broken quantifier "%s" - Error: %s' % (string, e.args[0]), TranslationWarning)
                elif handler.type == TranslationQuantifier.QuantifierTypes.STRING:
                    self.string_handlers[handler.id] = args
            else:
                warnings.warn('Uncaptured partial quantifier string "%s"' % (partial, ), UnknownIdentifierWarning)

    def handle(self, values, is_range):
        """
        Handle the given values based on the registered quantifiers.

        Parameters
        ----------
        values : list[int]
            list of values
        is_range : Iterable of bools
            specifies whether the value at the index is a range or not. Must be
            the same length as values.

        Returns
        -------
        list[int]
            handled list of values
        """
        values = list(values)
        for handler_name in self.index_handlers:
            f = self._get_handler_func(handler_name)
            if f is None:
                continue
            for index in self.index_handlers[handler_name]:
                index -= 1
                if is_range[index]:
                    values[index] = (f(values[index][0]), f(values[index][1]))
                else:
                    values[index] = f(values[index])

        for i, value in enumerate(values):
            if is_range[i]:
                 values[i] = tuple([self._whole_float_to_int(v) for v in value])
            else:
                 values[i] = self._whole_float_to_int(value)

        strings = OrderedDict()
        for handler_name, args in self.string_handlers.items():
            f = self._get_handler_func(handler_name)
            if f is None:
                continue
            strings[handler_name] = f(*args)

        return values, strings

    def handle_reverse(self, values):
        """
        Reverses the quantifier for the given values.

        Parameters
        ----------
        values : list[int]
            list of values

        Returns
        -------
        list[int]
            handled list of values
        """
        indexes = set(range(0, len(values)))
        for handler_name in self.index_handlers:
            try:
                f = self.reverse_handlers[handler_name].reverse_handler
            except KeyError:
                self._warn_uncaptured(handler_name)
                break
            for index in self.index_handlers[handler_name]:
                index -= 1
                indexes.remove(index)
                # TODO: handle string values
                values[index] = f(values[index])

        for index in indexes:
            values[index] = int(values[index])

        return values


class TranslationQuantifier(TranslationReprMixin):
    """
    Attributes
    ----------
    id : str
        string identifier of the handler
    arg_size : int
        number of arguments this handler accepts (excluding self)
    type : QuantifierTypes
        type of the quantifier
    handler : function
        function that handles the values, if any
    reverse_handler : function
        function  hat reverses handles the values, if any
    """

    class QuantifierTypes(IntEnum):
        INT = 1
        STRING = 2

    __slots__ = [
        'id', 'arg_size', 'type', 'handler', 'reverse_handler',
    ]

    def __init__(self, id, arg_size=1, type=QuantifierTypes.INT, handler=None,
                 reverse_handler=None):
        self.id = id
        self.arg_size = arg_size
        if not isinstance(type, self.QuantifierTypes):
            raise ValueError('Type must be a QuantifierTypes instance')
        self.type = type
        self.handler = handler
        self.reverse_handler = reverse_handler
        TranslationQuantifierHandler.install_quantifier(self)


class TQReminderString(TranslationQuantifier):
    def __init__(self, relational_reader, *args, **kwargs):
        self.relational_reader = relational_reader
        super(TQReminderString, self).__init__(
            id='reminderstring',
            type=self.QuantifierTypes.STRING,
            handler=self.handle,
            reverse_handler=None,
        )

    def handle(self, *args):
        return self.relational_reader['ClientStrings.dat'].index['Id'][args[0].strip()]['Text']


class TranslationResult(TranslationReprMixin):
    """
    Translation result of :meth:`TranslationFile:get_translation`.

    Attributes
    ----------
    found : list[Translation]
        List of found :class:`Translation` instances (in order)
    found_lines : list[str]:
        List of related translated strings (in order)L
    lines : list[str]
        List of translated strings (minus missing ones)
    missing_ids : list[str]
        List of missing identifier tags
    missing_values : list[int]
        List of missing identifier values
    partial: list[Translation]
        List of partial matches of translation tags (in order)
    values : list[int]
        List of values (in order)
    values_unused : list[int]
        List of unused values
    values_parsed : list[str]
        List of parsed values (i.e. with quantifier applied)
    source_ids : list[str]
        List of the original tags passed before the translation occurred
    source_values : list[int] or list[int, int]
        List of the original values passed before the translation occurred
    extra_strings : list[dict[str, str]]
        List of dictionary containing extra strings returned.
        The key is the quantifier id used and the value is the string returned.
    """
    __slots__ = [
        'found',
        'found_lines',
        'lines',
        'missing_ids',
        'missing_values',
        'partial',
        'values',
        'values_unused',
        'values_parsed',
        'source_ids',
        'source_values',
        'extra_strings',
    ]

    def __init__(self, found, found_lines, lines, missing,
                 missing_values, partial, values, unused, values_parsed,
                 source_ids, source_values, extra_strings):
        self.found = found
        self.found_lines = found_lines
        self.lines = lines
        self.missing_ids = missing
        self.missing_values = missing_values
        self.partial = partial
        self.values = values
        self.values_unused = unused
        self.values_parsed = values_parsed
        self.source_ids = source_ids
        self.source_values = source_values
        self.extra_strings = extra_strings

    def _get_found_ids(self):
        """
        Generates a list of found ids and returns it.

        Returns
        -------
        list[list[str]]
            List of found ids
        """
        return [tr.ids for tr in self.found]

    found_ids = property(fget=_get_found_ids)

    @property
    def missing(self):
        """
        Zips :attr:`missing_ids` and :attr:`missing_values`.

        Returns
        -------
        zip
        """
        return zip(self.missing_ids, self.missing_values)


class TranslationReverseResult(TranslationReprMixin):
    """
    Result of :meth:`TranslationFile.reverse_translation`

    Attributes
    ----------
    translations : list[Translation]
        List of :class:`Translation` instances
    values : list[list[float]]
        List of values
    """
    __slots__ = [
        'translations',
        'values',
    ]

    def __init__(self, translations, values):
        self.translations = translations
        self.values = values


class TranslationFile(AbstractFileReadOnly):
    """
    Translation file reader.

    Translation files can be found in the following folder in the content.ggpk:

    Metadata/StatDescriptions/xxx_descriptions.txt

    Attributes
    ----------
    translations : list[Translation]
        List of parsed :class:`Translation` instances (in order)
    translations_hash   : dict[str, list[Translation]]
        Mapping of parsed :class:`Translation` instances with their id(s) as
        key.

        Each value is a list of :class:`Translation` instances, even if there
        is only one.
    """

    __slots__ = ['translations', 'translations_hash', '_base_dir', '_parent']

    def __init__(self, file_path=None, base_dir=None, parent=None):
        """
        Creates a new TranslationFile instance from the given translation
        file(s).

        file_path can be specified to initialize the file(s) right away. It
        takes the same arguments as :meth:`TranslationFile.read`.

        Some translation files have an "include" tag which includes the
        translation strings of another translation file automatically. By
        default that behaviour is ignored and a warning is raised.
        To enable the automatic include, specify either of the base_dir or
        parent variables.

        .. note::
            the inclusion paths for other translation files are relative to
            root of the content.ggpk and if using a file system it is expected
            to mirror this behaviour

        Parameters
        ----------
        file_path : Iterable or str or None
            The file to read. Can also accept an iterable of files to read
            which will all be merged into one file. Also see
            :meth:`read`
        base_dir : str or None
            Base directory from where other translation files that contain the
            "include" tag will be included
        parent : :class:`TranslationFileCache` or None
            parent :class:`TranslationFileCache` that will be used for inclusion

        Raises
        ------
        ValueError
            if both parent and base_dir are specified
        TypeError
            if parent is not a :class:`TranslationFileCache`
        """
        self.translations = []
        self.translations_hash = {}
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
        self.translations = []
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
                                'Malformed translation string near line %s @ ids %s: %s' % (
                                    data.count('\n', 0, offset),
                                    ids,
                                    data[offset:offset_next_lang+1],
                                )
                            )

                        offset = ts_match.end()

                        ts = TranslationString(parent=tl)

                        # Min/Max limiter
                        limiter = ts_match.group('minmax').strip().split()
                        for j in range(0, id_count):
                            matchstr = limiter[j]
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

                        ts.quantifier.register_from_string(
                            ts_match.group('quantifier'),
                        )

                    offset = offset_next_lang

                self.translations.append(translation)
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
                    warnings.warn(
                        'Translation file includes other file, but no base_dir '
                        'or parent specified. Skipping.', TranslationWarning)
            elif match.group('header'):
                pass

            # Done, search next
            match = match_next

    def __eq__(self, other):
        if not isinstance(other, TranslationFile):
            return False

        for attr in ('translations', 'translations_hash'):
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def _add_translation_hashed(self, translation_id, translation):
        if translation_id in self.translations_hash:
            for old_translation in self.translations_hash[translation_id]:
                # Identical, ignore
                if translation == old_translation:
                    return

                # Identical ids, but more recent - update
                if translation.ids == old_translation.ids:
                    self.translations_hash[translation_id] = [translation, ]
                    # Attempt to remove the old one if it exists
                    try:
                        self.translations.remove(old_translation)
                    except ValueError as e:
                        pass

                    return

                '''print('Diff for id: %s' % translation_id)
                translation.diff(other)
                print('')'''

                warnings.warn('Duplicate id "%s"' % translation_id, DuplicateIdentifierWarning)
                self.translations_hash[translation_id].append(translation)
        else:
            self.translations_hash[translation_id] = [translation, ]

    def copy(self):
        """
        Creates a shallow copy of this TranslationFile.

        Note that the same objects will still be referenced.

        Returns
        -------
        :class:`TranslationFile`
            copy of self
        """
        t = TranslationFile()
        for name in self.__slots__:
            setattr(t, name, getattr(self, name))

        return t

    def merge(self, other):
        """
        Merges the current translation file with another translation file.

        Parameters
        ----------
        other : :class:`TranslationFile`
            other :class:`TranslationFile` object to merge with


        Returns
        -------
        None
        """

        if not isinstance(other, TranslationFile):
            TypeError('Wrong type: %s' % type(other))
        self.translations += other.translations
        for trans_id in other.translations_hash:
            for trans in other.translations_hash[trans_id]:
                self._add_translation_hashed(trans_id, trans)

        #self.translations_hash.update(other.translations_hash)

    def get_translation(self, tags, values, lang='English', full_result=False, use_placeholder=False, only_values=False):
        """
        Attempts to retrieve a translation from the loaded translation file for
        the specified language with the given tags and values.

        Generally the list of values should be the size of the number of tags.

        If instead of the real value a placeholder is desired use_placeholder
        can be used.

        Parameters
        ----------
        tags : list[str]
            A list of identifiers for the tags
        values : list[int] or list[int, int]
            A list of integer values to use for the translations. It is also
            possible to use a list of size 2 for each element, which then
            will be treated as range of acceptable value and formatted
            accordingly (i.e. (x to y) instead of just x).
        lang : str
            Language to use. If it doesn't exist, English will be used as
            fallback.
        full_result : bool
            If true, a :class:`TranslationResult` object will  be returned
        use_placeholder : bool or callable
            If true, Instead of values in the translations a placeholder (i.e.
            x, y, z) will be used. Values are still required however to find
            the "correct" wording of the translation.
            If a callable is specified, it will call the function with
            the index as first parameter. The callable should return a
            string to use as placeholder.
        only_values : bool
            If true, only the handled values instead of the string are returned


        Returns
        -------
        list[str] or TranslationResult
            Returns a list of found translation strings. The list may be empty
            if none are found. If full_result is specified, a
            :class:`TranslationResult` object is returned instead
        """
        # A single translation might have multiple references
        # I.e. the case for always_freeze

        if isinstance(tags, str):
            tags = [tags, ]

        trans_found = []
        trans_missing = []
        trans_missing_values = []
        trans_found_values = []
        for i, tag in enumerate(tags):
            # stats that are zero are not displayed
            try:
                if values[i][0] == 0 and values[i][1] == 0:
                    continue
            except TypeError:
                if values[i] == 0:
                    continue

            if tag not in self.translations_hash:
                trans_missing.append(tag)
                trans_missing_values.append(values[i])
                continue

            #tr = self.translations_hash[tag][-1]
            for tr in self.translations_hash[tag]:
                index = tr.ids.index(tag)
                if tr in trans_found:
                    tf_index = trans_found.index(tr)
                    trans_found_values[tf_index][index] = values[i]
                else:
                    trans_found.append(tr)
                    # Used to identify invalid translations later
                    v = [0xFFFFFFFF for i in range(0, len(tr.ids))]
                    v[index] = values[i]
                    trans_found_values.append(v)

        # It seems that partial matches for the tags are indeed allowed and not
        # invalid.
        # Cases are base_chance_to_freeze_% and always_freeze for example
        partial = []
        for i, found_values in enumerate(trans_found_values):
            for j, value in enumerate(found_values):
                if value == 0xFFFFFFFF:
                    # Assume 0 as default.
                    found_values[j] = 0
                    partial.append(trans_found[i])

        if partial:
            warnings.warn(
                'Partial tag match for %s' % ', '.join([
                   str(p) for p in partial
                ]),
                TranslationWarning
            )

        trans_lines = []
        trans_found_lines = []
        unused = []
        values_parsed = []
        extra_strings = []
        for i, tr in enumerate(trans_found):

            tl = tr.get_language(lang)
            result = tl.get_string(trans_found_values[i], use_placeholder, only_values)
            if result:
                trans_lines.append(result[0])
                trans_found_lines.append(result[0])
                values_parsed.append(result[2])
                if full_result:
                    unused.append(result[1])
                    extra_strings.append(result[3])

            else:
                trans_found_lines.append('')
                values_parsed.append([])

        if full_result:
            return TranslationResult(
                found=trans_found,
                found_lines=trans_found_lines,
                lines=trans_lines,
                missing=trans_missing,
                missing_values=trans_missing_values,
                values=trans_found_values,
                values_parsed=values_parsed,
                partial=partial,
                unused=unused,
                source_ids=tags,
                source_values=values,
                extra_strings=extra_strings,
            )
        if only_values:
            return values_parsed
        else:
            return trans_lines

    def reverse_translation(self, string, lang='English'):
        """
        Attempt to reverse a translation string and return probable candidates
        as well as probable values the translation string was used with.

        .. warning::
            During translation there is a loss of information incurred and
            there are cases where it might be impossible reconstruct the string.

        .. warning::
            The method can only work of **exact** translation strings, so
            minor differences already might result in failure detection. As
            such strings from previous versions of Path of Exile may not work.

        Parameters
        ----------
        string : str
            The translation string to reverse
        lang
            The language the string is in

        Returns
        -------
        TranslationReverseResult
            :class:`TranslationReverseResult` instance containing any found
            translation instances as well as the values.
        """
        translations_found = []
        values_found = []

        for tr in self.translations:
            tl = tr.get_language(lang)
            values = tl.reverse_string(string)
            if values is not None:
                translations_found.append(tr)
                values_found.append(values)

        return TranslationReverseResult(translations_found, values_found)


@doc(append=AbstractFileCache)
class TranslationFileCache(AbstractFileCache):
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
    """
    FILE_TYPE = TranslationFile

    @doc(prepend=AbstractFileCache.__init__)
    def __init__(self, *args, merge_with_custom_file=None, **kwargs):
        """
        Parameters
        ----------
        merge_with_custom_file : None, bool or TranslationFile
            If this option is specified, each file will be merged with a custom
            translation file. If set to True, it will load the default
            translation file located in PyPoE's data directory. Alternatively a
            TranslationFile instance can be passed which then will be used.
        """
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

        # Call order matters here
        super(TranslationFileCache, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        """
        Shortcut for :meth:`TranslationFileCache.get_file` that will also
        added Metadata automatically.

        That means the following is equivalent:
        obj['stat_descriptions.txt']
        obj.get_file('Metadata/StatDescriptions/stat_descriptions.txt')

        Parameters
        ----------
        item :  str
            file name/path relative to the Metadata/StatDescriptions/ directory


        Returns
        -------
        TranslationFile
            the specified TranslationFile
        """
        if not item.startswith('Metadata/StatDescriptions/'):
            item = 'Metadata/StatDescriptions/' + item
        return self.get_file(item)

    @doc(doc=AbstractFileCache._get_file_instance_args)
    def _get_file_instance_args(self, file_name, *args, **kwargs):
        return {
            'parent': self,
        }

    def get_file(self, file_name):
        """
        Returns the specified file from the cache (and loads it if not in the
        cache already).

        Note that the file name must be relative to the root path of exile
        folder (or a virtual) folder or it won't work properly.
        That means 'Metadata/stat_descriptions.txt' needs to be referenced
        as such.
        For a shortcut consider using obj[name] instead.


        Parameters
        ----------
        file_name :  str
            file name/path relative to the root path of exile directory


        Returns
        -------
        TranslationFile
            the specified TranslationFile
        """
        if file_name not in self.files:
            tf = self._create_instance(file_name=file_name)

            if self._custom_file:
                tf.merge(self._custom_file)

            self.files[file_name] = tf

            return tf

        return self.files[file_name]


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

    Returns
    -------
    TranslationFile
        the currently loaded custom translation file
    """
    global _custom_translation_file
    if _custom_translation_file is None:
        set_custom_translation_file()
    return _custom_translation_file


def set_custom_translation_file(file=None):
    """
    Sets the custom translation file.

    Parameters
    ----------
    file : str
        Path where the custom translation file is located. If None,
        the default file will be loaded
    """
    global _custom_translation_file
    _custom_translation_file = TranslationFile(
        file_path=file or CUSTOM_TRANSLATION_FILE
    )

custom_translation_file = property(
    fget=get_custom_translation_file,
    fset=set_custom_translation_file,
)


def install_data_dependant_quantifiers(relational_reader):
    """
    Install data dependant quantifiers into this class.

    Parameters
    ----------
    relational_reader : RelationalReader
        :class:`RelationalReader` instance to read the required game data
        files from.
    """
    def _mod_value_to_item_class_reverse( value):
        for row in relational_reader['ItemClasses.dat']:
            if row['Name'] == value:
                return row.rowid
        return None

    TranslationQuantifier(
        id='mod_value_to_item_class',
        handler=lambda v: relational_reader['ItemClasses.dat'][v]['Name'],
        reverse_handler=_mod_value_to_item_class_reverse,
    )

    def _tempest_mod_text_reverse(value):
        results = []
        for row in relational_reader['Mods.dat']:
            if row['GenerationType'] != MOD_GENERATION_TYPE.TEMPEST:
                continue
            if row['Name'] == value:
                results.append(row.rowid)

        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            return None
        else:
            return results

    TranslationQuantifier(
        id='tempest_mod_text',
        handler=lambda v: relational_reader['Mods.dat'][v]['Name'],
        reverse_handler=_tempest_mod_text_reverse,
    )

    TQReminderString(relational_reader=relational_reader)

    TranslationQuantifierHandler.init()

# =============================================================================
# Init
# =============================================================================

#
# Translation Quantifiers
#

# Notes:
# * It's hardly possible to reverse rounding accurately

"""
TranslationQuantifier(
    id='',
    handler=lambda v: ,
    reverse_handler=lambda v: ,
)
"""

TranslationQuantifier(
    id='30%_of_value',
    handler=lambda v: v*0.3,
    reverse_handler=lambda v: v/0.3,
)

TranslationQuantifier(
    id='60%_of_value',
    handler=lambda v: v*0.6,
    reverse_handler=lambda v: v/0.6,
)

TranslationQuantifier(
    id='deciseconds_to_seconds',
    handler=lambda v: v/10,
    reverse_handler=lambda v: float(v)*10,
)

TranslationQuantifier(
    id='divide_by_one_hundred',
    handler=lambda v: v/100,
    reverse_handler=lambda v: float(v)*100,
)

TranslationQuantifier(
    id='divide_by_one_hundred_and_negate',
    handler=lambda v: -v/100,
    reverse_handler=lambda v: -float(v)*100,
)

TranslationQuantifier(
    id='divide_by_one_hundred_2dp',
    handler=lambda v: round(v/100, 2),
    reverse_handler=lambda v: float(v)*100,
)

TranslationQuantifier(
    id='milliseconds_to_seconds',
    handler=lambda v: v/1000,
    reverse_handler=lambda v: float(v)*1000,
)

TranslationQuantifier(
    id='milliseconds_to_seconds_0dp',
    handler=lambda v: int(round(v/1000, 0)),
    reverse_handler=lambda v: float(v)*1000,
)

TranslationQuantifier(
    id='milliseconds_to_seconds_2dp',
    handler=lambda v: round(v/1000, 2),
    reverse_handler=lambda v: float(v)*1000,
)

TranslationQuantifier(
    id='multiplicative_damage_modifier',
    handler=lambda v: v+100,
    reverse_handler=lambda v: float(v)-100,
)

TranslationQuantifier(
    id='multiplicative_permyriad_damage_modifier',
    handler=lambda v: v/100+100,
    reverse_handler=lambda v: (float(v)-100)*100,
)

TranslationQuantifier(
    id='negate',
    handler=lambda v: -v,
    reverse_handler=lambda v: -float(v),
)

TranslationQuantifier(
    id='old_leech_percent',
    handler=lambda v: v/5,
    reverse_handler=lambda v: float(v)*5,
)

TranslationQuantifier(
    id='old_leech_permyriad',
    handler=lambda v: v/500,
    reverse_handler=lambda v: float(v)*500,
)

TranslationQuantifier(
    id='per_minute_to_per_second',
    handler=lambda v: round(v/60, 1),
    reverse_handler=lambda v: float(v)*60,
)

TranslationQuantifier(
    id='per_minute_to_per_second_0dp',
    handler=lambda v: int(round(v/60, 0)),
    reverse_handler=lambda v: float(v)*60,
)

TranslationQuantifier(
    id='per_minute_to_per_second_1dp',
    handler=lambda v: int(round(v/60, 1)),
    reverse_handler=lambda v: float(v)*60,
)

TranslationQuantifier(
    id='per_minute_to_per_second_2dp',
    handler=lambda v: round(v/60, 2),
    reverse_handler=lambda v: float(v)*60,
)

TranslationQuantifier(
    id='per_minute_to_per_second_2dp_if_required',
    handler=lambda v: round(v/60, 2) if v % 60 != 0 else v//60,
    reverse_handler=lambda v: float(v)*60,
)

TranslationQuantifier(
    id='divide_by_ten_0dp',
    handler=lambda v: v//10,
    reverse_handler=lambda v: int(v)*10,
)

TranslationQuantifier(
    id='divide_by_two_0dp',
    handler=lambda v: v//2,
    reverse_handler=lambda v: int(v)*2,
)

TranslationQuantifier(
    id='divide_by_fifteen_0dp',
    handler=lambda v: v//15,
    reverse_handler=lambda v: int(v)*15,
)

TranslationQuantifier(
    id='divide_by_twenty_then_double_0dp',
    handler=lambda v: v//20*2,
    reverse_handler=lambda v: int(v)*20//2,
)

TranslationQuantifier(
    id='canonical_line',
    type=TranslationQuantifier.QuantifierTypes.STRING,
    arg_size=0,
)

TranslationQuantifier(
    id='canonical_stat',
)

# These will be replaced by install_data_dependant_quantifiers
TranslationQuantifier(
    id='mod_value_to_item_class',
)

TranslationQuantifier(
    id='tempest_mod_text',
)

TranslationQuantifier(
    id='reminderstring',
    type=TranslationQuantifier.QuantifierTypes.STRING,
)

TranslationQuantifierHandler.init()
