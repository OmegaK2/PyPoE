"""
Overview
===============================================================================

+----------+------------------------------------------------------------------+
| Path     | PyPoE/poe/file/dat.py                                            |
+----------+------------------------------------------------------------------+
| Version  | 1.0.0a0                                                          |
+----------+------------------------------------------------------------------+
| Revision | $Id$                  |
+----------+------------------------------------------------------------------+
| Author   | Omega_K2                                                         |
+----------+------------------------------------------------------------------+

Description
===============================================================================

Support for .dat file format.

.dat files can be found in Data/ and are read by :class:`DatFile`.
Unfortunately, there is no magic keyword for identifying the GGG .dat format,
so advise caution when trying to read dat files.

The GGG .dat format uses a fixed-width table and a variable-length data section.
In the fixed-width table, the number of rows is defined, however, the data
format stored has to be reverse-engineered and is currently not stored in the
file itself.
The data is a continuous amount of binary data; reading values form there is
generally done by pointers (int) or list pointers (size, int) from the
table-data.

A list of default specification is included with PyPoE; to set the correct
version :func:`set_default_spec` may be used.

Agreement
===============================================================================

See PyPoE/LICENSE


.. todo::

    * DatValue.get_value might hit the python recursion limit, but it is not a
      problem for any of the actual dat files.
    * Update RR with the new indexing

Documentation
===============================================================================

Public API
-------------------------------------------------------------------------------

.. autoclass:: DatFile

.. autoclass:: RelationalReader

.. autofunction:: set_default_spec

Internal API
-------------------------------------------------------------------------------

.. autoclass:: DatReader

.. autoclass:: DatValue
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import struct
import warnings
from enum import IntEnum
from io import BytesIO
from collections import OrderedDict, defaultdict
from collections.abc import Iterable

# 3rd-party

# self
from PyPoE.shared.decorators import deprecated, doc
from PyPoE.shared.mixins import ReprMixin
from PyPoE.poe import constants
from PyPoE.poe.file.shared import AbstractFileReadOnly
from PyPoE.poe.file.shared.cache import AbstractFileCache
from PyPoE.poe.file.specification import load
from PyPoE.poe.file.specification.errors import SpecificationError, \
    SpecificationWarning

# =============================================================================
# Globals
# =============================================================================

_default_spec = None

__all__ = [
    'DAT_FILE_MAGIC_NUMBER',
    'DatFile', 'RelationalReader',
    'set_default_spec',
]

DAT_FILE_MAGIC_NUMBER = b'\xBB\xbb\xBB\xbb\xBB\xbb\xBB\xbb'

# =============================================================================
# Classes
# =============================================================================


class DatValue:
    """
    Representation of a value found in a dat file.

    DatValue instances are created by reading or writing a DatValue and should
    not be directly be created. The purpose of DatValues is to keep information
    regarding the placement of the value in the respective DatFile intact.



    Support for built-ins:

    DatValue do support comparison, however is it performed on the dereferenced
    value it holds, not the equality of the dat value itself.

    This means generally DatValues can be compared to anything, the actual
    comparison is however performed depending on the data type.

    Example 1: dat_value < 0

    * works if the dat_value holds an integer
    * raises TypeError if it holds a list

    Example 2: dat_value1 < dat_value2

    * works if both dat values have the same or comparable types
    * raises TypeError if one holds a list, and the other an integer


    Dev notes:
    Must keep the init
    """

    # Very important to cut down the cost of class creation
    # In some dat files we may be creating millions of instances, simply using
    # slots can make a significant difference (~35% speedup)
    __slots__ = [
        'value', 'size', 'offset', 'parent', 'specification', 'children',
        'child',
    ]

    def __init__(self, value=None, offset=None, size=None, parent=None,
                 specification=None):
        self.value = value
        self.size = size
        self.offset = offset
        self.parent = parent
        self.specification = specification
        self.children = None
        self.child = None

    def __repr__(self):
        # TODO: iterative vs recursive?
        if self.is_pointer:
            return repr(self.child)
        elif self.is_list:
            return repr([repr(dv) for dv in self.children])
        else:
            return 'DatValue(' + repr(self.value) +')'

    def __lt__(self, other):
        if not isinstance(other, DatValue):
            return self.get_value() < other

        return self.get_value() < other.get_value()

    def __le__(self, other):
        if not isinstance(other, DatValue):
            return self.get_value() <= other

        return self.get_value() <= other.get_value()

    def __eq__(self, other):
        if not isinstance(other, DatValue):
            return self.get_value() == other

        return self.get_value() == other.get_value()

    def __ne__(self, other):
        if not isinstance(other, DatValue):
            return self.get_value() != other

        return self.get_value() != other.get_value()

    def __gt__(self, other):
        if not isinstance(other, DatValue):
            return self.get_value() > other

        return self.get_value() > other.get_value()

    def __ge__(self, other):
        if not isinstance(other, DatValue):
            return self.get_value() >= other

        return self.get_value() >= other.get_value()
    # Properties

    def _get_data_size(self):
        """
        Retrieves size of the data held by the current instance in the data
        section.

        Returns
        -------
        int
            size of data


        Raises
        ------
        TypeError
            If performed on DatValue instances without data
        """
        if self.is_list:
            if self.children:
                size = self.children[0].size * self.value[0]
            else:
                size = 0
        elif self.is_pointer:
            size = self.child.size
        else:
            raise TypeError('Only supported on DatValue instances with data (lists, pointers)')
        return size

    def _get_data_start_offset(self):
        """
        Retrieves the start offset of the data held by the current instance in
        the data section.

        Returns
        -------
        int
            start offset of data


        Raises
        ------
        TypeError
            If performed on DatValue instances without data
        """
        if self.is_list:
            return self.value[1]
        elif self.is_pointer:
            return self.value
        else:
            raise TypeError('Only supported on DatValue instances with data (lists, pointers)')

    def _get_data_end_offset(self):
        """
        Retrieves the end offset of the data held by the current instance in the
        data section.

        Returns
        -------
        int
            end offset of data


        Raises
        ------
        TypeError
            If performed on DatValue instances without data
        """
        return self._get_data_start_offset() + self._get_data_size()

    def _is_data(self):
        """
        Whether this DatValue instance is data or not.

        Returns
        -------
        bool
        """
        return self.parent is not None

    def _has_data(self):
        """
        Whether this DatValue instance has data or not; this applies to types
        that hold a pointer.

        Returns
        -------
        bool
        """
        return self.is_list or self.is_pointer

    def _is_list(self):
        """
        Whether this DatValue instance is a list.

        Returns
        -------
        bool
        """
        return self.children is not None

    def _is_pointer(self):
        """
        Whether this DatValue instance is a pointer.

        Returns
        -------
        bool
        """
        return self.child is not None

    def _is_parsed(self):
        """
        Whether this DatValue instance is parsed (i.e. non bytes).

        Returns
        -------
        bool
        """
        return not isinstance(self.value, bytes)

    data_size = property(fget=_get_data_size)
    data_start_offset = property(fget=_get_data_start_offset)
    data_end_offset = property(fget=_get_data_end_offset)
    is_data = property(fget=_is_data)
    has_data = property(fget=_has_data)
    is_list = property(fget=_is_list)
    is_pointer = property(fget=_is_pointer)
    is_parsed = property(fget=_is_parsed)

    # Public

    def get_value(self):
        """
        Returns the value that is held by the DatValue instance. This is done
        recursively, i.e. pointers will be dereferenced accordingly.

        This means if you want the actual value of the DatValue, you should
        probably access the value attribute instead.


        If this DatValue instance is a list, this means a python list of items
        will be returned.
        If this DatValue instance is a pointer, this means whatever value the
        child of this instance holds will be returned.
        Otherwise the value of the DatValue instance itself will be returned.

        Note, that values may be nested i.e. if a list contains a list, a
        nested list will be returned accordingly.

        Returns
        -------
        object
            the dereferenced value
        """
        if self.is_pointer:
            return self.child.get_value()
        elif self.is_list:
            return [dv.get_value() for dv in self.children]
        else:
            return self.value


class DatRecord(list):
    """
    Attributes
    ----------
    parent :  DatReader
        The parent DatReader instance this DatRecord instance belongs to
    rowid :  int
        The rowid of this DatRecord instance
    """

    __slots__ = ['parent', 'rowid']

    def __init__(self, parent, rowid):
        """
        Parameters
        ----------
        parent :  DatReader
            The parent DatReader instance this DatRecord instance belongs to
        rowid :  int
            The rowid of this DatRecord instance
        """
        list.__init__(self)
        self.parent = parent
        self.rowid = rowid

    def __getitem__(self, item):
        if isinstance(item, str):
            if item in self.parent.table_columns:
                value = list.__getitem__(self, self.parent.table_columns[item]['index'])
                if isinstance(value, DatValue):
                    value = value.get_value()
                return value
            elif item in self.parent.specification['virtual_fields']:
                field = self.parent.specification['virtual_fields'][item]
                value = [self[fn] for fn in field['fields']]
                if field['zip']:
                    value = zip(*value)
                return value
            else:
                raise KeyError(item)
        return list.__getitem__(self, item)

    def __repr__(self):
        stuff = ["{%s: %s}" % (k, self[i]) for i, k in enumerate(self.parent.table_columns)]
        return '[%s]' % ', '.join(stuff)
    '''def find_all(self, key, value):
        row_index = self._get_column_index(key)
        values = []
        for row in self:
            if row[row_index] == value:
                values.append(value)
        return values'''

    def __hash__(self):
        return hash((self.parent.file_name, self.rowid))

    def iter(self):
        """
        Iterates over the DatRecord and returns key, value and index

        Yields
        ------
        str
            key
        object
            the value
        int
            index
        """
        for index, key in enumerate(self.parent.table_columns):
            yield key, self[key], index

    def keys(self):
        """

        Returns
        -------

        """
        return self.parent.table_columns.keys()


class DatReader(ReprMixin):
    """
    Attributes
    ----------
    _table_offset :  int
        Starting offset of table data in bytes
    _cast_table : dict[str, list[str, int]]
        Mapping of cast type to the corresponding struct
    type and the size
        of the cast in bytes
    auto_build_index : bool
        Whether the index is automatically build after reading
    x64 : bool
        Whether this the reader is running in 64 bit mode
    file_name :  str
        File name
    file_length :  int
        File length in bytes
    table_data : list[DatRecord[object]]
        List of rows containing DatRecord entries.
    table_length :  int
        Length of table in bytes
    table_record_length :  int
        Length of each record in bytes
    table_rows :  int
        Number of rows in table
    data_offset :  int
        Data section offset
    columns :  OrderedDict
        Shortened list of columns excluding intermediate columns
    columns_zip :  OrderedDict
        Shortened list of columns excluding zipped columns
    columns_all :  OrderedDict
        Complete list of columns, including all intermediate and virtual columns
    columns_data :  OrderedDict
        List of all columns directly derived from the data
    columns_unique:  OrderedDict
        List of all unique columns (which are also considered indexable)
    table_columns :  OrderedDict
        Used for mapping columns to indexes
    """
    _table_offset = 4
    _cast_table = {
        'bool': ['?', 1],
        'byte': ['b', 1],
        'ubyte': ['B', 1],
        'short': ['h', 2],
        'ushort': ['H', 2],
        'int': ['i', 4],
        'uint': ['I', 4],
        'long': ['q', 8],
        'ulong': ['Q', 8],
        'float': ['f', 4],
        'double': ['d', 8],
    }

    class CastTypes(IntEnum):
        VALUE = 1
        STRING = 2
        POINTER_LIST = 3
        POINTER = 4
        POINTER_SELF = 5

    def __init__(self, file_name, *args, use_dat_value=True, specification=None,
                 auto_build_index=False, x64=False):
        """
        Parameters
        ----------
        file_name : str
            Name of the dat file
        use_dat_value : bool
            Whether to use :class:`DatValue` instances or values
        specification : Specification
            Specification to use
        auto_build_index : bool
            Whether to automatically build the index for unique columns after
            reading.
        x64 : bool
            Whether the reader should run in 64 bit mode for dat64 files.

        Raises
        ------
        errors.SpecificationError
            if the dat file is not in the specification
        """
        self.auto_build_index = auto_build_index
        self.x64 = x64
        self.index = {}
        self.data_parsed = []
        self.data_offset = 0
        self.file_length = 0
        self._file_raw = b''
        self.table_data = []

        self.table_length = 0
        self.table_record_length = 0
        self.table_rows = 0
        self.file_name = file_name

        # Fix for the look up
        if x64:
            _file_name = file_name.replace('.dat64', '.dat')
        else:
            _file_name = file_name

        self.use_dat_value = use_dat_value

        # Process specification
        if specification is None:
            if _file_name in _default_spec:
                specification = _default_spec[_file_name]
            else:
                raise SpecificationError(
                    SpecificationError.ERRORS.RUNTIME_MISSING_SPECIFICATION,
                    'No specification for "%s"' % file_name
                )
        else:
            specification = specification[_file_name]
        self.specification = specification

        # Prepare the casts
        self.table_columns = OrderedDict()
        self.cast_size = 0
        self.cast_spec = []
        self.cast_row = []
        for i, key in enumerate(specification.columns_data):
            k = specification.fields[key]
            self.table_columns[key] = {'index': i, 'section': k}
            casts = []
            remainder = k.type
            while remainder:
                remainder, cast_type = self._get_cast_type(remainder)
                casts.append(cast_type)
            self.cast_size += casts[0][1]

            self.cast_spec.append((k, casts))
            self.cast_row.append(casts[0][2])

        self.cast_row = '<' + ''.join(self.cast_row)

        for var in ('columns', 'columns_all', 'columns_zip', 'columns_data',
                    'columns_unique'):
            setattr(self, var, getattr(specification, var))

    def __iter__(self):
        return iter(self.table_data)

    def __getitem__(self, item):
        return self.table_data[item]

    def build_index(self, column=None):
        """
        Builds or rebuilds the index for the specified column.

        Indexed columns can be accessed though the instance variable index and
        will return a single value for unique columns and a list for non-unique
        columns.

        For example:
        self.index[column_name][indexed_value]

        .. warning::
            This method only works for columns that are marked as unique in the
            specification.

        Parameters
        ----------
        column : str or Iterable or None
            if specified the index will the built for the specified column
            or iterable of columns
            if not specified, the index will be build for any 'unique' columns
            by default
        """
        columns = set()
        if column is None:
            for column in self.columns_unique:
                columns.add(column)
        elif isinstance(column, str):
            columns.add(column)
        elif isinstance(column, Iterable):
            for c in column:
                columns.add(c)

        columns_1to1 = set()
        columns_1toN = set()
        columns_NtoN = set()
        for column in columns:
            if column in self.columns_unique:
                self.index[column] = {}
                columns_1to1.add(column)
            elif self.specification.fields[column].type.startswith('ref|list'):
                columns_NtoN.add(column)
                self.index[column] = defaultdict(list)
            else:
                columns_1toN.add(column)
                self.index[column] = defaultdict(list)

        # Second loop
        for row in self:
            for column in columns_1to1:
                self.index[column][row[column]] = row
            for column in columns_1toN:
                self.index[column][row[column]].append(row)
            for column in columns_NtoN:
                for value in row[column]:
                    self.index[column][value].append(row)

    def row_iter(self):
        """
        Returns
        -------
        iter
            Iterator over the rows
        """
        return iter(self.table_data)

    def column_iter(self):
        """
        Iterators over the columns

        Yields
        ------
        list
            Values per column
        """
        for ci, column in enumerate(self.table_columns):
            yield [item[ci] for item in self]

    def _get_cast_type(self, caststr):
        size = None
        cast = None
        remainder = ''
        if caststr in self._cast_table:
            cast_type = self.CastTypes.VALUE
            size = self._cast_table[caststr][1]
            cast = self._cast_table[caststr][0]
        elif caststr == 'string':
            cast_type = self.CastTypes.STRING
        elif caststr.startswith('ref|list|'):
            cast_type = self.CastTypes.POINTER_LIST
            if self.x64:
                size = 16
                cast = 'QQ'
            else:
                size = 8
                cast = 'II'
            remainder = caststr[9:]
        elif caststr.startswith('ref|'):
            if self.x64:
                size = 8
                cast = 'Q'
            else:
                size = 4
                cast = 'I'
            if caststr.startswith('ref|generic'):
                cast_type = self.CastTypes.POINTER_SELF
            else:
                cast_type = self.CastTypes.POINTER
                remainder = caststr[4:]
        return remainder, (cast_type, size, cast)

    def _cast_from_spec(self, specification, casts, parent=None, offset=None, data=None, queue_data=None):
        if casts[0][0] in (self.CastTypes.VALUE, self.CastTypes.POINTER_SELF):
            ivalue = data[0] if data else struct.unpack('<' + casts[0][2], self._file_raw[offset:offset+casts[0][1]])[0]

            if ivalue in (-0x1010102, 0xFEFEFEFE, -0x101010101010102, 0xFEFEFEFEFEFEFEFE, 0xFFFFFFFF):
                ivalue = None

            if self.use_dat_value:
                value = DatValue(ivalue, offset, casts[0][1], parent, specification)
            else:
                value = ivalue
        elif casts[0][0] == self.CastTypes.STRING:
            # Beginning of the sequence, +1 to adjust for it
            offset_new = self._file_raw.find(b'\x00\x00\x00\x00', offset)
            # Account for 0 size strings
            if offset == offset_new:
                string = ''
            else:
                # It's possible that a string ends in \x00 and the next starts
                # with \x00
                # UTF-16 must be at least a multiple of 2
                while (offset_new-offset) % 2:
                    offset_new = self._file_raw.find(b'\x00\x00\x00\x00', offset_new+1)
                string = self._file_raw[offset:offset_new].decode('utf-16')
            # Store the offset including the null terminator
            if self.use_dat_value:
                value = DatValue(string, offset, offset_new-offset+4, parent, specification)
            else:
                value = string

        elif casts[0][0] in (self.CastTypes.POINTER_LIST, self.CastTypes.POINTER):
            data = data if data else struct.unpack('<' + casts[0][2], self._file_raw[offset:offset+casts[0][1]])
            data_offset = data[-1] + self.data_offset

            # Instance..
            if self.use_dat_value:
                value = DatValue(data[0] if casts[0][0] == 4 else data, offset, casts[0][1], parent, specification)

                if casts[0][0] == self.CastTypes.POINTER_LIST:
                    value.children = []
                    for i in range(0, data[0]):
                        '''if offset < self._data_offset_current:
                            print(self._data_offset_current, offset)
                            raise SpecificationError("Overlapping offset for cast %s:%s" % (parent.is_list, casts[0]))'''
                        value.children.append(self._cast_from_spec(specification, casts[1:], value, data_offset+i*casts[1:][0][1]))
                elif casts[0][0] == self.CastTypes.POINTER:
                    value.child = self._cast_from_spec(specification, casts[1:], value, data_offset)
                self.data_parsed.append(value)
            else:
                if casts[0][0] == self.CastTypes.POINTER_LIST:
                    value = []
                    for i in range(0, data[0]):
                        value.append(self._cast_from_spec(specification, casts[1:], value, data_offset+i*casts[1:][0][1]))
                elif casts[0][0] == self.CastTypes.POINTER:
                    value = self._cast_from_spec(specification, casts[1:], None, data_offset)
        # TODO:
        # if parent:
        #    self._data_offset_current = offset
        #    self.data_parsed.append(value)

        return value

    def _process_row(self, rowid):
        offset = 4 + rowid * self.table_record_length
        row_data = DatRecord(self, rowid)
        data_raw = self._file_raw[offset:offset+self.table_record_length]

        # We don't have any data, return early
        if len(data_raw) == 0:
            return row_data

        # Unpacking the entire row in one go will help breaking down the
        # function calls significantly
        row_unpacked = struct.unpack(self.cast_row, data_raw)
        i = 0
        for spec, casts in self.cast_spec:
            if casts[0][0] == 3:
                cell_data = row_unpacked[i:i+2]
                i += 1
            else:
                cell_data = (row_unpacked[i], )
            row_data.append(self._cast_from_spec(spec, casts, data=cell_data, offset=offset))
            offset += casts[0][1]
            i += 1

        return row_data

    def read(self, raw):
        # TODO consider memory issues for saving raw contents
        if isinstance(raw, bytes):
            self._file_raw = raw
        elif isinstance(raw, BytesIO):
            self._file_raw = raw.read()
        else:
            raise TypeError('Raw must be bytes or BytesIO instance, got %s' %
                            type)

        # Jump to last byte to get length
        self.file_length = len(self._file_raw)

        self.data_offset = self._file_raw.find(DAT_FILE_MAGIC_NUMBER)

        if self.data_offset == -1:
            raise ValueError(
                'Did not find data magic number in "%(file)s"' % {
                    'file': self.file_name,
                }
            )

        self.table_rows = struct.unpack('<I', self._file_raw[0:4])[0]
        self.table_length = self.data_offset - self._table_offset
        if self.table_rows > 0:
            self.table_record_length = self.table_length//self.table_rows
        elif self.table_rows == 0 and self.table_length == 0:
            self.table_record_length = 0
        else:
            # TODO
            raise ValueError("WTF")

        if self.specification is None:
            self.cast_size = self.table_record_length

        if self.cast_size != self.table_record_length:
            raise SpecificationError(
                SpecificationError.ERRORS.RUNTIME_ROWSIZE_MISMATCH,
                '"%(name)s": Specification row size %(spec_size)s vs real size %(cast_size)s' % {
                    'name': self.file_name,
                    'spec_size': self.cast_size,
                    'cast_size': self.table_record_length
                }
            )

        self.table_data = []

        # Prepare data section
        self.data_parsed = list()

        for i in range(0, self.table_rows):
            self.table_data.append(self._process_row(i))

        if self.auto_build_index:
            self.build_index()

        return self.table_data

    def print_data(self):
        """
        For debugging. Prints out data.
        """
        for row in self.table_data:
            print('Row: %s' % row.rowid)
            for k in row.keys():
                v = row[k]
                print('|- %s: %s' % (k, v))

    @deprecated
    def export_to_html(self, export_table=True, export_data=False):
        outstr = []
        if export_table:
            outstr.append('<table>')

            outstr.append('<thead>')
            outstr.append('<tr>')
            outstr.append('<th>')
            outstr.append('ROW')
            outstr.append('</th>')
            for key in self.specification['fields']:
                outstr.append('<th>')
                disp = self.specification['fields'][key]['display']
                if not disp:
                    disp = key
                outstr.append(disp)
                outstr.append('</th>')
            outstr.append('</tr>')
            outstr.append('</thead>')

            outstr.append('<tbody>')
            for row in self.table_data:
                outstr.append('<tr>')
                outstr.append('<th>')
                outstr.append(str(row.rowid))
                outstr.append('</th>')
                for dv in row:
                    outstr.append('<td>')
                    if self.use_dat_value:
                        outstr.append(str(dv.get_value()))
                    elif isinstance(dv, DatRecord):
                        outstr.append(str(dv.rowid))
                    else:
                        outstr.append(str(dv))
                    outstr.append('</td>')
                outstr.append('</tr>')
            outstr.append('</tbody>')

            outstr.append('</table>')
        if export_data:
            outstr.append('<table>')

            outstr.append('<thead>')
            outstr.append('<tr>')
            outstr.append('</tr>')
            outstr.append('</thead>')

            outstr.append('<tbody>')
            outstr.append('</tbody>')

            outstr.append('</table>')
        return ''.join(outstr)


class DatFile(AbstractFileReadOnly):
    """
    Representation of a .dat file.

    Attributes
    ----------
    reader : DatReader
        reference to the DatReader instance once :meth:`read` has been called
    """

    def __init__(self, file_name):
        """
        Parameters
        ----------
        file_name : str
            Name of the .dat file
        """
        self._file_name = file_name
        self.reader = None

    def __repr__(self):
        return 'DatFile<%s>(file_name="%s")' % (hex(id(self)), self._file_name)

    def _read(self, buffer, *args, **kwargs):
        self.reader = DatReader(self._file_name, **kwargs)
        self.reader.read(buffer.read())

        return self.reader


@doc(doc=AbstractFileCache, prepend="""
    Read dat files in a relational matter and cache them for further use.

    The relational reader will process **all** relations upon accessing a dat
    file; this means any field marked as relation or enum in the specification
    will be processed and the pointer will be replaced with the actual value.


    For example, if a row "OtherKey" points to another file "OtherDatFil.dat",
    the contents of "OtherKey" will no longer be a reference like 0, but instead
    the actual row from the file "OtherDatFile.dat".

    As a result you have equivalence of:

    * rr["DatFile.dat"]["OtherKey"]["OtherDatFileValue"]
    * rr["OtherDatFile.dat"][0]["OtherDatFileValue"]


    Enums are processed in a similar fashion, except they'll be replaced with
    the according enum instance from :py:mod:`PyPoE.poe.constants` for the
    specific value.
""")
class RelationalReader(AbstractFileCache):
    FILE_TYPE = DatFile

    @doc(doc=AbstractFileCache.__init__, append="""
    Parameters
    ----------
    raise_error_on_missing_relation : bool
        Raises error instead of issuing an warning when a relation is broken
    language : str
        language subdirectory in data directory
    """)
    def __init__(self, raise_error_on_missing_relation=False,
                 language=None, *args, **kwargs):
        self.raise_error_on_missing_relation = raise_error_on_missing_relation
        if language == 'English' or language is None:
            self._language = ''
        else:
            self._language = language + '/'
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        """
        Shortcut that also appends Data/ if missing

        The following calls are equivalent:

        * self['DF.dat'] <==> read_file('Data/DF.dat').reader
        * self['Data/DF.dat'] <==> read_file('Data/DF.dat').reader
        """
        if not item.startswith('Data/'):
            item = 'Data/' + self._language + item

        return self.get_file(item).reader

    def _set_value(self, obj, other, key, offset):
        if obj is None:
            obj = None
        elif key:
            try:
                obj = other.index[key][obj]
            except KeyError:
                msg = 'Did not find proper value for foreign key "%s" with ' \
                      'value "%s"' % (key, obj)
                if self.raise_error_on_missing_relation:
                    raise SpecificationError(
                        SpecificationError.ERRORS.RUNTIME_MISSING_FOREIGN_KEY,
                        msg
                    )
                else:
                    warnings.warn(msg, SpecificationWarning)
                    obj = None
        else:
            # offset is default 0
            try:
                obj = other[obj-offset]
            except IndexError:
                msg = 'Did not find proper value at index %s in %s' % (
                    obj-offset, other.file_name)
                if self.raise_error_on_missing_relation:
                    raise SpecificationError(
                        SpecificationError.ERRORS.RUNTIME_MISSING_FOREIGN_KEY,
                        msg
                    )
                else:
                    warnings.warn(msg, SpecificationWarning)
                    obj = None
        return obj

    def _dv_set_value(self, value, other, key, offset):
        if value.is_pointer:
            self._dv_set_value(value.child, other, key, offset)
        elif value.is_list:
            [self._dv_set_value(dv, other, key, offset) for dv in value.children]
        else:
            value.value = self._set_value(value.value, other, key, offset)

        return value

    def _simple_set_value(self, value, other, key, offset):
        if isinstance(value, list):
            return [self._set_value(item, other, key, offset) for item in value]
        else:
            return self._set_value(value, other, key, offset)

    def _get_file_instance_args(self, file_name, *args, **kwargs):
        opts = super()._get_file_instance_args(file_name)
        opts['file_name'] = file_name.replace('Data/' + self._language, '')
        return opts

    def get_file(self, file_name):
        """
        Attempts to return a dat file from the cache and if it isn't available,
        reads it in.

        During the process any relations (i.e. fields that have a "key" to
        other .dat files specified) will be read. This will result in the
        appropriate fields being replaced by the related row.
        Note that a related row may be "None" if no key was specified in the
        read dat file.

        Parameters
        ----------
        file_name :  str
            The name of the .dat to read. Extension is required.


        Returns
        -------
        DatFile
            Returns the given DatFile instance
        """
        if file_name in self.files:
            return self.files[file_name]

        df = self._create_instance(file_name)

        self.files[file_name] = df

        vf = self._dv_set_value if df.reader.use_dat_value else self._simple_set_value

        for key, spec_row in df.reader.specification.fields.items():
            if spec_row.key:
                if df.reader.x64:
                    spec_row_key = spec_row.key.replace('.dat', '.dat64')
                else:
                    spec_row_key = spec_row.key

                df_other_reader = self[spec_row_key]

                key_id = spec_row.key_id
                key_offset = spec_row.key_offset
                # Don't need to rebuild the index if it was specified as generic
                # read option already.
                if not self.read_options.get('auto_build_index') \
                        and not key_offset and key_id:
                    df_other_reader.build_index(key_id)

                index = df.reader.table_columns[key]['index']

                for i, row in enumerate(df.reader.table_data):
                    try:
                        df.reader.table_data[i][index] = vf(
                            row[index],
                            df_other_reader,
                            key_id,
                            key_offset,
                        )
                    except SpecificationError as e:
                        raise SpecificationError(
                            e.code,
                            '%(fn)s:%(rn)s->%(on)s:%(msg)s' % {
                                'fn': file_name,
                                'rn': key,
                                'on': spec_row.key,
                                'msg': e.msg,
                            },
                        )
            elif spec_row.enum:
                const_enum = getattr(constants, spec_row.enum)
                index = df.reader.table_columns[key]['index']
                for i, row in enumerate(df.reader.table_data):
                    df.reader.table_data[i][index] = vf(
                        value=row[index],
                        other=const_enum,
                        key=None,
                        offset=0
                    )

        return df


# =============================================================================
# Functions
# =============================================================================


def set_default_spec(version=constants.VERSION.DEFAULT, reload=False):
    """
    Sets the default specification to use for the dat reader.

    See :py:mod:`PyPoE.poe.file.specification.__init__` for more info

    Parameters
    ----------
    version : constants.VERSION
        Version of the game to load the default specification for.
    reload : bool
        Whether to reload the version.
    """
    global _default_spec
    _default_spec = load(version=version, reload=reload)

# =============================================================================
# Init
# =============================================================================


set_default_spec()
