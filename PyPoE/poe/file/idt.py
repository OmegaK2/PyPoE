"""
Path     PyPoE/poe/file/idt.py
Name     .idt File Format
Version  1.0.0a0
Revision $Id$
Author   [#OMEGA]- K2

INFO

File Format handler for Grinding Gear Games' .idt format.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import codecs
import re

# self
from PyPoE.shared.containers import Record, TypedList, TypedContainerMeta
from PyPoE.poe.file._shared import AbstractFile, ParserError

# =============================================================================
# Globals
# =============================================================================

__all__ = ['IDTFile']

# =============================================================================
# Classes
# =============================================================================

class CoordinateRecord(Record):

    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


class CoordinateList(TypedList, metaclass=TypedContainerMeta):
    ACCEPTED_TYPES = CoordinateRecord


class TextureRecord(Record):

    __slots__ = ['name', 'records']

    def __init__(self, name, records=None):
        self.name = name
        if records is None:
            self.records = CoordinateList()
        elif isinstance(records, CoordinateList):
            self.records = records
        elif isinstance(records, list):
            self.records = CoordinateList(records)
        else:
            raise TypeError('records must a valid CoordinateList.')



class TextureList(TypedList, metaclass=TypedContainerMeta):
    ACCEPTED_TYPES = TextureRecord


class IDTFile(AbstractFile):
    # complete match
    _regex_parse = re.compile(
        r'^'
        r'version (?P<version>[0-9]+)[\r\n]*'
        r'image "(?P<image>[\w\./_]+)"[\r\n]*'
        r'(?P<texture_count>[0-9]+)[\r\n]*'
        r'(?P<textures>.*)' # Match the rest
        r'$',
        re.UNICODE | re.MULTILINE | re.DOTALL
    )

    # for findall
    _regex_texture = re.compile(
        r'^'
        r'(?P<name>[a-zA-Z]+)[ ]+'
        r'(?P<count>[0-9]+)[ ]+'
        r'(?P<coordinates>(?:[0-9]+[ ]*)*)'
        r'[\r\n]*$',
        re.UNICODE | re.MULTILINE | re.DOTALL
    )

    # for findall
    _regex_coordinates = re.compile(
        r'(?P<x>[0-9]+)[ ]+'
        r'(?P<y>[0-9]+)[ ]*'
        r'',
        re.UNICODE | re.MULTILINE | re.DOTALL
    )

    def __init__(self, data=None):
        if data is None:
            self.version = 0
            self.image = None
            self._records = TextureList()
        else:
            tex = TextureList()
            for tex_record in data['records']:
                x = CoordinateList()
                for coord_record in tex_record['records']:
                    x.append(CoordinateRecord(**coord_record))

                kwargs = tex_record.copy()
                del kwargs['records']

                tex.append(TextureRecord(records=x, **kwargs))

            self.version = data['version']
            self.image = data['image']
            self._records = tex

    # Properties

    def _get_records(self):
        return self._records

    def _set_records(self, value):
        if isinstance(value, TextureList):
            self._records = value
        elif isinstance(value, list):
            self._records = TextureList(value)
        else:
            raise TypeError('records must be a valid TextureList.')

    records = property(fget=_get_records, fset=_set_records)

    # Private

    def _write(self, buffer):
        out = []

        out.append('version %s\n' % self.version)
        out.append('image "%s"\n' % self.image)
        out.append('%s\n' % len(self._records))
        for tex_record in self._records:
            out.append('%s %s' % (tex_record.name, len(tex_record.records)))
            for coord_record in tex_record.records:
                out.append(' %s %s' % (coord_record.x, coord_record.y))
            out.append('\n')

        ''.join(out).encode('utf-16_le')

        buffer.write(codecs.BOM_UTF16_LE + ''.join(out).encode('utf-16_le'))

    def _read(self, buffer, *args, **kwargs):
        # Should detect little endian byte order accordingly and remove the BOM
        data = buffer.read().decode('utf-16')
        match = self._regex_parse.match(data)

        if not match:
            raise ParserError('Failed to find the base information. File may not be a .idt file or malformed.')

        textures = TextureList()
        for tex_match in self._regex_texture.finditer(match.group('textures')):
            coordinates = CoordinateList()
            for coord_match in self._regex_coordinates.finditer(tex_match.group('coordinates')):
                coordinates.append(CoordinateRecord(**coord_match.groupdict()))

            if len(coordinates) != int(tex_match.group('count')):
                raise ParserError('Amount of found coordinates (%s) does not match the amount of specified coordinates (%s)' % (len(coordinates), tex_match.group('count')))

            textures.append(TextureRecord(tex_match.group('name'), coordinates))

        if len(textures) != int(match.group('texture_count')):
            raise ParserError('Amount of found textures (%s) does not match the amount of specified textures (%s)' % (len(textures), match.group('texture_count')))

        self._records = textures
        self.version = int(match.group('version'))
        self.image = match.group('image')
