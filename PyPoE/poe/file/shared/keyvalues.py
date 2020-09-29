"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/shared/keyvalues.py                               |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Shared abstract classes for files that contain key-value pairs.

When implementing support for other file types that use the generic key-value
format GGG uses, the file should subclass the files found here and appropriately
change the logic.

The key value format is generally something like this:

.. code-block:: none

    SectionName
    {
        key = value
        key = "quoted value"
    }

.. warning::
    None of the abstract classes found here should be instantiated directly.

See also:

* :mod:`PyPoE.poe.file.shared`
* :mod:`PyPoE.poe.file.shared.cache`


Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Abstract Classes
-------------------------------------------------------------------------------

.. autoclass:: AbstractKeyValueSection
    :private-members:
    :no-inherited-members:

.. autoclass:: AbstractKeyValueFile
    :exclude-members: write
    :private-members:
    :no-inherited-members:

    .. automethod:: read
    .. automethod:: get_read_buffer
    .. automethod:: write
    .. automethod:: get_write_buffer


.. autoclass:: AbstractKeyValueFileCache
    :private-members:

Exceptions & Warnings
-------------------------------------------------------------------------------

.. autoclass:: DuplicateKeyWarning

.. autoclass:: OverriddenKeyWarning
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re
import warnings
import os
from collections import defaultdict, OrderedDict
from typing import Union

# 3rd-party

# self
from PyPoE.shared.decorators import doc
from PyPoE.poe.file.shared import AbstractFile, ParserError, ParserWarning
from PyPoE.poe.file.shared.cache import AbstractFileCache
from PyPoE.poe.file.file_system import FileSystem

# =============================================================================
# Globals
# =============================================================================

__all__ = [
    'AbstractKeyValueFile', 'AbstractKeyValueFileCache',
    'AbstractKeyValueSection'
]

# =============================================================================
# Classes
# =============================================================================


class DuplicateKeyWarning(ParserWarning):
    """
    Warning for keys that are not explicitly specified to be overridden.
    """
    pass


class OverriddenKeyWarning(ParserWarning):
    """
    Warning for keys that are overridden during a merge.
    """
    pass


class AbstractKeyValueSection(dict):
    APPEND_KEYS = set()
    ORDERED_HASH_KEYS = set()
    NAME = ''

    def __init__(self, parent, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent: 'AbstractKeyValueFile' = parent
        if name:
            self.name: str = name
        elif self.NAME:
            self.name: str = self.NAME
        else:
            raise ParserError('Missing name for section')

    def __setitem__(self, key, value):
        # Equals "override" behaviour
        if key in self.ORDERED_HASH_KEYS:
            if not isinstance(value, OrderedDict):
                if key in self:
                    self[key][value] = True
                    return
                else:
                    value = OrderedDict(((value, True), ))
        elif key in self.APPEND_KEYS:
            if not isinstance(value, list):
                if key in self:
                    self[key].append(value)
                    return
                else:
                    value = [value, ]
        super().__setitem__(key, value)

    def merge(self, other: 'AbstractKeyValueSection'):
        if not isinstance(other, AbstractKeyValueSection):
            raise TypeError(
                'Other must be a AbstractKeyValuesSection instance, got "%s" '
                'instead.' % other.__class__.__name__
            )

        for k, v in other.items():
            if k in self.ORDERED_HASH_KEYS:
                if isinstance(v, OrderedDict):
                    if k in self:
                        v = OrderedDict(list(self[k].items()) + list(v.items()))
                    else:
                        v = OrderedDict(v.items())
                else:
                    if k in self:
                        self[k][v] = True
                        continue
                    else:
                        v = OrderedDict(((v, True), ))
            elif k in self.APPEND_KEYS:
                if isinstance(v, list):
                    if k in self:
                        v += self[k]
                    else:
                        pass
                else:
                    if k in self:
                        self[k].append(v)
                        continue
                    else:
                        v = [v, ]
            elif k in self:
                continue

            self[k] = v


class AbstractKeyValueFile(AbstractFile, defaultdict):
    """
    Attributes
    ----------
    SECTIONS : dict[AbstractKeyValueSection]
        Registered sections for this class
    EXTENSION : str
        File extension (if any) for this file class
    _parent_dir : str

    _parent_ggpk : GGPKFile

    _parent_file : AbstractKeyValueFile

    version : None or int
        File format version of the file
    extends : None or str
        Whether the file extends another file
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
        r'(?P<key>[\S]+)'
        r'[\s]*=[\s]*'
        r'(?P<value>"[^"]*"|[\S]+)'
        r'[\s]*$',
        re.UNICODE | re.MULTILINE,
    )

    def __init__(self,
                 parent_or_file_system: Union['AbstractKeyValueFile', FileSystem,
                                              None] = None,
                 version: Union[int, None] = None,
                 extends: Union[str, None] = None,
                 keys=None
                 ):
        AbstractFile.__init__(self)
        defaultdict.__init__(self, keys)

        self.version: Union[int, None] = version
        self.extends: Union[str, None] = extends

        self._parent_file: Union[AbstractKeyValueFile, None] = None
        self._parent_file_system: Union[FileSystem, None] = None

        if isinstance(parent_or_file_system, AbstractKeyValueFile):
            self._parent_file = parent_or_file_system
        elif isinstance(parent_or_file_system, FileSystem):
            self._parent_file_system = parent_or_file_system
        elif parent_or_file_system is not None:
            raise TypeError('parent_or_file_system is of invalid type.')

    #
    # Properties
    #
    @property
    def parent_or_file_system(self) -> Union['AbstractKeyValueFile', FileSystem]:
        return self._parent_file or self._parent_file_system

    #
    # Special
    #
    def __missing__(self, key) -> AbstractKeyValueSection:
        try:
            self[key] = self.SECTIONS[key](parent=self)
        except KeyError:
            self[key] = AbstractKeyValueSection(parent=self, name=key)

        return self[key]

    def __delitem__(self, key):
        raise NotImplementedError()

    def __repr__(self) -> str:
        return '%(name)s(extends="%(extends)s", version="%(version)s", ' \
               'keys=%(keys)s' % {
                    'name': self.__class__.__name__,
                    'extends': self.extends,
                    'version': self.version,
                    'keys': defaultdict.__repr__(self),
               }

    @doc(doc=AbstractFile._read)
    def _read(self, buffer, *args, **kwargs):
        data = buffer.read().decode('utf-16')

        match = self._re_header.match(data)
        if match is None:
            raise ParserError(
                'File is not a valid %s file.' % self.__class__.__name__
            )

        self.version = int(match.group('version'))

        for section_match in self._re_find_kv_sections.finditer(
                match.group('remainder')):
            key = section_match.group('key')

            try:
                section = self[key]
            except KeyError:
                #print('Extra section:', key)
                section = AbstractKeyValueSection(parent=self, name=key)
                self[key] = section

            for kv_match in self._re_find_kv_pairs.finditer(
                    section_match.group('contents')):
                value = kv_match.group('value').strip('"')
                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            pass

                section[kv_match.group('key')] = value

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
            elif self._parent_file_system:
                obj = self.__class__(
                    parent_or_file_system=self._parent_file_system
                )
                obj.read(
                    file_path_or_raw=self._parent_file_system.get_file(
                        extend + self.EXTENSION
                    ),
                )
                self.merge(obj)
            else:
                raise ParserError(
                    'File extends "%s", but parent_or_file_system has not '
                    'been specified on class creation.' % extend
                )
            self.extends = extend

    @doc(doc=AbstractFile._write)
    def _write(self, buffer, *args, **kwargs):
        lines = [
            'version %s' % self.version,
            'extends "%s"' % (self.extends if self.extends else 'nothing'),
        ]

        for section, keyvalues in self.items():
            lines.append('')
            lines.append(section)
            lines.append('{')
            for key, value in keyvalues.items():
                if isinstance(value, list):
                    for v in value:
                        lines.append(self._get_write_line(key, v))
                else:
                    lines.append(self._get_write_line(key, value))
            lines.append('}')

        buffer.write('\n'.join(lines).encode('utf-16le'))

    @doc(prepend=AbstractFile.write)
    def write(self, *args, **kwargs):
        """
        Warning
        -------
            The current values held by the file instance will be written. This
            means values inherited from parent files will also be written.
        """
        return super().write(*args, **kwargs)

    def _get_write_line(self, key, value):
        return '\t%s = "%s"' % (key, value)

    def merge(self, other: 'AbstractKeyValueFile'):
        """
        Merge with other file.

        Parameters
        ----------
        other : AbstractKeyValueFile
            Instance of the other file to merge with


        Raises
        ------
        ValueError
            if other has a different type then this instance
        """
        if not isinstance(other, self.__class__):
            raise ValueError(
                'Can\'t merge only with classes with the same base class, got '
                '"%s" instead' % other.__class__.__name__
            )

        for k, v in other.items():
            if k in self:
                self[k].merge(v)
            else:
                self[k] = v


class AbstractKeyValueFileCache(AbstractFileCache):
    FILE_TYPE = AbstractKeyValueFile

    @doc(doc=AbstractFileCache._get_file_instance_args)
    def _get_file_instance_args(self, file_name):
        options = super()._get_file_instance_args(file_name)
        options['parent_or_file_system'] = self.file_system

        return options
# =============================================================================
# Functions
# =============================================================================
