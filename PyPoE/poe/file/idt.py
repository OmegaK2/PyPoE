"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/idt.py                                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

File Format handler for Grinding Gear Games' .idt format.

.idt files are generally used to link the inventory texture to an object.

Agreement
===============================================================================

See PyPoE/LICENSE

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

.. autoclass:: IDTFile

.. autoclass:: TextureRecord

.. autoclass:: CoordinateRecord


Internal API
-------------------------------------------------------------------------------

.. autoclass:: TextureList

.. autoclass:: CoordinateList
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import codecs
import re

# self
from PyPoE.shared.containers import Record, TypedList, TypedContainerMeta
from PyPoE.poe.file.shared import AbstractFile, ParserError

# =============================================================================
# Globals
# =============================================================================

__all__ = ['IDTFile', 'TextureRecord', 'CoordinateRecord']

# =============================================================================
# Classes
# =============================================================================


class CoordinateRecord(Record):
    """
    Object that represents a single coordinate with the relevant attributes

    Attributes
    ----------
    x :  int
        x-coordinate
    y :  int
        y-coordinate
    """
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        """
        Parameters
        ----------
        x :  int
            x-coordinate
        y :  int
            y-coordinate
        """
        self.x = int(x)
        self.y = int(y)


class CoordinateList(TypedList, metaclass=TypedContainerMeta):
    """
    A list that only accepts :class:`CoordinateRecord` instances.
    """
    ACCEPTED_TYPES = CoordinateRecord


class TextureRecord(Record):
    """
    Object that represents a single texture with the relevant attributes

    Attributes
    ----------
    'name' :  str
        name (internal path) of the texture
    'records' : CoordinateList[CoordinateRecord]
        :class:`CoordinateList` of :class:`CoordinateRecord` instances for this
        texture.
    """

    __slots__ = ['name', 'records']

    def __init__(self, name, records=None):
        """
        Parameters
        ----------
        name :  str
            name (internal path) of the texture
        records : None or CoordinateList[CoordinateRecord]
            :class:`CoordinateList` of :class:`CoordinateRecord` instances for
            this texture. If None, an empty :class:`CoordinateList` will be
            created.

        Raises
        ------
        TypeError
            If records is of invalid type
        TypeError
            If the containing types of records are invalid
        """
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
    """
    A list that only accepts TextureRecord instances.
    """
    ACCEPTED_TYPES = TextureRecord


class IDTFile(AbstractFile):
    """
    Encapsulated in-memory representation of .idt files.
    """
    # complete match
    _regex_parse = re.compile(
        r'^'
        r'version (?P<version>[0-9]+)[\r\n]*'
        r'image "(?P<image>[\w\./\\_\'\-]+)"[\r\n]*'
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

    EXTENSION = '.idt'

    def __init__(self, data=None):
        """
        Creates a new IDTFile instance.

        Optionally data can be specified to initialize the object in memory
        with the given data. The same can be achieved by simply setting the
        relevant attributes.
        Note that :meth:`IDTFile.read` will override any initial data.

        Parameters
        ----------
        data : dict or None
            Take a dict containing the data to create this object and it's
            attributes with. The dict should match the structure of the classes
            attributes and the respective sub attributes.

        Raises
        ------
        TypeError
            if dict contains data of invalid types
        """
        if data is None:
            self.version = 0
            self._image = None
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
        """
        Get records

        Returns
        -------
        TextureList[TextureRecord]
            List of stored :class:`TextureRecord` instances
        """
        return self._records

    def _set_records(self, value):
        """
        Set records

        Parameters
        ----------
        value : TextureList[TextureRecord]
            value to set the records to

        Raises
        ------
        TypeError
            if the record is an invalid texture list

        """
        if isinstance(value, TextureList):
            self._records = value
        elif isinstance(value, list):
            self._records = TextureList(value)
        else:
            raise TypeError('records must be a valid TextureList.')

    records = property(fget=_get_records, fset=_set_records)

    def _get_image(self):
        """
        Get image path

        Returns
        -------
        str
            image path relative to content.ggpk root
        """
        return self._image

    def _set_image(self, value):
        """
        Set image path

        Parameters
        ----------
        value : str
            image path relative to content.ggpk root
        """
        self._image = value.replace('\\', '/')

    image = property(fget=_get_image, fset=_set_image)

    # Private

    def _write(self, buffer):
        out = []

        out.append('version %s\n' % self.version)
        out.append('image "%s"\n' % self._image)
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
