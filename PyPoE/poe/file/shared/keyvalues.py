"""
Shared Utilities for files that contain key-value pairs

Overview
-------------------------------------------------------------------------------

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/shared/keyvalues.py                               |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                                                             |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
-------------------------------------------------------------------------------

Shared utilities for files that contain key-value pairs.

When implementing support for other file types that use the generic key-value
format GGG uses, the file should subclass the files found here and appropriately
change the logic.

The key value format is generally something like this:

SectionName
{
    key = value
    key = "quoted value"
}

Agreement
-------------------------------------------------------------------------------

See PyPoE/LICENSE
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import warnings
import os
from collections import defaultdict
from collections.abc import MutableMapping
from enum import Enum

# 3rd-party

# self
from PyPoE.poe.file.shared import AbstractFile, ParserError, ParserWarning
from PyPoE.poe.file.ggpk import GGPKFile

# =============================================================================
# Globals
# =============================================================================

__all__ = []

# =============================================================================
# Classes
# =============================================================================


class DuplicateKeyWarning(ParserWarning):
    """
    Warning for keys that are not explicitly specified to be overridden.
    """
    pass


class AbstractKeyValueSection(dict):
    APPEND_KEYS = []
    OVERRIDE_KEYS = []
    OVERRIDE_WARNING = True
    NAME = ''

    def __init__(self, parent, name=None, *args, **kwargs):
        super(AbstractKeyValueSection, self).__init__(*args, **kwargs)
        self.parent = parent
        if name:
            self.name = name
        elif self.NAME:
            self.name = self.NAME
        else:
            raise ParserError('Missing name for section')

    def __setitem__(self, key, value):
        if key in self.APPEND_KEYS:
            if isinstance(value, set):
                if key in self:
                    value = self[key].union(value)
                else:
                    pass
            else:
                if key in self:
                    self[key].add(value)
                    return
                else:
                    value = {value, }
        elif self.OVERRIDE_WARNING and key in self and self[key] != value and key not in self.OVERRIDE_KEYS:
            warnings.warn('Override of %s[%s] to %s (was %s)' % (
                self.name, repr(key), repr(value), repr(self[key])
            ), DuplicateKeyWarning)

        super(AbstractKeyValueSection, self).__setitem__(key, value)

    def merge(self, other):
        if not isinstance(other, AbstractKeyValueSection):
            raise TypeError('Other must be a AbstractKeyValuesSection instance, got "%s" instead.' % other.__class__.__name__)

        for k, v in other.items():
            #print(k, v)
            if k in self:
                warnings.warn("%s, %s" % (k, v))
            self[k] = v


class AbstractKeyValueFile(AbstractFile, defaultdict):
    """


    :ivar _parent_dir:
    :type _parent_dir: str

    :ivar _parent_ggpk:
    :type _parent_ggpk: GGPKFile

    :ivar _parent_file:
    :type _parent_file: AbstractKeyValueFile

    :ivar version:
    :type version: None or int

    :ivar extends:
    :type extends: None or str
    """
    version = None
    extends = None

    SECTIONS = {}

    EXTENSION = ''

    _re_header = re.compile(
        r'^'
        r'version (?P<version>[0-9]+)[\r\n]*'
        r'extends "(?P<extends>[\w\./_]+)"[\r\n]*'
        r'(?P<remainder>.*)' # Match the rest
        r'$',
        re.UNICODE | re.MULTILINE | re.DOTALL
    )

    _re_find_kv_sections = re.compile(
        r'^(?P<key>[\w]+)[\r\n]+'
        r'^{'
        r'(?P<contents>[^}]*)'
        r'^}',
        re.UNICODE | re.MULTILINE,
    )

    _re_find_kv_pairs = re.compile(
        r'^[\s]*'
        r'(?P<key>[\w]*)'
        r'[\s]*=[\s]*'
        r'(?P<value>"[^"]*"|[\w]*)'
        r'[\s]*$',
        re.UNICODE | re.MULTILINE,
    )

    def __init__(self, parent_or_base_dir_or_ggpk=None, version=None, extends=None, keys=None):
        super(AbstractKeyValueFile, self).__init__()

        self.version = version
        self.extends = extends
        #self._keys = keys if keys else {}

        #for cls in self.SECTIONS:
        #    self[cls.NAME] = cls(parent=self)

        self._parent_dir = None
        self._parent_file = None
        self._parent_ggpk = None

        if isinstance(parent_or_base_dir_or_ggpk, AbstractKeyValueFile):
            self._parent_file = parent_or_base_dir_or_ggpk
        elif isinstance(parent_or_base_dir_or_ggpk, GGPKFile):
            self._parent_ggpk = parent_or_base_dir_or_ggpk
        elif isinstance(parent_or_base_dir_or_ggpk, str):
            self._parent_dir = parent_or_base_dir_or_ggpk
        elif parent_or_base_dir_or_ggpk is not None:
            raise TypeError('parent_or_base_dir_or_ggpk is of invalid type.')

    def __missing__(self, key):
        try:
            self[key] = self.SECTIONS[key](parent=self)
        except KeyError:
            self[key] = AbstractKeyValueSection(parent=self, name=key)

        return self[key]

    def __delitem__(self, key):
        raise NotImplementedError()

    def __repr__(self):
        return '%(name)s(extends="%(extends)s", version="%(version)s", keys=%(keys)s' % {
            'name': self.__class__.__name__,
            'extends': self.extends,
            'version': self.version,
            'keys': defaultdict.__repr__(self),
        }

    def _read(self, buffer):
        data = buffer.read().decode('utf-16')

        match = self._re_header.match(data)
        if match is None:
            raise ParserError('File is not a valid %s file.' % self.__class__.__name__)

        extend = match.group('extends')

        if extend == 'nothing':
            self.extends = None
        elif extend:
            if self._parent_file:
                self.merge(self._parent_file)
                if self._parent_file.name != extend:
                    warnings.warn(
                        'Parent file name "%s" doesn\'t match extended file '
                        'name "%s"' % (self._parent_file.name, extend),
                        ParserWarning,
                    )
            elif self._parent_dir:
                obj = self.__class__(
                    parent_or_base_dir_or_ggpk=self._parent_dir
                )
                obj.read(file_path_or_raw=os.path.join(
                    self._parent_dir, extend + self.EXTENSION
                ))
                self.merge(obj)
            elif self._parent_ggpk:
                obj = self.__class__(
                    parent_or_base_dir_or_ggpk=self._parent_ggpk
                )
                obj.read(file_path_or_raw=
                    self._parent_ggpk.directory[extend].extract()
                )
                self.merge(obj)
            else:
                raise ParserError('File extends "%s", but parent_or_base_dir_or_ggpk has not been specified on class creation.' % extend)
            self.__class__()

        self.version = match.group('version')

        for section_match in self._re_find_kv_sections.finditer(match.group('remainder')):
            key = section_match.group('key')

            try:
                section = self[key]
            except KeyError:
                #print('Extra section:', key)
                section = AbstractKeyValueSection(parent=self, name=key)
                self[key] = section

            for kv_match in self._re_find_kv_pairs.finditer(section_match.group('contents')):
                value = kv_match.group('value').strip('"')
                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass

                section[kv_match.group('key')] = value

    def _get_name(self):
        return self._name

    def merge(self, other):
        """

        :param other:
        :type other: AbstractKeyValueFile
        """
        if not isinstance(other, self.__class__):
            raise ValueError('Can\'t merge only with classes with the same base class, got "%s" instead' % other.__class__.__name__)

        for k, v in other.items():
            if k in self:
                self[k].merge(v)
            else:
                self[k] = v


    name = property(fget=_get_name)

# =============================================================================
# Functions
# =============================================================================
