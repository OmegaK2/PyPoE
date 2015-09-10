"""
Path     PyPoE/poe/file/dat.py
Name     Dat Reader Tool
Version  1.0.0a0
Revision $Id$
Author   [#OMEGA]- K2

INFO

Toolkit for reading & writing GGG .dat files.

.dat files can be found in Data/ and are read by the class DatFile.
Unfortunately, there is no magic keyword for identifying the GGG .dat format,
so advise caution when trying to read dat files.

The GGG .dat format uses a fixed-width table and a variable-length data section.
In the fixed-width table, the number of rows is defined, however, the data
format stored has to be reverse-engineered and is currently not stored in the
file itself.
The data is a continuous amount of binary data; reading values form there is
generally done by pointers (int) or list pointers (size, int) from the
table-data.

A list of default specification is included with PyPoE; to reload those or load
other specifications, load_spec may be used.


AGREEMENT

See PyPoE/LICENSE


TODO



KNOWN ISSUES

- DatValue.get_value might hit the python recursion limit, but is not a problem
  for any of the actual dat file.

"""

# =============================================================================
# Imports
# =============================================================================

# Python
import struct
import os
import multiprocessing
from io import BytesIO
from collections import OrderedDict

# 3rd Party Library
import configobj
import validate

# Library imports
from PyPoE import DAT_SPECIFICATION, DAT_SPECIFICATION_CONFIGSPEC
from PyPoE.shared.decorators import deprecated
from PyPoE.poe.file._shared import AbstractFileReadOnly
from PyPoE.poe.file.ggpk import GGPKFile

# =============================================================================
# Globals
# =============================================================================

_default_spec = None


__all__ = [
    'SpecificationError',
    'DatFile', 'RelationalReader',
    'load_spec', 'reload_default_spec',
]

# =============================================================================
# Classes
# =============================================================================

class SpecificationError(ValueError):
    pass

class DatValue(object):
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
    - works if the dat_value holds an integer
    - raises TypeError if it holds a list
    Example 2: dat_value1 < dat_value2
    - works if both dat values have the same or comparable types
    - raises TypeError if one holds a list, and the other an integer


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

    def __init__(self, value=None, offset=None, size=None, parent=None, specification=None):
        self.value = value
        self.size = size
        self.offset = offset
        self.parent = parent
        self.specification = specification
        self.children = None
        self.child = None

    def __repr__(self):
        #TODO: iterative vs recursive?
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
        Retrieves site of the data held by the current instance in the data
        section.

        :raises TypeError: If performed on DatValue instances without data

        :return: Returns the end offset
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

        :raises TypeError: If performed on DatValue instances without data

        :return: Returns the start offset
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

        :raises TypeError: If performed on DatValue instances without data

        :return: Returns the end offset
        """
        return self._get_data_start_offset() + self._get_data_size()

    def _is_data(self):
        """
        Whether this DatValue instance is data or not.

        :return: True or False
        :rtype: bool
        """
        return self.parent is not None

    def _has_data(self):
        """
        Whether this DatValue instance has data or not; this applies to types
        that hold a pointer.

        :return: True or False
        :rtype: bool
        """
        return self.is_list or self.is_pointer

    def _is_list(self):
        """
        Whether this DatValue instance is a list.

        :return: True or False
        :rtype: bool
        """
        return self.children is not None

    def _is_pointer(self):
        """
        Whether this DatValue instance is a pointer.

        :return: True or False
        :rtype: bool
        """
        return self.child is not None

    def _is_parsed(self):
        """
        Whether this DatValue instance is parsed (i.e. non bytes).

        :return: True or False
        :rtype: bool
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

        :return: Returns the dereference value
        """
        if self.is_pointer:
            return self.child.get_value()
        elif self.is_list:
            return [dv.get_value() for dv in self.children]
        else:
            return self.value

class RecordList(list):
    __slots__ = ['parent', 'rowid']

    def __init__(self, parent, rowid):
        list.__init__(self)
        self.parent = parent
        self.rowid = rowid

    def __getitem__(self, item):
        if isinstance(item, str):
            value = list.__getitem__(self, self.parent.table_columns[item]['index'])
            if isinstance(value, DatValue):
                value = value.get_value()
            return value
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

    def iter(self):
        """
        Iterates over the RecordList and returns key, value and index
        """
        for index, key in enumerate(self.parent.table_columns):
            yield key, self[key], index


    def keys(self):
        return self.parent.table_columns.keys()


class DatReader(object):
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
    }
    _data_magic_number = b'\xBB\xbb\xBB\xbb\xBB\xbb\xBB\xbb'

    def __init__(self, file_name, *args, use_dat_value=True, specification=None):
        self.data_parsed = []
        self.data_offset = 0
        self.file_length = 0
        self._file_raw = b''
        self.table_data = []

        self.table_length = 0
        self.table_record_length = 0
        self.table_rows = 0
        self.file_name = file_name

        #
        self.use_dat_value = use_dat_value

        # Process specification
        if specification is None:
            if file_name in _default_spec:
                specification = _default_spec[file_name]
            else:
                raise SpecificationError('No specification for "%s"' % file_name)
        else:
            specification = specification[file_name]
        self.specification = specification

        # Prepare the casts
        self.table_columns = OrderedDict()
        self.cast_size = 0
        self.cast_spec = []
        self.cast_row = []
        if specification:
            for i, key in enumerate(specification['fields']):
                k = specification['fields'][key]
                self.table_columns[key] = {'index': i, 'section': k}
                casts = []
                remainder = k['type']
                while remainder:
                    remainder, cast_type = self._get_cast_type(remainder)
                    casts.append(cast_type)
                self.cast_size += casts[0][1]

                self.cast_spec.append((k, casts))
                self.cast_row.append(casts[0][2])

            self.cast_row = '<' + ''.join(self.cast_row)

        else:
            s = configobj.Section(None, 0, None)
            s.name = 'Unparsed'
            self.table_columns.append(s)

    def __iter__(self):
        return iter(self.table_data)

    def __getitem__(self, item):
        return self.table_data[item]

    def row_iter(self):
        return iter(self.table_data)

    def column_iter(self):
        for ci, column in enumerate(self.table_columns):
            yield [item[ci] for item in self]

    def _get_cast_type(self, caststr):
        size = None
        cast = None
        remainder = ''
        if caststr in self._cast_table:
            cast_type = 1
            size = self._cast_table[caststr][1]
            cast = self._cast_table[caststr][0]
        elif caststr == 'string':
            cast_type = 2
        elif caststr.startswith('ref|list|'):
            cast_type = 3
            size = 8
            cast = 'II'
            remainder = caststr[9:]
        elif caststr.startswith('ref|'):
            cast_type = 4
            size = 4
            cast = 'I'
            remainder = caststr[4:]
        return remainder, (cast_type, size, cast)

    def _cast_from_spec(self, specification, casts, parent=None, offset=None, data=None, queue_data=None):
        if casts[0][0] == 1:
            ivalue = data[0] if data else struct.unpack('<' + casts[0][2], self._file_raw[offset:offset+casts[0][1]])[0]

            if ivalue in (-0x1010102, 0xFEFEFEFE, -0x101010101010102, 0xFEFEFEFEFEFEFEFE):
                ivalue = None

            if self.use_dat_value:
                value = DatValue(ivalue, offset, casts[0][1], parent, specification)
            else:
                value = ivalue
        elif casts[0][0] == 2:
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

        elif casts[0][0] >= 3:
            data = data if data else struct.unpack('<' + casts[0][2], self._file_raw[offset:offset+casts[0][1]])
            data_offset = data[-1] + self.data_offset

            # Instance..
            if self.use_dat_value:
                value = DatValue(data[0] if casts[0][0] == 4 else data, offset, casts[0][1], parent, specification)

                if casts[0][0] == 3:
                    value.children = []
                    for i in range(0, data[0]):
                        '''if offset < self._data_offset_current:
                            print(self._data_offset_current, offset)
                            raise SpecificationError("Overlapping offset for cast %s:%s" % (parent.is_list, casts[0]))'''
                        value.children.append(self._cast_from_spec(specification, casts[1:], value, data_offset+i*casts[1:][0][1]))
                elif casts[0][0] == 4:
                    value.child = self._cast_from_spec(specification, casts[1:], value, data_offset)
                self.data_parsed.append(value)
            else:
                if casts[0][0] == 3:
                    value = []
                    for i in range(0, data[0]):
                        value.append(self._cast_from_spec(specification, casts[1:], value, data_offset+i*casts[1:][0][1]))
                elif casts[0][0] == 4:
                    value = self._cast_from_spec(specification, casts[1:], None, data_offset)
        # TODO
        #if parent:
        #    self._data_offset_current = offset
        #    self.data_parsed.append(value)

        return value

    def _process_row(self, rowid):
        offset = 4 + rowid * self.table_record_length
        row_data = RecordList(self, rowid)
        data_raw = self._file_raw[offset:offset+self.table_record_length]
        if self.cast_spec:
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
        else:
            unparsed = DatValue(value=data_raw, offset=offset, size=self.table_record_length)
            row_data.append(unparsed)
            offset += self.table_record_length

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

        self.data_offset = self._file_raw.find(self._data_magic_number)

        if self.data_offset == -1:
            raise ValueError(
                'Did not find data magic number in "%(file)s"' % {
                    'file:': self.file_name,
                }
            )

        self.table_rows = struct.unpack('<I', self._file_raw[0:4])[0]
        self.table_length = self.data_offset - self._table_offset
        if self.table_rows > 0:
            self.table_record_length = self.table_length//self.table_rows
        elif self.table_rows == 0 and self.table_length == 0:
            self.table_record_length = 0
        else:
            #TODO
            raise ValueError("WTF")

        if self.specification is None:
            self.cast_size = self.table_record_length

        if self.cast_size != self.table_record_length:
            raise SpecificationError(
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

        return self.table_data

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
                    elif isinstance(dv, RecordList):
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
    """
    
    def __init__(self, file_name, *args, read_file=None, read_raw=None, options={}):
        self._file_name = file_name
        self.reader = None

        if read_file and read_raw:
            raise ValueError('Only one of read_file and read_raw should be set.')

        if read_file:
            self.read(os.path.join(read_file, file_name), **options)
        elif read_raw:
            self.read(read_raw, **options)

    def print_data(self):
        for row in d.table_data:
            print('Row: %s' % row.rowid)
            for k in row.keys():
                v = row[k]
                print('|- %s: %s' % (k, v))

    def _read(self, buffer, *args, **kwargs):
        self.reader = DatReader(self._file_name, **kwargs)
        self.reader.read(buffer.read())

        return self.reader

    @deprecated(message='Use of %(func)s is deprecated, use read instead.')
    def read_from_file(self, path, **options):
        return self.read(os.path.join(path, self._file_name), **options)

    @deprecated(message='Use of %(func)s is deprecated, use read instead.')
    def read_from_raw(self, raw, **options):
        """
        Specification as _ordered_ dictionary key:value format
        """
        return self.read(raw, **options)


class RelationalReader(object):
    """
    Read dat files in a relational matter.

    This acts both as a cache and as a way to easily access the instances.
    """
    def __init__(self, path_or_ggpk=None, files=None, options=None):
        """
        Creates a new Relational Reader instance.

        See DatReader for details on the options available.

        :param path_or_ggpk: The path where the dat files are stored or a
        GGPKFile instance
        :type path_or_ggpk: :class:`GGPKFile` or str
        :param Iterable files: Iterable of files that will be loaded right away
        :param dict: options to pass to the reader for the DatFile

        :raises TypeError: if path_or_ggpk not specified or invalid type
        :raises ValueError: if a GGPKFile was passed, but it was not parsed
        """
        if isinstance(path_or_ggpk, GGPKFile):
            if not self._ggpk.is_parsed:
                raise ValueError('The GGPK File must be parsed.')
            self._ggpk = path_or_ggpk
            self._path = None
        elif isinstance(path_or_ggpk, str):
            self._ggpk = None
            self._path = path_or_ggpk
        else:
            raise TypeError('path_or_ggpk must be a valid directory or GGPKFile')

        self.options = {} if options is None else options

        self.files = {}
        for file_name in files:
            self.read_file(file_name)

    def __getitem__(self, item):
        """
        Shortcut.

        self[item] <==> read_file(item).reader
        """
        return self.read_file(item).reader

    def _set_value(self, obj, other, key, offset):
        if obj is None:
            obj = None
        elif offset:
            obj = other[obj-offset]
        elif key:
            for row in other:
                if row[key] == obj:
                    obj = row
                    break
            if obj is not row:
                raise SpecificationError('Did not find proper value for foreign key %s' % key)
        else:
            obj = other[obj]
        return obj

    def _dv_set_value(self, value, other, key, offset):
        if value.is_pointer:
            self._dv_set_value(value.child, other, key, offset)
        elif value.is_list:
            [self._dv_set_value(dv, other, key, offset) for dv in self.children]
        else:
            value.value = self._set_value(value.value, other, key, offset)

        return value

    def _simple_set_value(self, value, other, key, offset):
        if isinstance(value, list):
            return [self._set_value(item, other, key, offset) for item in value]
        else:
            return self._set_value(value, other, key, offset)

    def read_file(self, name):
        """
        Attempts to return a dat file from the cache and if it isn't available,
        reads it in.

        During the process any relations (i.e. fields that have a "key" to
        other .dat files specified) will be read. This will result in the
        appropriate fields being replaced by the related row.
        Note that a related row may be "None" if no key was specified in the
        read dat file.

        :param str name: The name of the .dat to read. Extension is required.
        :return: Returns the given DatFile instance
        :rtype: DatFile
        """
        if name in self.files:
            return self.files[name]

        if self._ggpk:
            df = DatFile(
                name,
                read_raw=self._ggpk.directory['Data'][name].node.extract(),
                options=self.options
            )
        elif self._path:
            df = DatFile(name, read_file=self._path, options=self.options)

        self.files[name] = df

        vf = self._dv_set_value if df.reader.use_dat_value else self._simple_set_value

        for key in df.reader.specification['fields']:
            other = df.reader.specification['fields'][key]['key']
            if not other:
                continue
            df_other = self.read_file(other)

            key_id = df.reader.specification['fields'][key]['key_id']
            key_offset = df.reader.specification['fields'][key]['key_offset']

            index = df.reader.table_columns[key]['index']

            for i, row in enumerate(df.reader.table_data):
                df.reader.table_data[i][index] = vf(
                    row[index],
                    df_other.reader,
                    key_id,
                    key_offset,
                )

        return df



# =============================================================================
# Functions
# =============================================================================

def load_spec(path=None):
    """
    Loads a specification that can be used for the dat files. It will be
    verified and errors will be raised accordingly if any errors occur.

    :param str path: If specified, read the specified file as config
    :return: returns the ConfigObj of the read file.
    :rtype: :class:`ConfigObj`

    :raises SpecificationError: if key or key_id point to invalid files or
    keys respectively
    """
    if path is None:
        path = DAT_SPECIFICATION
    spec = configobj.ConfigObj(infile=path, configspec=DAT_SPECIFICATION_CONFIGSPEC)
    spec.validate(validate.Validator())

    for file_name in spec:
        for f in spec[file_name]['fields']:
            other = spec[file_name]['fields'][f]['key']
            if not other:
                continue
            if other not in spec:
                raise SpecificationError(
                    '%(dat_file)s->%(field)s->key: %(other)s not in '
                    'specification' % {
                        'dat_file': file_name,
                        'field': f,
                        'other': other,
                    }
                )

            other_key = spec[file_name]['fields'][f]['key_id']
            if not other_key:
                continue
            if other_key not in spec[other]['fields']:
                raise SpecificationError(
                    '%(dat_file)s->%(field)s->key_id: %(other)s->%(other_key)s'
                    ' not in specification' % {
                        'dat_file': file_name,
                        'field': f,
                        'other': other,
                        'other_key': other_key,
                    }
                )

    return spec

def reload_default_spec():
    """
    Reloads the default specification.
    """
    global _default_spec
    _default_spec = load_spec()

# =============================================================================
# Init
# =============================================================================

reload_default_spec()
        
if __name__ == '__main__':
    from line_profiler import LineProfiler
    profiler = LineProfiler()
    #profiler.add_function(DatValue.__init__)
    #profiler.add_function(DatReader._cast_from_spec)
    #profiler.add_function(DatReader._process_row)
    #profiler.add_function(RecordList.__getitem__)

    #profiler.run("d = DatFile('GrantedEffects.dat', read_file='C:/Temp/Data')")
    #profiler.run("for i in range(0, 10000): d.reader[0]['Data1']")
    #profiler.print_stats()

    #print(d.reader[0])

    #profiler.add_function(RelationalReader._set_value)
    #profiler.add_function(RelationalReader._dv_set_value)
    #profiler.add_function(RelationalReader._simple_set_value)
    #profiler.add_function(RelationalReader.read_file)
    #profiler.run("r = RelationalReader('C:/Temp/Data', files=['BaseItemTypes.dat'], options={'use_dat_value': False})")
    #profiler.print_stats()

    #for a in d.reader.column_iter(): print(a)

    #r = RelationalReader(path_or_ggpk='C:/Temp/Data', files=['BaseItemTypes.dat'], options={'use_dat_value': True})
    #print(r.files['BaseItemTypes.dat'].reader[0]['ItemVisualIdentityKey'])

    #print(d.table_data)
    import cProfile
    #cProfile.run("d = DatFile('GrantedEffectsPerLevel.dat', read_file='C:/Temp/Data')")

